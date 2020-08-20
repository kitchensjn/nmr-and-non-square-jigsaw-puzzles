import random
from PIL import Image


def combineConstraints(c1, c2, c3, c4):
  """
  Aggregates all building constraints from edges

  Parameters
  c1,c2,c3,c4: dictionaries, edge building constraints

  Return
  dictionary, all edge building constraints
  """
  for element in c2:
    c1[element] = c2[element]
  for element in c3:
    c1[element] = c3[element]
  for element in c4:
    c1[element] = c4[element]
  return c1

def surroundingCoordinates(x,y,max):
  """
  Calculates coordinates surrounding (x,y)

  Parameters
  x: integer, x coordinate of piece
  y: integer, y coordinate of piece
  max: integer, size of puzzle

  Return
  list, surrounding coordinates
  """
  coords = []
  if x != 0:
    coords.append((x-1,y))
  if x != max:
    coords.append((x+1,y))
  if y != 0:
    coords.append((x,y-1))
  if y != max:
    coords.append((x,y+1))
  return coords


class Puzzle:

  def __init__(self, pieceSize, puzzleSize, pieces=[], scramble=True, nonSquare=False):
    """
    Creates puzzle

    Parameters
    pieceSize: integer, number of pixels in length/width of piece
    puzzleSize: integer, number of pieces in length, width of puzzle
    pieces: list, ordered list of lists of pieces in corresponding position
    scramble: boolean, scramble the pieces after making
    nonSquare: boolean, whether any empty coordinates throughout puzzle
    """
    self.pieces = pieces
    self.pieceSize = pieceSize
    self.puzzleSize = puzzleSize
    if len(self.pieces) == 0:
      for vertical in range(self.puzzleSize):
        puzzleCanvasLine = []
        for horizontal in range(self.puzzleSize):
          puzzleCanvasLine.append("-")
        self.pieces.append(puzzleCanvasLine)

      pieceByLocation = []  # a dictionary containing the locations of every placed piece
      previouslyUsedCoordinates = []

      vertical = random.randrange(0,len(self.pieces))
      horizontal = random.randrange(0, len(self.pieces[0]))

      pieceByLocation.append((horizontal, vertical))
      while len(pieceByLocation) > len(previouslyUsedCoordinates):
        coordinateCheck = False
        while coordinateCheck == False:  # this loop ensures that randomly selected coordinate is not used more than once
          coordinate = pieceByLocation[random.randrange(0, len(pieceByLocation))]
          if coordinate not in previouslyUsedCoordinates:
            previouslyUsedCoordinates.append(coordinate)
            coordinateCheck = True
        if nonSquare == True:
          if len(pieceByLocation) == 1:
            pass
          else:
            skipPiece = random.randrange(0, 3)
            if skipPiece == 1:
              continue
        self.pieces[coordinate[1]][coordinate[0]] = 1
        surCoor = surroundingCoordinates(coordinate[0],coordinate[1],self.puzzleSize-1)
        for coor in surCoor:
          if coor not in pieceByLocation:
            pieceByLocation.append(coor)
      for vertical in range(len(self.pieces)):
        for horizontal in range(len(self.pieces[0])):
          if self.pieces[vertical][horizontal] == 1:
            top = {}
            bottom = {}
            left = {}
            right = {}
            if horizontal == 0 or self.pieces[vertical][horizontal - 1] == "-":
              for mid in range(1, self.pieceSize - 1):
                left[str(mid) + ",0"] = 0
            elif self.pieces[vertical][horizontal - 1] != "-":
              left = self.pieces[vertical][horizontal - 1].rightConstraints
            if horizontal == puzzleSize - 1 or self.pieces[vertical][horizontal + 1] == "-":
              for mid in range(1, self.pieceSize - 1):
                right[str(mid) + "," + str(self.pieceSize - 1)] = 0
            if vertical == 0 or self.pieces[vertical - 1][horizontal] == "-":
              for mid in range(1, self.pieceSize - 1):
                top["0," + str(mid)] = 0
            elif self.pieces[vertical - 1][horizontal] != "-":
              top = self.pieces[vertical - 1][horizontal].bottomConstraints
            if vertical == puzzleSize - 1 or self.pieces[vertical + 1][horizontal] == "-":
              for mid in range(1, self.pieceSize - 1):
                bottom[str(self.pieceSize - 1) + "," + str(mid)] = 0
            allConstraints = combineConstraints(c1=top, c2=bottom, c3=left, c4=right)
            self.pieces[vertical][horizontal] = JigsawPiece(size=self.pieceSize, buildingConstraints=allConstraints)
      for vertical in range(len(self.pieces)):
        for horizontal in range(len(self.pieces[0])):
          if self.pieces[vertical][horizontal] == "-":
            self.pieces[vertical][horizontal] = JigsawPiece(size=self.pieceSize, empty=True)
    if scramble == True:
      self.scrambledPieces = []
      for individual in self.pieces:
        for ip in individual:
          self.scrambledPieces.append(ip)
      random.shuffle(self.scrambledPieces)
      for pp in self.scrambledPieces:
        rotations = random.randrange(0, 4)
        if pp.empty == False:
          for r in range(rotations):
            pp.rotatePiece()

  def displaySolved(self, path, type=""):
    """
    Saves entire puzzle as a png

    Parameters
    path: string, path to output png
    type: string, 'answer' or not, changes which it uses orientation is used when placing pieces
    """
    outFile = path
    out = Image.new("RGB", (self.pieceSize * self.puzzleSize, self.pieceSize * self.puzzleSize))
    for line in range(len(self.pieces)):
      for piece in range(len(self.pieces[line])):
        if type == "answer":
          for pixelLine in range(len(self.pieces[line][piece].pieceInfo)):
            for pixel in range(len(self.pieces[line][piece].pieceInfo[pixelLine])):
              if self.pieces[line][piece].pieceInfo[pixelLine][pixel] == "-":
                out.putpixel(((piece * self.pieceSize + pixel), (line * self.pieceSize + pixelLine)),(0, 0, 0))
              elif (line % 2 == 0 and piece % 2 == 0):
                if self.pieces[line][piece].pieceInfo[pixelLine][pixel] == -1:
                  out.putpixel(((piece * self.pieceSize + pixel), (line * self.pieceSize + pixelLine)),(191, 63, 65))
                else:
                  out.putpixel(((piece * self.pieceSize + pixel), (line * self.pieceSize + pixelLine)),(63, 116, 191))
              elif (line % 2 == 1 and piece % 2 == 1):
                if self.pieces[line][piece].pieceInfo[pixelLine][pixel] == -1:
                  out.putpixel(((piece * self.pieceSize + pixel), (line * self.pieceSize + pixelLine)),(191, 63, 65))
                else:
                  out.putpixel(((piece * self.pieceSize + pixel), (line * self.pieceSize + pixelLine)),(63, 116, 191))
              else:
                if self.pieces[line][piece].pieceInfo[pixelLine][pixel] == -1:
                  out.putpixel(((piece * self.pieceSize + pixel), (line * self.pieceSize + pixelLine)),(63, 116, 191))
                else:
                  out.putpixel(((piece * self.pieceSize + pixel), (line * self.pieceSize + pixelLine)),(191, 63, 65))
        else:
          for pixelLine in range(len(self.pieces[line][piece].solvedOrientation)):
            for pixel in range(len(self.pieces[line][piece].solvedOrientation[pixelLine])):
              if self.pieces[line][piece].solvedOrientation[pixelLine][pixel] == "-":
                out.putpixel(((piece * self.pieceSize + pixel), (line * self.pieceSize + pixelLine)),(0, 0, 0))
              elif (line % 2 == 0 and piece % 2 == 0):
                if self.pieces[line][piece].solvedOrientation[pixelLine][pixel] == -1:
                  out.putpixel(((piece * self.pieceSize + pixel), (line * self.pieceSize + pixelLine)), (191, 63, 65))
                else:
                  out.putpixel(((piece * self.pieceSize + pixel), (line * self.pieceSize + pixelLine)), (63, 116, 191))
              elif (line % 2 == 1 and piece % 2 == 1):
                if self.pieces[line][piece].solvedOrientation[pixelLine][pixel] == -1:
                  out.putpixel(((piece * self.pieceSize + pixel), (line * self.pieceSize + pixelLine)), (191, 63, 65))
                else:
                  out.putpixel(((piece * self.pieceSize + pixel), (line * self.pieceSize + pixelLine)), (63, 116, 191))
              else:
                if self.pieces[line][piece].solvedOrientation[pixelLine][pixel] == -1:
                  out.putpixel(((piece * self.pieceSize + pixel), (line * self.pieceSize + pixelLine)), (63, 116, 191))
                else:
                  out.putpixel(((piece * self.pieceSize + pixel), (line * self.pieceSize + pixelLine)), (191, 63, 65))
    out.save(outFile)


