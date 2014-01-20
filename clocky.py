import Image, ImageFont, ImageDraw
import time, datetime
from BlinkyTape import BlinkyTape

bb = BlinkyTape('/dev/ttyACM0')

font_sm = ImageFont.truetype("3-by-5-Pixel-Font.ttf", 8)
top_off = 0
left_off = -24
c_mult = 0.2
hr_color = tuple([int(s*c_mult) for s in [0x24, 0x13, 0x5F]])
min_color = tuple([int(s*c_mult) for s in [0xDF, 0x46, 0x01]])
frame_delay = 10 # 0.2

width = 8
height = 8

hr_disp = Image.new("RGB", (width, height), "black")
hr_disp_draw = ImageDraw.Draw(hr_disp)
min_disp = Image.new("RGB", (width, height), "black")
min_disp_draw = ImageDraw.Draw(min_disp)

forbidden_pixels = {
  (0,0): 1,
  (0,7): 1,
  (7,0): 1,
  (7,7): 1
}
dt = 8
first_pass = True;
while True:
  hr_disp.paste("black", (0,0,width,height))
  min_disp.paste("black", (0,0,width,height))
  now = datetime.datetime.now()
  #t = now.strftime("%I:%M").lstrip("0")
  h = now.strftime("%I")
  m = now.strftime("%M")
  # Blended
  hr_disp_draw.text((1,3), m, font=font_sm, fill=min_color)
  hr_disp_draw.text((0,0), h, font=font_sm, fill=hr_color)
  min_disp_draw.text((0,0), h, font=font_sm, fill=hr_color)
  min_disp_draw.text((1,3), m, font=font_sm, fill=min_color)
  disp = Image.blend(hr_disp, min_disp, 0.65)

  # Minutes on top
#  min_disp_draw.text((0,0), h, font=font_sm, fill=(10,10,0))
#  min_disp_draw.text((1,3), m, font=font_sm, fill=(20,20,0))
#  disp = min_disp

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
  if(first_pass):
    time.sleep(0.2)
    bb.show()
    time.sleep(0.2)
    bb.show()
    first_pass = False
  time.sleep(frame_delay)
