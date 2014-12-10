from __future__ import division
from PIL import Image, ImageDraw
import os, sys, string
from operator import itemgetter

white = (255, 255, 255)

# Delimit the area around the Characters
def getBoxes(image, rgbImage):
  
  width, height = image.size

  boxes = []
  whiteLine = True
  readingChar = False
  
  charStartX = 0
  charEndX = 0

  # Start reading the image
  for x in range(0, width):

    # Read one vertical line  
    for y in range(0, height):
      if rgbImage.getpixel((x, y)) != white:
        whiteLine = False
        break;
      whiteLine = True

    if whiteLine == False:
      if readingChar == False:
        charStartX = x
        readingChar = True
    else:
      if readingChar == True:
        charEndX = x
        readingChar = False

        # Get the box height
        charStartY, charEndY = getBoxHeight(rgbImage, width, height, charStartX, charEndX)
        boxes.append((charStartX, charEndX, charStartY, charEndY))

  return boxes

# Get the height of the character box
def getBoxHeight(rgbImage, width, height, charStartX, charEndX):

  whiteLine = True
  readingChar = False

  charStartY = 0
  charEndY = 0

  for y in range(0, height):
    for x in range(charStartX, charEndX):
      if rgbImage.getpixel((x, y)) != white:
        whiteLine = False
        break;
      whiteLine = True

    if whiteLine == False:
      if readingChar == False:
        charStartY = y
        readingChar = True
    else:
      if readingChar == True:
        charEndY = y
        readingChar = False

  return (charStartY, charEndY)

# Read white spaces
def getSpaces(image, rbgImage):

  width, height = image.size

  spaces = []
  whiteLine = True
  readingSpace = False
  
  spaceStartX = 0
  spaceEndX = 0

  # Start reading image
  for x in range(0, width):

    # Read one vertical line  
    for y in range(0, height):
      if rgbImage.getpixel((x, y)) != white:
        whiteLine = False
        break;
      whiteLine = True

    if whiteLine == False:
      if readingSpace == True:
        spaceEndX = x
        readingSpace = False
        spaces.append((spaceStartX, spaceEndX))
    else:
      if readingSpace == False:
        spaceStartX = x
        readingSpace = True

  return spaces

# Get the spaces read and insert them in the box list
def mergeSpacesIntoBoxes(boxes, spaces, imageHeight):

  # Identify and add the Spaces. Avg may not be a good method
  s = 0
  for space in spaces:
    s = s + (space[1] - space[0])

  average = s / len(spaces)
  spaceInBoxes = []
  for space in spaces:
    if space[1] - space[0] > average + 1:
      spaceInBoxes.append((space[0], space[1], 0, imageHeight))

  boxes = boxes + spaceInBoxes
  boxes = sorted(boxes, key=itemgetter(0))

  return boxes

# Run a XNOR in the read box matrix against the trained matrix
def xnor(box, matrix):

  # Compare it against each character in the trained matrix
  results = []
  for character in matrix:
    
    # Check if the boxes are the same size
    letter = character[0]
    width = character[1]
    height = character[2]
    positives = 0

    # If the box read is too big, we scale it down to match the trained box
    subImage = rgbImage.crop((box[0], box[2], box[1], box[3]))
    boxWidth, boxHeight = subImage.size
    trainedWidth, trainedHeight = (int(character[1]), int(character[2]))
    
    if boxWidth > trainedWidth and boxHeight > trainedHeight:
      subImage = subImage.resize((trainedWidth, trainedHeight), Image.NEAREST)
      boxWidth, boxHeight = subImage.size
    
    # Read this character's matrix
    boxMatrix = []
    for y in range(0, boxHeight):
      for x in range(0, boxWidth):
        if subImage.getpixel((x, y)) == white:
          boxMatrix.append("0")
        else:
          boxMatrix.append("1")

    boxSize = boxWidth * boxHeight
    trainedSize = trainedWidth * trainedHeight
    size = 0
    if boxSize < trainedSize:
      size = boxSize
    else:
      size = trainedSize

    # XNOR
    for i in range(0, size):
      if character[i + 3] == boxMatrix[i]:
        positives = positives + 1

    if size == 0:
      size = 1
    ratio = positives / size
    
    if all(item == "0" for item in boxMatrix): # Check if space
      results.append((" ", 0))
    elif positives > 0: # A character!
      results.append((letter, ratio))

  results = sorted(results, key=itemgetter(1), reverse=True)

  # Print the results
  if results[0][1] == 0:
    print " "
  else:
    print str(results[0][0]) + " - " + str(results[0][1] * 100) + "% sure"

  return results

# Open the trained OCR table
def readOCRMatrix(fontName):

  f = open(fontName + ".ocr", "r")
  content = f.read()

  matrix = []
  
  for line in content.split("\n"):
    lineSplit = line.split(",")
    if len(lineSplit) == 1:
      break;

    matrix.append((lineSplit))

  f.close()
  return matrix

# ----------------------------------------------------------------------------------------------------------

if len(sys.argv) == 2:
  filename = sys.argv[1]
else:
  print "Usage: python ocr.py filename"
  print "Example: python ocr.py image.png"
  sys.exit()

# Open the image to be read
fontName = "Helvetica"
image = Image.open(filename)
rgbImage = image.convert("RGB")
width, height = image.size

# Read the trained ocr table
matrix = readOCRMatrix(fontName)

# Get the boxes
boxes = getBoxes(image, rgbImage)
spaces = getSpaces(image, rgbImage)
boxes = mergeSpacesIntoBoxes(boxes, spaces, height)

# Read the image and try to identify the Characters
for box in boxes:
  result = xnor(box, matrix)

print "---"
