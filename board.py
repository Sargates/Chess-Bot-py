from re import A
import pygame, os
from move   import *
from fen import Fen
from PygameExtensions import *

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

	valueDict = {
		'p': 1, 
		'R': 5, 
		'N': 3, 
		'B': 3, 
		'Q': 9
	}

	ranksToRows = {'1': 7, '2': 6, '3': 5, '4': 4,
				   '5': 3, '6': 2, '7': 1, '8': 0}
	rowsToRanks = {v: k for k, v in ranksToRows.items()}
	filesToCols = {'a': 0, 'b': 1, 'c': 2, 'd': 3,
				   'e': 4, 'f': 5, 'g': 6, 'h': 7}
	colsToFiles = {v: k for k, v in filesToCols.items()}
	highlightedSquares = set()
	selectedIndex = None

	moveHistory = []
	moveFuture = []

	checkMate = False
	matchDraw = False

	def loadImages(self):
		self.images = []

		for piece in ['bB', 'bK', 'bN', 'bp', 'bQ', 'bR', 'wB', 'wK', 'wN', 'wp', 'wQ', 'wR']:
			self.images.append(pygame.transform.scale(pygame.image.load(os.path.join(os.path.dirname(os.path.abspath(__file__)) + "/img/" + piece + '.png')), (int(SQ_SIZE * 10/11), int(SQ_SIZE * 10/11))))
			
		
		self.boardImage = pygame.transform.scale(pygame.image.load(os.path.join(os.path.dirname(os.path.abspath(__file__)) + "/img/board_alt.png")), (WIDTH, HEIGHT))

	def __init__(self, ):
		self.loadImages()
		
		# self.fen = Fen("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
		# self.fen = Fen("r3k2r/p1ppqpb1/bn2pnp1/3PN3/1p2P3/2N2Q1p/PPPBBPPP/R3K2R w KQkq - 0 0")
		# self.fen = Fen("8/2p5/3p4/KP5r/1R3p1k/8/4P1P1/8 w - - 0 0")
		self.fen = Fen("r3k2r/Pppp1ppp/1b3nbN/nP6/BBP1P3/q4N2/Pp1P2PP/R2Q1RK1 w kq - 0 1")
		# self.fen = Fen("rnbq1k1r/pp1Pbppp/2p5/8/2B5/8/PPP1NnPP/RNBQK2R w KQ - 1 8")
		# self.fen = Fen("r4rk1/1pp1qppp/p1np1n2/2b1p1B1/2B1P1b1/P1NP1N2/1PP1QPPP/R4RK1 w - - 0 10")


		# self.fen = Fen("rnbqkbnr/pppppPpp/8/8/8/8/PPPPP1PP/RNBQKBNR w KQkq - 0 1")


		
		

		self.aiInProgress = False


		self.board = self.fen.boardParse()
		self.resetPublicBoard()
		

		self.moveFunctions = {
			'p': self.getPawnMoves, 
			'R': self.getRookMoves, 
			'N': self.getKnightMoves, 
			'B': self.getBishopMoves, 
			'Q': self.getQueenMoves, 
			'K': self.getKingMoves,
		}
		
		whitePos, blackPos = -1, -1
		for row in range(len(self.board)):
			for col in range(len(self.board[row])):
				if self.board[row][col][1] == "K":
					if self.board[row][col][0] == "w":
						self.whiteKingPos = (col, row)
						continue
					self.blackKingPos = (col, row)
				if whitePos != -1 and blackPos != -1:
					break				
			if whitePos != -1 and blackPos != -1:
				break


		self.kingMap = {
			"w": self.whiteKingPos,
			"b": self.blackKingPos
		}

		self.waitingOnPromotion = False

		self.selectedIndex = None
		self.selectedMoves = []


		self.rookPromotion 		= Box(pygame.Rect(688, 114, 60, 60), color=pygame.Color(0, 0, 0, 255), isDraggable=False)
		self.bishopPromotion 	= Box(pygame.Rect(688, 174, 60, 60), color=pygame.Color(0, 0, 0, 255), isDraggable=False)
		self.knightPromotion 	= Box(pygame.Rect(688, 234, 60, 60), color=pygame.Color(0, 0, 0, 255), isDraggable=False)
		self.queenPromotion 	= Box(pygame.Rect(688, 294, 60, 60), color=pygame.Color(0, 0, 0, 255), isDraggable=False)

		self.promotionDict = {
			'R': self.rookPromotion,
			'B': self.bishopPromotion,
			'N': self.knightPromotion,
			'Q': self.queenPromotion
		}

	def reset(self, ):
		pass

	def resetPublicBoard(self):
		self.publicBoard = [["" for x in range(8)]for x in range(8)]

		for i in range(8):
			for j in range(8):
				self.publicBoard[i][j] = self.board[i][j]

	def checkForPromotion(self, move :Move):
		# print("big cum")
		if type(move) == Promotion:
			# print("big cum 2")
			self.waitingOnPromotion = True

			self.rookPromotion.image = self.images[self.idToIndex[move.pieceMoved[0] + "R"]]
			self.bishopPromotion.image = self.images[self.idToIndex[move.pieceMoved[0] + "B"]]
			self.knightPromotion.image = self.images[self.idToIndex[move.pieceMoved[0] + "N"]]
			self.queenPromotion.image = self.images[self.idToIndex[move.pieceMoved[0] + "Q"]]

	def checkForEnPassant(self, move :Move):
		if move.pieceMoved[1] == "p" and abs(move.endPos[1] - move.startPos[1]) == 2 and move.startPos[1]:
			self.fen.setEnPassant(move.endPos)
			return
		
		self.fen.setEnPassant(None)

	def checkCastling(self, move :Move):
		if move.pieceMoved[1] == "K":
			if move.pieceMoved[0] == "w":
				if "K" in self.fen.castling:
					self.fen.castling.pop(self.fen.castling.index("K"))
				if "Q" in self.fen.castling:
					self.fen.castling.pop(self.fen.castling.index("Q"))
			if move.pieceMoved[0] == "b":
				if "k" in self.fen.castling:
					self.fen.castling.pop(self.fen.castling.index("k"))
				if "q" in self.fen.castling:
					self.fen.castling.pop(self.fen.castling.index("q"))
		
		if move.pieceMoved[1] == "R":
			if move.startPos == (7,7):
				if "K" in self.fen.castling:
					self.fen.castling.pop(self.fen.castling.index("K"))
			if move.startPos == (0,7):
				if "Q" in self.fen.castling:
					self.fen.castling.pop(self.fen.castling.index("Q"))
			if move.startPos == (7,0):
				if "k" in self.fen.castling:
					self.fen.castling.pop(self.fen.castling.index("k"))
			if move.startPos == (0,0):
				if "q" in self.fen.castling:
					self.fen.castling.pop(self.fen.castling.index("q"))
						

		self.fen.refreshCastling()
	
	def removeInvalidMoves(self, moves :list[Move], kingInfo):
		inCheck, pins, checks, kingPos = kingInfo
		if not inCheck:
			return

		requiredSquares = []
		if len(checks) == 0:
			return

		if len(checks) == 1:
			check = checks[0]
			# if crashing come back here
			# not checking if move is valid
			direction = (check[2], check[3])
			endPos = (check[0], check[1])
			i = 1


			while (kingPos[0] + direction[0] * i, kingPos[1] + direction[1] * i) != (endPos[0] + direction[0], endPos[1] + direction[1]):
				if self.getSpace(*endPos)[1] == "N":
					requiredSquares.append(endPos)
					break
				requiredSquares.append((kingPos[0] + direction[0] * i, kingPos[1] + direction[1] * i))
				i += 1
			
			# print(requiredSquares)
			# print([str(move) for move in moves])
			for i in range(len(moves)-1, -1, -1):
				move = moves[i]

				# print(move)
				# print(move.endPos in requiredSquares)
				# print((move.pieceMoved.type == "K" and move.endPos in [m.endPos for m in self.getEnemyMoves(board)]))
				if not move.endPos in requiredSquares:
					# print("\t", move)
					moves.pop(i)
					continue
		else:
			moves = []

	def getPieceMoves(self, i, j, directions, moveDepths):
		color = self.getSpace(i, j)[0]
		pos = self.kingMap[color]

		inCheck, pins, checks = self.isSquareCovered(*pos, color)
		piecePinned = False
		availableMoves = []


		for x in range(len(pins)-1, -1, -1):
			# print("STARTING ITER")
			# print(pins[x])
			# print(i, j)
			if pins[x][0] == i and pins[x][1] == j:
				piecePinned = True
				pinDirection = (pins[x][2], pins[x][3])
				# print("pin found")
				# print(pins[x])
				pins.pop(x)
				break

		# print(f"piecePinned = {piecePinned}")
		for direction in directions:
			if piecePinned and not (direction == pinDirection or direction == (-pinDirection[0], -pinDirection[1])):
				# print(f"direction == pinDirection = {direction == pinDirection}")
				continue

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
		
		self.removeInvalidMoves(availableMoves, (inCheck, pins, checks, pos))
		
		return availableMoves
	def getPawnMoves(self, i, j):
		space = self.getSpace(i, j)
		color = space[0]
		kingPos = self.kingMap[color]

		inCheck, pins, checks = self.isSquareCovered(*kingPos, color)
		piecePinned = False
		availableMoves = []


		for x in range(len(pins)-1, -1, -1):
			# print("STARTING ITER")
			# print(pins[x])
			# print(i, j)
			if pins[x][0] == i and pins[x][1] == j:
				piecePinned = True
				pinDirection = (pins[x][2], pins[x][3])
				# print("pin found")
				# print(pins[x])
				pins.pop(x)
				break
		
		direction = (0, 1) if color == "b" else (0, -1)

		forwardOne = direction
		forwardTwo = (direction[0], direction[1] * 2)
		forwardQ = (direction[0]-1, direction[1])
		forwardK = (direction[0]+1, direction[1])

		enPassantIndex = -1
		

		endPos = (i + forwardOne[0], j + forwardOne[1])
		if 0 <= endPos[0] < 8 and 0 <= endPos[1] < 8 and self.getSpace(i + forwardOne[0], j + forwardOne[1]) == "--" and not (piecePinned and forwardOne != pinDirection):
			endSpace = self.getSpace(*endPos)
			possiblePromotion = Move(self, space, endSpace, (i, j), endPos)
			if endPos[1] == int(3.5 + (3.5 * forwardOne[1])):
				availableMoves.append(Promotion(possiblePromotion, "R"))
				availableMoves.append(Promotion(possiblePromotion, "B"))
				availableMoves.append(Promotion(possiblePromotion, "N"))
				availableMoves.append(Promotion(possiblePromotion, "Q"))
			else:
				availableMoves.append(possiblePromotion)



		endPos = (i + forwardTwo[0], j + forwardTwo[1])
		if 0 <= endPos[0] < 8 and 0 <= endPos[1] < 8 and self.getSpace(i + forwardOne[0], j + forwardOne[1]) == "--" and self.getSpace(i + forwardTwo[0], j + forwardTwo[1]) == "--" and not (piecePinned and forwardOne != pinDirection) and j == int(direction[1] * (-2.5) + 3.5):
			endSpace = self.getSpace(*endPos)
			availableMoves.append(Move(self, space, endSpace, (i, j), endPos))

			
			
		endPos = (i + forwardQ[0], j + forwardQ[1])
		if not (piecePinned and forwardQ != pinDirection) and 0 <= endPos[0] < 8 and 0 <= endPos[1] < 8:
			endSpace = self.getSpace(*endPos)
			if endSpace != "--" and endSpace[0] != color:
				possiblePromotion = Move(self, space, endSpace, (i, j), endPos)
				if endPos[1] == int(3.5 + (3.5 * forwardOne[1])):
					availableMoves.append(Promotion(possiblePromotion, "R"))
					availableMoves.append(Promotion(possiblePromotion, "B"))
					availableMoves.append(Promotion(possiblePromotion, "N"))
					availableMoves.append(Promotion(possiblePromotion, "Q"))
				else:
					availableMoves.append(possiblePromotion)
			
			if (endPos[0], endPos[1] - forwardQ[1]) == self.fen.getEnPassantPos():
				endSpace = self.getSpace(endPos[0], endPos[1] - forwardQ[1])
				availableMoves.append(EnPassant(self, space, endSpace, (i, j), endPos))
				enPassantIndex = len(availableMoves)-1

		endPos = (i + forwardK[0], j + forwardK[1])
		if not (piecePinned and forwardK != pinDirection) and 0 <= endPos[0] < 8 and 0 <= endPos[1] < 8:
			endSpace = self.getSpace(*endPos)
			if endSpace != "--" and endSpace[0] != color:
				possiblePromotion = Move(self, space, endSpace, (i, j), endPos)
				if endPos[1] == int(3.5 + (3.5 * forwardOne[1])):
					availableMoves.append(Promotion(possiblePromotion, "R"))
					availableMoves.append(Promotion(possiblePromotion, "B"))
					availableMoves.append(Promotion(possiblePromotion, "N"))
					availableMoves.append(Promotion(possiblePromotion, "Q"))
				else:
					availableMoves.append(possiblePromotion)
			
			if (endPos[0], endPos[1] - forwardK[1]) == self.fen.getEnPassantPos():
				endSpace = self.getSpace(endPos[0], endPos[1] - forwardK[1])
				availableMoves.append(EnPassant(self, space, endSpace, (i, j), endPos))
				enPassantIndex = len(availableMoves)-1
		
		# for i in range(len(availableMoves)-1, -1, -1):
		# 	testedMove = availableMoves[i]

		# 	self.makeMove(testedMove)

		# 	if self.isSquareCovered(*self.kingMap[color], color)[0]:
		# 		availableMoves.pop(i)
			
		# 	self.undoMove()
		self.removeInvalidMoves(availableMoves, self.isSquareCovered(*self.kingMap[color], color) + (self.kingMap[color],))

		# test enPassantMove
		if enPassantIndex != -1:
			enPassantMove = availableMoves[enPassantIndex]

			enPassantMove.makeMove()

			if self.isSquareCovered(*self.kingMap[color], color)[0]:
				availableMoves.pop(enPassantIndex)
			
			enPassantMove.undo()
		
		return availableMoves
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
	
	# def isMoveValid(self, move :Move):
	# 	move.makeMove()
	# 	# self.whiteKing
	# 	inCheck = 

	def isSquareCovered(self, x1, y1, color) -> tuple[bool, tuple, tuple]: 
		pins = []
		checks = []
		inCheck = False

		directions = ((0, -1), (1, 0), (0, 1), (-1, 0), (1, 1), (-1, 1), (-1, -1), (1, -1))

		for j in range(len(directions)):
			dir = directions[j]
			possiblePin = ()
			for i in range(1, 8):
				testedPos = (x1 + dir[0]*i, y1 + dir[1]*i)
				if not (0 <= testedPos[0] < 8 and 0 <= testedPos[1] < 8):
					break

				endSpace = self.getSpace(*testedPos)

				if endSpace == "--":
					continue

				if endSpace[0] == color and endSpace[1] != 'K':
					if possiblePin == ():
						possiblePin = (testedPos[0], testedPos[1], dir[0], dir[1])
						# print("Possible Pin")
						# print(possiblePin)
					else:
						break
				elif endSpace[0] != color:
					type = endSpace[1]
					# 5 possibilities here in this complex conditional
					# 1. orthoganally away from king and piece is rook
					# 2. diagonally away from king and piece is bishop
					# 3. 1 square away diagonally from king and piece is a pawn
					# 4. any direction and piece is a queen
					# 5. anydirection 1 square away and piece is a king( this is necessary to prevent a king move to a square controlled by another king)
					if (0 <= j <= 3 and type == 'R') or \
							(4 <= j <= 7 and type == 'B') or \
							(i == 1 and type == 'p' and ((color == 'w' and 6 <= j <= 7) or \
							(color == 'b' and 4 <= j <= 5))) or \
							(type == 'Q') or (i == 1 and type == 'K'):
						if possiblePin == (): # no piece blocking, so check the king
							inCheck = True
							checks.append((testedPos[0], testedPos[1], dir[0], dir[1]))
							# print("Check found")
							# print((testedPos[0], testedPos[1], dir[0], dir[1]))

							break
						else: # pinned piece blocking check
							pins.append(possiblePin)
							# print("Pin found")
							# print(possiblePin)
							break
					else:
						break

		knightMoves = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2,-1), (2, 1))
		for m in knightMoves:
			testedPos = (x1 + m[0], y1 + m[1])
			if not (0 <= testedPos[0] < 8 and 0 <= testedPos[1] < 8):
				continue

			endPiece = self.getSpace(*testedPos)
			if endPiece == "--":
				continue
			if endPiece[0] != color and endPiece[1] == "N":
				inCheck = True
				checks.append((testedPos[0], testedPos[1], m[0], m[1]))
					
		# print("End of pin check")

		return (inCheck, pins, checks)

	def getKingMoves(self, i, j):
		moveDepths = [1]
		directions = [(-1, 0), (0, 1), (1, 0), (0, -1), (-1, -1), (1, -1), (-1, 1), (1, 1)]
		
		
		availableMoves = []

		startPos = (i, j)
		startSpace = self.getSpace(*startPos)
		color = startSpace[0]

		for direction in directions:
			x = direction[0]
			y = direction[1]

			endPos = (i+x, j+y)
			# print(endPos)

			if not (0 <= endPos[0] < 8 and 0 <= endPos[1] < 8):
				continue
			endSpace = self.getSpace(*endPos)

			squareCovered, throw1, throw2 = self.isSquareCovered(*endPos, color)
			# print(squareCovered, throw1, throw2)
			if squareCovered:
				continue

			if startSpace == "--":
				availableMoves.append(Move(self, startSpace, endSpace, startPos, endPos))
				continue
			
			if endSpace[0] != startSpace[0]:
				availableMoves.append(Move(self, startSpace, endSpace, startPos, endPos))
			# break

		self.fen.refreshCastling()
		castle = self.fen.castling

		
		unCheckableSpaces = {
			"q": [(2,0), (3,0)],
			"k": [(5,0), (6,0)],
			"Q": [(2,7) ,(3,7)],
			"K": [(5,7), (6,7)]
		}

		clearSpaces = {
			"q": [(1, 0), (2,0), (3,0)],
			"k": [(5,0), (6,0)],
			"Q": [(1, 7), (2,7) ,(3,7)],
			"K": [(5,7), (6,7)]
		}

		rookKingPos = {
			"q": ((4,0), (0,0)),
			"k": ((4,0), (7,0)),
			"Q": ((4,7), (0,7)),
			"K": ((4,7), (7,7))
		}

		if self.isSquareCovered(i, j, color)[0]:
			return availableMoves

		if castle == ["-"]:
			return availableMoves

		if color == "b":
			if not self.isSquareCovered(*unCheckableSpaces['q'][0], color)[0] and not self.isSquareCovered(*unCheckableSpaces['q'][1], color)[0] and \
				self.getSpace(*clearSpaces['q'][0]) == "--" and self.getSpace(*clearSpaces['q'][1]) == "--" and self.getSpace(*clearSpaces['q'][2]) == "--" and \
				self.getSpace(*rookKingPos['q'][0])[1] == "K" and self.getSpace(*rookKingPos['q'][1])[1] == "R" and ('q' in self.fen.castling):
					availableMoves.append(Castle(self, startSpace, self.getSpace(*rookKingPos['q'][1]), rookKingPos['q'][0], rookKingPos['q'][1]))

			if not self.isSquareCovered(*unCheckableSpaces['k'][0], color)[0] and not self.isSquareCovered(*unCheckableSpaces['k'][1], color)[0] and \
				self.getSpace(*clearSpaces['k'][0]) == "--" and self.getSpace(*clearSpaces['k'][1]) == "--" and \
				self.getSpace(*rookKingPos['k'][0])[1] == "K" and self.getSpace(*rookKingPos['k'][1])[1] == "R" and ('k' in self.fen.castling):
					availableMoves.append(Castle(self, startSpace, self.getSpace(*rookKingPos['k'][1]), rookKingPos['k'][0], rookKingPos['k'][1]))

		if color == "w":
			if not self.isSquareCovered(*unCheckableSpaces['Q'][0], color)[0] and not self.isSquareCovered(*unCheckableSpaces['Q'][1], color)[0] and \
				self.getSpace(*clearSpaces['Q'][0]) == "--" and self.getSpace(*clearSpaces['Q'][1]) == "--" and self.getSpace(*clearSpaces['Q'][2]) == "--" and \
				self.getSpace(*rookKingPos['Q'][0])[1] == "K" and self.getSpace(*rookKingPos['Q'][1])[1] == "R" and ('Q' in self.fen.castling):
					availableMoves.append(Castle(self, startSpace, self.getSpace(*rookKingPos['Q'][1]), rookKingPos['Q'][0], rookKingPos['Q'][1]))

			if not self.isSquareCovered(*unCheckableSpaces['K'][0], color)[0] and not self.isSquareCovered(*unCheckableSpaces['K'][1], color)[0] and \
				self.getSpace(*clearSpaces['K'][0]) == "--" and self.getSpace(*clearSpaces['K'][1]) == "--" and \
				self.getSpace(*rookKingPos['K'][0])[1] == "K" and self.getSpace(*rookKingPos['K'][1])[1] == "R" and ('K' in self.fen.castling):
					availableMoves.append(Castle(self, startSpace, self.getSpace(*rookKingPos['K'][1]), rookKingPos['K'][0], rookKingPos['K'][1]))	




		return availableMoves

	def getAllMoves(self) -> list[Move]:
		color = self.fen.colorToMove
		totalMoves = []

		for i in range(8):
			for j in range(8):
				if self.board[i][j][0] == color:

					totalMoves.extend(self.moveFunctions[self.board[i][j][1]](j, i))
		
		# kingInfo = self.isSquareCovered(*kingPos, color) + (kingPos,)
		# self.removeInvalidMoves(totalMoves, kingInfo)
		
		return totalMoves


	def evalBoard(self):
		total = 0
		perspective = 1 if self.fen.colorToMove == "w" else -1

		for i in range(8):
			for j in range(8):
				if self.board[i][j] == "--":
					continue

				if self.board[i][j][1] == "K":
					continue
				
				total += self.valueDict[self.board[i][j][1]]
		
		return total * perspective				

	def makeMove(self, move :Move):
		self.fen.switchTurns(self.board)
		move.makeMove()
		if move.pieceMoved[1] == "K":
			self.kingMap[move.pieceMoved[0]] = move.endPos
		self.checkForEnPassant(move)
		self.checkCastling(move)
		# self.checkForCheckmate()
		self.moveHistory.append(move)

	def undoMove(self):
		move = self.moveHistory.pop(-1)
		move.undo()

		if move.pieceMoved[1] == "K":
			self.kingMap[move.pieceMoved[0]] = move.startPos
		if type(move) == Promotion:
			self.waitingOnPromotion = False

			RenderPipeline.removeAsset(self.rookPromotion)
			RenderPipeline.removeAsset(self.bishopPromotion)
			RenderPipeline.removeAsset(self.knightPromotion)
			RenderPipeline.removeAsset(self.queenPromotion)

			self.rookPromotion.setAction	(None)
			self.bishopPromotion.setAction	(None)
			self.knightPromotion.setAction	(None)
			self.queenPromotion.setAction	(None)

		self.checkForEnPassant(move)
		self.fen.refreshCastling()
		# self.checkForCheckmate()
		self.moveFuture.append(move)
		self.fen.undo()

	def selectionLogic(self, index :tuple[int]):
		if self.selectedIndex != None: # index is selected

			space = self.getSpace(*self.selectedIndex)
			if index == self.selectedIndex: # if selected index is clicked
				self.selectedIndex = None
				self.selectedMoves = []
				return

			tempMove = Move(self, space, self.getSpace(*index), self.selectedIndex, index)
			tempMoveInSelectedMoves = False

			# for selectedMove in self.selectedMoves:
			# 	if tempMove == selectedMove:
			# 		tempMoveInSelectedMoves = True
			# 	if type(selectedMove) == Promotion:
			# 		self.waitingOnPromotion = True
			# 		# return

			# if self.waitingOnPromotion:
			# 	RenderPipeline.addAsset(self.rookPromotion)
			# 	RenderPipeline.addAsset(self.bishopPromotion)
			# 	RenderPipeline.addAsset(self.knightPromotion)
			# 	RenderPipeline.addAsset(self.queenPromotion)
			# 	return
			
			if tempMove in self.selectedMoves: # if index in in avialable moves
				moveIndex = self.selectedMoves.index(tempMove)
				move = self.selectedMoves[moveIndex]
				if space[1] == "p":
					self.fen.halfMoveCount = 0
				else:
					self.fen.halfMoveCount += 1

				if type(move) == Promotion:
					self.waitingOnPromotion = True

					self.rookPromotion.setAction(self.makeMove)
					self.rookPromotion.setArgs((self.selectedMoves[moveIndex+0], ))
					self.rookPromotion.setImage(self.images[self.idToIndex[space[0] + "R"]])

					self.bishopPromotion.setAction(self.makeMove)
					self.bishopPromotion.setArgs((self.selectedMoves[moveIndex+1], ))
					self.bishopPromotion.setImage(self.images[self.idToIndex[space[0] + "B"]])

					self.knightPromotion.setAction(self.makeMove)
					self.knightPromotion.setArgs((self.selectedMoves[moveIndex+2], ))
					self.knightPromotion.setImage(self.images[self.idToIndex[space[0] + "N"]])

					self.queenPromotion.setAction(self.makeMove)
					self.queenPromotion.setArgs((self.selectedMoves[moveIndex+3], ))
					self.queenPromotion.setImage(self.images[self.idToIndex[space[0] + "Q"]])

					RenderPipeline.addAsset(self.rookPromotion)
					RenderPipeline.addAsset(self.bishopPromotion)
					RenderPipeline.addAsset(self.knightPromotion)
					RenderPipeline.addAsset(self.queenPromotion)



				else:
					self.makeMove(move)
				self.fen.future = []

				# for move in self.selectedMoves:
				# 	print(move)

				self.selectedIndex = None
				self.selectedMoves = []

				self.moveFuture = []
				self.resetPublicBoard()
				# print(self.fen.getFenString(self.board), "\n")

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
			if self.getSpace(*index) != "--":
				self.selectedIndex = index
				self.selectedMoves = self.moveFunctions[self.getSpace(*index)[1]](*index)

	def getSpace(self, x, y):
		return self.board[y][x]