class JigsawPiece:

  def __init__(self, size, empty = False, buildingConstraints = {}):
    """
    Creates a square puzzle piece with jagged edges.
    Pixels along edges have three states (-1-concave, 0-flat, 1-protrudes).
    Corners are always flat to keep continuity

    Parameters
    size: integer, number of pixels in length/width of piece
    empty: boolean, whether piece is empty or not
    buildingConstraints: dictionary, any edge contraints from neighboring pieces
    """
    self.empty = empty
    self.pieceSize = size
    self.pieceInfo = []
    self.solvedOrientation = []
    self.leftConstraints = {}
    self.topConstraints = {}
    self.rightConstraints = {}
    self.bottomConstraints = {}
    flatSide = [[],[],[],[]]
    bumpList = [-1, 1]
    if empty == True:
      for info in range(size):
        line = []
        for element in range(size):
          line.append("-")
        self.pieceInfo.append(line)
    else:
      for info in range(size):
        line = []
        for element in range(size):
          constrain = buildingConstraints.get(str(info) + "," + str(element), 3)
          if constrain == 3:
            if element != 1 and info != 1 and element != size - 2 and info != size - 2:
              if info == 0 or info == size - 1:
                if element != 0 and element != size - 1 and element != 1 and element != size - 2:
                  if element == size - 3:
                    if info == 0:
                      if 1 not in flatSide[0] and -1 not in flatSide[0]:
                        number = bumpList[random.randrange(2)]
                      else:
                        number = random.randrange(-1, 2)
                    else:
                      if 1 not in flatSide[2] and -1 not in flatSide[2]:
                        number = bumpList[random.randrange(2)]
                      else:
                        number = random.randrange(-1, 2)
                  else:
                    number = random.randrange(-1, 2)
                  line.append(number)
                  if info == 0:
                    flatSide[0].append(number)
                  else:
                    flatSide[2].append(number)
                  if info == 0:
                    self.topConstraints[str(size - 1 - info) + "," + str(element)] = 0 - number
                  else:
                    self.bottomConstraints[str(size - 1 - info) + "," + str(element)] = 0 - number
                else:
                  line.append(0)
              elif element == 0 or element == size - 1:
                if info == size - 3:
                  if element == 0:
                    if 1 not in flatSide[3] and -1 not in flatSide[0]:
                      number = bumpList[random.randrange(2)]
                    else:
                      number = random.randrange(-1, 2)
                  else:
                    if 1 not in flatSide[1] and -1 not in flatSide[2]:
                      number = bumpList[random.randrange(2)]
                    else:
                      number = random.randrange(-1, 2)
                else:
                  number = random.randrange(-1, 2)
                line.append(number)
                if element == 0:
                  flatSide[3].append(number)
                else:
                  flatSide[1].append(number)
                if element == 0:
                  self.leftConstraints[str(info) + "," + str(size - 1 - element)] = 0 - number
                else:
                  self.rightConstraints[str(info) + "," + str(size - 1 - element)] = 0 - number
              else:
                line.append(0)
            else:
              line.append(0)
          else:
            line.append(constrain)
            if info == 0:
              self.topConstraints[str(size - 1 - info) + "," + str(element)] = 0 - constrain
            elif info == size - 1:
              self.bottomConstraints[str(size - 1 - info) + "," + str(element)] = 0 - constrain
            elif element == 0:
              self.leftConstraints[str(info) + "," + str(size - 1 - element)] = 0 - constrain
            else:
              self.rightConstraints[str(info) + "," + str(size - 1 - element)] = 0 - constrain
        self.pieceInfo.append(line)
    self.solvedOrientation = self.pieceInfo

  def displayPiece(self, path):
    """
    Saves single piece of puzzle as a png

    Parameters
    path: string, path to output png
    """
    outFile = path
    out = Image.new("RGB", (self.pieceSize + 2, self.pieceSize + 2))
    for pixelLine in range(self.pieceSize + 2):
      for pixel in range(self.pieceSize + 2):
        out.putpixel((pixel, pixelLine), (255, 255, 255))
    for pixelLine in range(self.pieceSize):
      for pixel in range(self.pieceSize):
        if self.pieceInfo[pixelLine][pixel] == -1:
          out.putpixel((pixel + 1, pixelLine + 1), (255, 255, 255))
        elif self.pieceInfo[pixelLine][pixel] == 1:
          if pixel == 0:
            out.putpixel((pixel, pixelLine + 1), (63, 116, 191))
          elif pixel == self.pieceSize - 1:
            out.putpixel((pixel + 2, pixelLine + 1), (63, 116, 191))
          elif pixelLine == 0:
            out.putpixel((pixel + 1, pixelLine), (63, 116, 191))
          elif pixelLine == self.pieceSize - 1:
            out.putpixel((pixel + 1, pixelLine + 2), (63, 116, 191))
          out.putpixel((pixel + 1, pixelLine + 1), (63, 116, 191))
        else:
          out.putpixel((pixel + 1, pixelLine + 1), (63, 116, 191))
    out.save(outFile)

  def determineEdgeIndex(self):
    """
    Calculates edge indices by summing values along each edge, stored as list of integers
    """
    self.edgeIndex = []
    self.edges = [[], [], [], []]
    if self.empty == True:
      pass
    else:
      top = 0
      bottom = 0
      left = 0
      right = 0
      for row in range(len(self.pieceInfo)):
        for column in range(len(self.pieceInfo[row])):
          if row == 0:
            top += self.pieceInfo[row][column]
            self.edges[0].append(self.pieceInfo[row][column])
          if row == self.pieceSize - 1:
            bottom += self.pieceInfo[row][column]
            self.edges[2].append(self.pieceInfo[row][column])
          if column == 0:
            left += self.pieceInfo[row][column]
            self.edges[3].append(self.pieceInfo[row][column])
          if column == self.pieceSize - 1:
            right += self.pieceInfo[row][column]
            self.edges[1].append(self.pieceInfo[row][column])
      self.edgeIndex.append(top)
      self.edgeIndex.append(right)
      self.edgeIndex.append(bottom)
      self.edgeIndex.append(left)

  def rotatePiece(self):
    """
    Rotates piece by 90 degrees clockwise, resets edge indices
    """
    rotated = []
    for row in range(self.pieceSize):
      line = []
      for column in range(self.pieceSize):
        line.append(self.pieceInfo[self.pieceSize - 1 - column][row])
      rotated.append(line)
    self.pieceInfo = rotated
    self.determineEdgeIndex()