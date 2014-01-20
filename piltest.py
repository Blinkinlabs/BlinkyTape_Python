import Image, ImageFont, ImageDraw
import time, datetime
from BlinkyTape import BlinkyTape

bb = BlinkyTape('/dev/ttyACM0')

font_sm = ImageFont.truetype("3-by-5-Pixel-Font.ttf", 8)
top_off = 0
left_off = -24
fill_color = (32,32,32)
frame_delay = 10 # 0.2

width = 8
height = 8

disp = Image.new("RGB", (width, height), "black")
disp_draw = ImageDraw.Draw(disp)

forbidden_pixels = {
  (0,0): 1,
  (0,7): 1,
  (7,0): 1,
  (7,7): 1
}
dt = 8
while True:
  disp.paste("black", (0,0,width,height))
  now = datetime.datetime.now()
  #t = now.strftime("%I:%M").lstrip("0")
  h = now.strftime("%I")
  m = now.strftime("%M")
  #disp_draw.text((dt,top_off), t, font=font_sm, fill=fill_color)
  disp_draw.text((0,0), h, font=font_sm, fill=(16,0,16))
  disp_draw.text((1,3), m, font=font_sm, fill=(20,20,0))
  dt -= 1
  if(dt < left_off):
    dt = 8
  pixels = disp.load()
  
  for x in range(width):
    buf = []
    for y in range(height-1,-1,-1):
      if((x,y) not in forbidden_pixels):
        if(x % 2 == 0):
	  buf.append(pixels[x,y])
	else:
	  buf.insert(0,pixels[x,y])
    for i in range(len(buf)):
      bb.sendPixel(*buf[i])
  bb.show()
  time.sleep(frame_delay)
