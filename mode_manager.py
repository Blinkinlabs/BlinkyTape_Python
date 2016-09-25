import time
import sys
import optparse
from blinkytape import BlinkyTape


class ModeManager(object):
    def __init__(self, port):
        self.bb = BlinkyTape(port)

    def render(self, colors):
        self.bb.send_list(colors)

    def run_mode(self, mode):
        while True:
            start = time.time()
            mode.calc_next_step()
            self.render(mode.get_colors())
            if not mode.no_sleep:
                renderTime = time.time() - start
                sleepTime = 1.0 / mode.fps - renderTime
                if sleepTime >= 0.0:
                    time.sleep(sleepTime)
            diff = time.time() - start
            sys.stdout.write("%.02f fps                    \r" % (1.0 / diff))


if __name__ == "__main__":
    # Default Blinky Tape port on Raspberry Pi is /dev/ttyACM0
    parser = optparse.OptionParser()
    parser.add_option("-p", "--port", dest="portname",
                      help="serial port (ex: /dev/ttyACM0)", default="/dev/ttyACM0")
    (options, args) = parser.parse_args()

    port = options.portname

    mm = ModeManager(port)
    from IPython import embed

    embed()
