from PIL import Image, ImageDraw, ImageFont
import os, subprocess, string, sys

white = (255, 255, 255)

# Creates png image files for each character in the font
def textToImage(fontName, fontSize):

  font = ImageFont.truetype("fonts/" + fontName + ".ttf", fontSize)

  letters = string.ascii_uppercase
  for letter in letters:
    
    image = Image.new("RGB", (200, 120), white)
    draw = ImageDraw.Draw(image)
    draw.text((0, 0), letter, fill='black', font=font)
    filename = "characters/" + fontName + "-" + str(fontSize) + "-" + letter + ".png"
    image.save(filename)

# Count the amount of pixels in each section of the character image
def generatePixelMatrix(fontName, fontSize):

  f = open(fontName + ".ocr", "w")

  letters = string.ascii_uppercase
  for letter in letters:

    image = Image.open("characters/" + fontName + "-" + str(fontSize) + "-" + letter + ".png")
    rgbImage = image.convert("RGB")

    width, height = image.size

    # For each pixel: 0 is white, 1 is black
    matrix = []

    # Loop
    for y in range(0, height):
      for x in range(0, width):
        if rgbImage.getpixel((x, y)) == white:
          matrix.append("0")
        else:
          matrix.append("1")

    matrixToWrite = ""
    for i in range(0, len(matrix)):
      matrixToWrite = matrixToWrite + "," + matrix[i]

    f.write(letter + "," + str(width) + "," + str(height) + str(matrixToWrite) + "\n")

  f.close()

# -------------------------------

if len(sys.argv) == 2:
  fontName = sys.argv[1]
else:
  print "Usage: python train.py font-name"
  print "Example: python train.py Helvetica"
  sys.exit()

fontSize = 42
os.system("rm characters/*.png > /dev/null 2>&1")
textToImage(fontName, fontSize)
os.system("mogrify -trim characters/" + fontName + "-" + str(fontSize) + "-" + "*.png")
generatePixelMatrix(fontName, fontSize)
