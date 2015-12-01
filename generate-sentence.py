from PIL import Image, ImageDraw, ImageFont
import os
import string
import sys

white = (255, 255, 255)

if len(sys.argv) == 3:
  fontName = sys.argv[1]
  fontSize = int(sys.argv[2])
else:
  print("Usage: python generate-sentence.py font-name font-size")
  print("Example: python generate-sentence.py Helvetica 72")
  sys.exit()

font = ImageFont.truetype("fonts/" + fontName + ".ttf", fontSize)
image = Image.new("RGB", (fontSize * 30, fontSize), white)
draw = ImageDraw.Draw(image)
draw.text((0, 0), "THE QUICK BROWN FOX JUMPS OVER THE LAZY DOG", fill='black', font=font)
filename = "read.png"
image.save(filename)
os.system("convert -quality 1 read.png read.jpg")
os.system("convert -blur 0x1 read.jpg read.jpg")
os.system("convert -threshold 50% read.jpg image.png")
os.system("rm read.png")
os.system("rm read.jpg")