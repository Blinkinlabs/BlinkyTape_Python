import sys
import time

from socket import (socket, AF_INET, SOCK_DGRAM)
from struct import unpack

import BlinkyTape


UDP_IP = "" # listen on all sockets- INADDR_ANY
UDP_PORT = 0x1936 # Art-net is supposed to only use this address


PIXELS_PER_UNIVERSE = 170 # Number of pixels to expect on a universe
BYTES_PER_PIXEL = 3

BLINKYTAPE_DEVICE = "/dev/ttyACM0"
BLINKYTAPE_LENGTH = 450



class ArtnetPacket:

    ARTNET_HEADER = b'Art-Net\x00'
    OP_OUTPUT = 0x0050

    def __init__(self):
        self.op_code = None
        self.ver = None
        self.sequence = None
        self.physical = None
        self.universe = None
        self.length = None
        self.data = None

    @staticmethod
    def unpack_raw_artnet_packet(raw_data):

        if unpack('!8s', raw_data[:8])[0] != ArtnetPacket.ARTNET_HEADER:
            return None

        packet = ArtnetPacket()

        # We can only handle data packets
        (packet.op_code,) = unpack('!H', raw_data[8:10])
        if packet.op_code != ArtnetPacket.OP_OUTPUT:
            return None
 
 
        (packet.op_code, packet.ver, packet.sequence, packet.physical,
            packet.universe, packet.length) = unpack('!HHBBHH', raw_data[8:18])
 
        (packet.universe,) = unpack('<H', raw_data[14:16])
 
        (packet.data,) = unpack(
            '{0}s'.format(int(packet.length)),
            raw_data[18:18+int(packet.length)])
 
        return packet


def blinkytape_artnet_receiver():
    print(("Listening in {0}:{1}").format(UDP_IP, UDP_PORT))

    sock = socket(AF_INET, SOCK_DGRAM)  # UDP
    sock.bind((UDP_IP, UDP_PORT))

    bt = BlinkyTape.BlinkyTape(BLINKYTAPE_DEVICE, BLINKYTAPE_LENGTH)


    lastSequence = 0

    packetCount = 0
    lastTime = time.time()

    datas = []

    while True:
        try:
            data, addr = sock.recvfrom(1024)
            packet = ArtnetPacket.unpack_raw_artnet_packet(data)

            if packet != None:
		#print("Sequence=%i universe=%i"%(packet.sequence,packet.universe))
                packetCount += 1

                while len(datas) < packet.universe + 1:
                    print("adding new universe %i"%(packet.universe))
                    datas.append('')

                datas[packet.universe] = packet.data

                # Send an update to the tape when a new sequence is received on the last universe
            	if packet.universe == (len(datas)-1) and lastSequence != packet.sequence:
                    outputData = ''
                    #print(datas)

                    for data in datas:
                        if len(data) > PIXELS_PER_UNIVERSE*BYTES_PER_PIXEL:
                            data = data[0:PIXELS_PER_UNIVERSE*BYTES_PER_PIXEL]

                        if len(data) < PIXELS_PER_UNIVERSE*BYTES_PER_PIXEL:
                            data += '\x00' * (PIXELS_PER_UNIVERSE*BYTES_PER_PIXEL - len(data))

                        outputData += data

                        #print(len(outputData))

                    bt.sendData(outputData)
                    lastSequence = packet.sequence


            if time.time() > lastTime+1:
                print("Packets per second: %i"%(packetCount))
                packetCount = 0
                lastTime = time.time()

        except KeyboardInterrupt:
            sock.close()
            sys.exit()

blinkytape_artnet_receiver()
