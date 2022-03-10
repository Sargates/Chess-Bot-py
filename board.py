from sqlite3 import enable_shared_cache
import pygame, os
from pieces.move   import *
from pieces.piece import Piece
from pieces.king   import King
from pieces.pawn   import Pawn
from pieces.bishop import Bishop
from pieces.knight import Knight
from pieces.rook   import Rook
from pieces.queen  import Queen
from fen import Fen

WIDTH = HEIGHT = 768
WINDOWSIZE = (WIDTH, HEIGHT)
SQ_SIZE = ((256 - 80)/8) * (WIDTH/256)
OFFSET = 40 * (WIDTH/256)
PIECE_OFFSET = (10/11) * SQ_SIZE / 2

class Board:

	
	idToIndex = {
		'bB': 0,
		'bK': 1,
		'bN': 2,
		'bp': 3,
		'bQ': 4,
		'bR': 5,
		'wB': 6,
		'wK': 7,
		'wN': 8,
		'wp': 9,
		'wQ': 10,
		'wR': 11
	}

	ranksToRows = {'1': 7, '2': 6, '3': 5, '4': 4,
				   '5': 3, '6': 2, '7': 1, '8': 0}
	rowsToRanks = {v: k for k, v in ranksToRows.items()}
	filesToCols = {'a': 0, 'b': 1, 'c': 2, 'd': 3,
				   'e': 4, 'f': 5, 'g': 6, 'h': 7}
	colsToFiles = {v: k for k, v in filesToCols.items()}
	highlightedSquares = {}
	selectedIndex = None

	checkMate = False
	matchDraw = False

	def loadImages(self):
		self.images = []

		for piece in ['bB', 'bK', 'bN', 'bp', 'bQ', 'bR', 'wB', 'wK', 'wN', 'wp', 'wQ', 'wR']:
			self.images.append(pygame.transform.scale(pygame.image.load(os.path.join(os.path.dirname(os.path.abspath(__file__)) + "/img/" + piece + '.png')), (int(SQ_SIZE * 10/11), int(SQ_SIZE * 10/11))))
		
		self.boardImage = pygame.transform.scale(pygame.image.load(os.path.join(os.path.dirname(os.path.abspath(__file__)) + "/img/board_alt.png")), (WIDTH, HEIGHT))


	def __init__(self, ):
		self.loadImages()

		self.fen = Fen("8/4npk1/5p1p/1Q5P/1p4P1/4r3/7q/3K1R2 w - - 1 49")

		self.board = self.fen.boardParse()

		self.moveFunctions = {
		'p': self.getPawnMoves, 
		'R': self.getRookMoves, 
		'N': self.getKnightMoves, 
		'B': self.getBishopMoves, 
		'Q': self.getQueenMoves, 
		'K': self.getKingMoves,
	}

	def reset(self, ):
		pass

	def refreshChecksandPins(self, ):
		pass

	def checkForEnPassant(self, ):
		pass

	def checkForCheckmate(self, ):
		pass

	def getKingPos(self):
		whitePos, blackPos = -1
		for row in range(len(self.board)):
			for col in range(len(row)):
				if self.board[col][row][1] == "K":
					if self.board[row][col][0] == "w":
						whitePos = (col, row)
						continue
					blackPos = (col, row)
		
		return (whitePos, blackPos)

	def getPieceMoves(self, i, j, directions, moveDepths):

		# inCheck, pins, checks, kingPos = king.getChecksandPins(board, king.getPos(board)) + (king.getPos(board),)
		piecePinned = False
		availableMoves = []

		# for x in range(len(pins)-1, -1, -1):
		# 	# print(pins[x])
		# 	# print(i, j)
		# 	if pins[x][0] == i and pins[x][1] == j:
		# 		piecePinned = True
		# 		pinDirection = (pins[x][2], pins[x][3])
		# 		# print("pin found")
		# 		# print(pins[x])
		# 		# pins.remove(pins[x])
		# 		pins.pop(x)
		# 		break


		# print(f"piecePinned = {piecePinned}")
		for direction in directions:
			# print(f"direction == pinDirection = {direction == pinDirection}")
			# if piecePinned and direction != pinDirection:
			# 	continue

			for depth in moveDepths:
				if not (0 <= i + direction[0] * depth < 8 and 0 <= j + direction[1] * depth < 8):
					break

				endX = direction[0] * depth
				endY = direction[1] * depth

				startPos = (i, j)
				endPos = (i + endX, j + endY)
				startSpace = self.getSpace(*startPos)
				endSpace = self.getSpace(*endPos)
				if endSpace == "--":
					availableMoves.append(Move(self, startSpace, endSpace, startPos, endPos))
					continue
				
				if endSpace[0] != startSpace[0]:
					availableMoves.append(Move(self, startSpace, endSpace, startPos, endPos))
					break
				
				# if attacking:
				# 	availableMoves.append(Move(self, (i, j), endPos))
				# 	break
				break
		
		return availableMoves

	def getPawnMoves(self, x, y):
		pass

	def getKnightMoves(self, x, y):
		directions = [(-2, 1), (-1, 2), (1, 2), (2, 1), (2, -1), (1, -2), (-1, -2), (-2, -1)]
		moveDepths = [1]

		return self.getPieceMoves(x, y, directions, moveDepths)

	def getBishopMoves(self, x, y):
		moveDepths = [x for x in range(1, 8)]
		directions = [(-1, -1), (1, -1), (-1, 1), (1, 1)]

		return self.getPieceMoves(x, y, directions, moveDepths)

	def getRookMoves(self, x, y):
		moveDepths = [x for x in range(1,8)]
		directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]

		return self.getPieceMoves(x, y, directions, moveDepths)

	def getQueenMoves(self, x, y):
		moveDepths = [x for x in range(1, 8)]
		directions = [(-1, 0), (0, 1), (1, 0), (0, -1), (-1, -1), (1, -1), (-1, 1), (1, 1)]

		return self.getPieceMoves(x, y, directions, moveDepths)

	def getKingMoves(self, i, j):
		moveDepths = [1]
		directions = [(-1, 0), (0, 1), (1, 0), (0, -1), (-1, -1), (1, -1), (-1, 1), (1, 1)]
		
		
		availableMoves = []

		for direction in directions:
			for depth in moveDepths:
				x = direction[0]
				y = direction[1]
				# if inCheck:
				# 	for check in checks:
				# 		# print(check, direction)
				# 		if not (check[2] == -x and check[3] == -y):
				# 			break
				# 	else:
				# 		continue

				startPos = (i, y)
				startSpace = self.getSpace(*startPos)
				endPos = (i+x, j+y)
				endSpace = self.getSpace(*endPos)

				# if endPos in takenSquares:
				# 	continue

				if startSpace == "--":
					availableMoves.append(Move(self, startSpace, endSpace, startPos, endPos))
					continue
				
				if endSpace[0] != startSpace[0]:
					availableMoves.append(Move(self, startSpace, endSpace, startPos, endPos))
				break

		self.fen.refreshCastling(self)
		castle = self.fen.castling

		
		castleToInterval = {
			# change to support 2D indexing of b.board
			"q": [2, 3],
			"k": [5, 6],
			"Q": [58 ,59],
			"K": [61, 62]
		}

		if castle == "-":
			return availableMoves

		for char in castle:
			interval = castleToInterval[char]

			for square in interval:
				if self.getSpace(square) != "--":
					break
				moves = self.getEnemyMoves(self)
				if square in [move.endPos for move in moves]:
					break
			else:
				pos = self.castlingDict[char]
				# print(pos)
				if not position == pos[0]:
					continue
				availableMoves.append(Castle(self, self.getSpace(pos[1]), pos[0], pos[1]))


		return availableMoves


	def getAllMoves(self, ):
		pass

	def evalBoard(self, ):
		pass

	def makeMove(self, ):
		pass

	def undoMove(self, ):
		pass

	def selectionLogic(self, index :tuple[int]):
		if self.selectedIndex != None: # index is selected

			space = self.getSpace(*self.selectedIndex)
			if index == self.selectedIndex: # if selected index is clicked
				self.selectedIndex = None
				self.selectedMoves = []
				return

			tempMove = Move(self, space, self.getSpace(*index), self.selectedIndex, index)

			if tempMove in self.selectedMoves: # if index in in avialable moves
				move = self.selectedMoves[self.selectedMoves.index(tempMove)]
				self.moveHistory.append(move)
				if space.type == "p":
					self.fen.halfMoveCount = 0
				else:
					self.fen.halfMoveCount += 1

				self.fen.switchTurns(self.board)
				move.makeMove()
				self.checkForPromotion(move)
				self.checkForEnPassant(move)
				self.refreshChecksandPins()
				self.fen.refreshCastling(self)
				self.checkForCheckmate()

				self.selectedIndex = None
				self.selectedMoves = []
				self.futureMoves = []
				print(self.whiteInfo)
				print(self.blackInfo)
				print("\n", self.fen.getFenString(self.board), "\n")
				return

			if self.getSpace(*index) == "--": # selected index is not a piece
				self.selectedIndex = None
				self.selectedMoves = []
				return

			# guarenteed that clicked index is a different piece than is selected
			if self.getSpace(*index)[0] == self.fen.colorToMove:
				self.selectedIndex = index
				self.selectedMoves = self.moveFunctions[self.getSpace(*index)[1]](*index)
			else:
				self.selectedIndex = None
				self.selectedMoves = []

			# for move in self.selectedMoves:
			# 	print(move)
		if self.selectedIndex == None:
			self.selectedIndex = index
			self.selectedMoves = self.moveFunctions[self.getSpace(*index)[1]](*index)

	def getSpace(self, x, y):
		return self.board[y][x]

