from creator import *
import random


def edgeCheck(edge0, edge1):
  """
  Checks whether piece edges are compatible

  Parameters
  edge0: list, values along one edge of piece 0
  edge1: list, values along one edge of piece 1

  Return
  boolean, compatible or not
  """
  check = True
  for element in range(len(edge0)):
    if edge0[element] + edge1[element] != 0:
      check = False
      break
  return check

def coordinateFromRelativeDirection(coord, direction):
  """
  Determines coordinate of neighboring piece based on current piece and direction (up, down, left, right)

  Parameters
  coord: tuple, (x, y) position of piece
  direction: int, number between 0 and 3 inclusive corresponding to direction (0-up, 1-right, 2-down, 3-left)

  Return
  tuple, coordinate of neighbor
  """
  if direction == 0:
    return (coord[0], coord[1] + 1)
  if direction == 1:
    return (coord[0] + 1, coord[1])
  if direction == 2:
    return (coord[0], coord[1] - 1)
  if direction == 3:
    return (coord[0] - 1, coord[1])

def newSolvePuzzle(puzzle):
  """
  Solves a scrambled puzzle that has pieces with all unique edges

  Parameters
  puzzle: puzzle, custom class (see creator.py Puzzle)

  Return
  dictionary, all pieces with unscrambled coordinates
  """
  flatSide = []   # creates an example of a flat side for comparison, flat sides do not have connections
  for number in range(puzzle.pieceSize):  # loop based on piece size
    flatSide.append(0)
  pieceByLocation = {}  # a dictionary containing the locations of every placed piece
  startingPieceNotEmpty = False
  increment = 0
  while startingPieceNotEmpty == False:
    if puzzle.scrambledPieces[increment].empty == False:
      startingPieceNotEmpty = True
      pieceByLocation[(0,0)] = puzzle.scrambledPieces[increment]
    else:
      increment += 1
  previouslyUsedPieces = []   # a list of all previously placed pieces
  previouslyUsedPieces.append(puzzle.scrambledPieces[0])
  previouslyUsedCoordinates = []  # a list of all previously used coordinates, don't want to place two pieces on same coordinate
  numberOfEmpties = 0
  for emptyCheck in puzzle.scrambledPieces:
    if emptyCheck.empty == True:
      numberOfEmpties += 1
  nonUniqueCoordinates = []
  unplacedCoors = 0
  while len(pieceByLocation) < (puzzle.puzzleSize**2)-numberOfEmpties-unplacedCoors:
    coordinateCheck = False
    while coordinateCheck == False: # this loop ensures that randomly selected coordinate is not used more than once
      coordinateList = list(pieceByLocation.keys())
      coordinate = coordinateList[random.randrange(0,len(coordinateList))]
      if coordinate not in previouslyUsedCoordinates:
        previouslyUsedCoordinates.append(coordinate)
        coordinateCheck = True
    piece = pieceByLocation[coordinate] # pulls piece from dictionary based on location
    for edge in range(len(piece.edgeIndex)):  # tries to match every edge of the piece
      newPieceCoordinate = coordinateFromRelativeDirection(coord=coordinate, direction=edge)
      if piece.edges[edge] == flatSide:
        pass
      elif newPieceCoordinate in list(pieceByLocation.keys()):
        pass
      else:
        possibleConnectionsForEdge = []
        for testPiece in puzzle.scrambledPieces:
          if piece == testPiece:  # cannot connect piece to itself, no reason to check
            pass
          elif testPiece.empty == True:   # ignore empty pieces
            pass
          else:
            for e in range(len(testPiece.edgeIndex)):
              if testPiece in previouslyUsedPieces:
                pass
              elif piece.edgeIndex[edge] == -testPiece.edgeIndex[e]:  # checks edge index before rotating
                desiredEdge = (edge + 2) % 4  # uses index of edge in list to determine how to rotate
                rotations = desiredEdge - e
                if rotations < 0:
                  rotations = 4 + rotations
                returnRotations = 4 - rotations
                for rotate in range(rotations):
                  testPiece.rotatePiece()
                check = edgeCheck(edge0=piece.edges[edge], edge1=testPiece.edges[desiredEdge])
                if check == True:   # if it passes the edge check, add to possible connections
                  possibleConnectionsForEdge.append(testPiece)
                  break
                else:
                  for rotate in range(returnRotations): # rotates back to original position after fail
                    testPiece.rotatePiece()
        if len(possibleConnectionsForEdge) == 1:  # setting up for possibility of non-unique edges in future
          pieceByLocation[newPieceCoordinate] = possibleConnectionsForEdge[0]
          previouslyUsedPieces.append(possibleConnectionsForEdge[0])
        else:
          return {}, False
      unplacedCoors = 0
      for nUCoor in nonUniqueCoordinates:
        if nUCoor not in pieceByLocation:
          unplacedCoors += 1
  return pieceByLocation, True

def placeOnCanvas(pieces):
  """
  Creates puzzle from unscambled pieces

  Parameters
  pieces: dictionary

  Return
  puzzle, custom class (see creator.py Puzzle), solved puzzle
  """
  coordinates = list(pieces.keys())
  x = []
  for coord in coordinates:
    x.append(coord[0])
  y = []
  for coord in coordinates:
    y.append(coord[1])
  xMin = min(x)   # crude method for determining bounds of puzzle
  yMax = max(y)
  xRange = max(x)-min(x) + 1
  yRange = max(y)-min(y) + 1
  if xRange >= yRange:
    tRange = xRange
  else:
    tRange = yRange
  canvas = [] # creates a canvas with length and width equal to the largest dimension of the puzzle
  for row in range(tRange):
    line = []
    for column in range(tRange):
      line.append(JigsawPiece(size=pieceSize, empty=True))  # uses empty as default
    canvas.append(line)
  for c in coordinates:
    canvas[yMax - c[1]][c[0] - xMin] = pieces[c]  # replaces "-" with actual pieces by coordinate
  return Puzzle(pieceSize=canvas[0][0].pieceSize, puzzleSize=tRange, pieces=canvas, scramble=False)





pieceSize = 20
puzzleSize = 20
startingPuzzlePath = "starting_puzzle.png"
solvedPuzzlePath = "solved_puzzle.png"

p = Puzzle(pieceSize=pieceSize, puzzleSize=puzzleSize, nonSquare=True)
p.displaySolved(path=startingPuzzlePath)
print("Created Puzzle and Scrambled")
for ip in range(len(p.scrambledPieces)):
  p.scrambledPieces[ip].determineEdgeIndex()
print("Determined Edge Indices")
pieceByLocation, success = newSolvePuzzle(puzzle=p)
if success == True:
  print("Solved All Pieces")
  final = placeOnCanvas(pieces=pieceByLocation)
  final.displaySolved(path=solvedPuzzlePath, type="answer")
  print("Saved Puzzle To Path")
else:
  print("Failed To Solve: Puzzle Possesses Non-Unique Edges")