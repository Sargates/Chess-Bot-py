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
		
		self.fen = Fen("r3k2r/Pppp1ppp/1b3nbN/nP6/BBP1P3/q4N2/Pp1P2PP/R2Q1RK1 w kq - 0 1")

		self.board = self.fen.boardParse()
		self.resetPublicBoard()
		

		self.pieceMoveFunctions = {
			'p': self.getPawnMoves, 
			'R': self.getRookMoves, 
			'N': self.getKnightMoves, 
			'B': self.getBishopMoves, 
			'Q': self.getQueenMoves, 
			'K': self.getKingMoves,
		}

		self.pieceLocationSet = set()

		self.kingMap = {
			"w": -1,
			"b": -1
		}

		for i in range(64):
			if self.board[i] == "--":
				continue

			self.pieceLocationSet.add((self.board[i], i))
			if self.board[i][1] == "K":
				self.kingMap[self.board[i][0]] = i


		
		temp = {
			0:	 -8,
			1:	  8,
			2:	 -1,
			3:	  1,
			4:	 -9,
			5:	  9,
			6:	 -7,
			7:	  7,

			8:	 15,
			9:	 17,
			10:	-17,
			11:	-15,
			12:	 10,
			13:	 -6,
			14:	  6,
			15:	-10,
		}

		self.directionsToSquaresFromEdge = {v: k for k, v in temp.items()}

		self.numSquaresToEdge = {x: [0 for x in range(16)] for x in range(64)}

		for squareIndex in range(len(self.numSquaresToEdge)):
			y = squareIndex // 8
			x = squareIndex % 8

			north = y
			south = 7 - y
			west = x
			east = 7 - x

			# QUEEN SLIDING MOVES
			self.numSquaresToEdge[squareIndex][0] = north
			self.numSquaresToEdge[squareIndex][1] = south
			self.numSquaresToEdge[squareIndex][2] = west
			self.numSquaresToEdge[squareIndex][3] = east
			self.numSquaresToEdge[squareIndex][4] = min(north, west)
			self.numSquaresToEdge[squareIndex][5] = min(south, east)
			self.numSquaresToEdge[squareIndex][6] = min(north, east)
			self.numSquaresToEdge[squareIndex][7] = min(south, west)

			
			for knightIndex in range(8, 16):
				knightJumpSquare = squareIndex + temp[knightIndex]

				knightSquareY = knightJumpSquare // 8
				knightSquareX = knightJumpSquare % 8
				maxCoordMoveDst = max(abs(x - knightSquareX), abs(y - knightSquareY))

				if (maxCoordMoveDst == 2):
					self.numSquaresToEdge[squareIndex][knightIndex] = 1

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
		self.publicBoard = ["" for x in range(64)]

		for i in range(64):
			self.publicBoard[i] = self.board[i]

	def checkForPromotion(self, move :Move):
		if type(move) == Promotion:
			self.waitingOnPromotion = True

			self.rookPromotion.image = self.images[self.idToIndex[move.pieceMoved[0] + "R"]]
			self.bishopPromotion.image = self.images[self.idToIndex[move.pieceMoved[0] + "B"]]
			self.knightPromotion.image = self.images[self.idToIndex[move.pieceMoved[0] + "N"]]
			self.queenPromotion.image = self.images[self.idToIndex[move.pieceMoved[0] + "Q"]]

	def checkForEnPassant(self, move :Move):
		if move.pieceMoved[1] == "p" and abs(move.endPos - move.startPos) == 16:
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
			direction = check[1]
			endPos = check[0]
			i = 1


			while (kingPos + direction * i) != (endPos + direction):
				if self.getSpace(endPos)[1] == "N":
					requiredSquares.append(endPos)
					break
				requiredSquares.append(kingPos + direction * i)
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

	def getPawnMoves(self, pos):
		space = self.getSpace(pos)
		color = space[0]
		# for piece in self.pieceLocationSet:
		# 	if piece[0] == color + "K":
		# 		kingPos = piece[1]
		kingPos = self.kingMap[color]

		inCheck, pins, checks = self.isSquareCovered(kingPos, color)
		piecePinned = False
		availableMoves = []

		# print(inCheck, pins, checks)


		for x in range(len(pins)-1, -1, -1):
			# print("STARTING ITER")
			# print(pins[x])
			# print(i, j)
			if pins[x][0] == pos:
				piecePinned = True
				pinDirection = (pins[x][1])
				# print("pin found")
				# print(pins[x])
				pins.pop(x)
				break
		
		
		direction = 8 if color == "b" else -8

		forwardOne = direction
		forwardTwo = direction * 2
		forwardQ = direction-1
		forwardK = direction+1

		enPassantIndex = -1
		

		endPos = pos + forwardOne
		if self.isMoveInbounds(pos, forwardOne) and self.getSpace(endPos) == "--" and not (piecePinned and forwardOne != pinDirection):
			endSpace = self.getSpace(endPos)
			possiblePromotion = Move(self, space, endSpace, pos, endPos)
			if (endPos//8) == int(3.5 + (3.5 * (forwardOne // 8))):
				availableMoves.append(Promotion(possiblePromotion, "R"))
				availableMoves.append(Promotion(possiblePromotion, "B"))
				availableMoves.append(Promotion(possiblePromotion, "N"))
				availableMoves.append(Promotion(possiblePromotion, "Q"))
			else:
				availableMoves.append(possiblePromotion)



		endPos = pos + forwardTwo
		if (pos//8) == (int((direction//8) * (-2.5) + 3.5)) and self.getSpace(pos + forwardOne) == "--" and self.getSpace(endPos) == "--" and not (piecePinned and forwardOne != pinDirection):
			endSpace = self.getSpace(endPos)
			availableMoves.append(Move(self, space, endSpace, pos, endPos))

			
			
		endPos = pos + forwardQ
		if not (piecePinned and forwardQ != pinDirection) and self.isMoveInbounds(pos, forwardQ):
			endSpace = self.getSpace(endPos)
			if endSpace != "--" and endSpace[0] != color:
				possiblePromotion = Move(self, space, endSpace, pos, endPos)
				if (endPos//8) == int(3.5 + (3.5 * (forwardOne // 8))):
					availableMoves.append(Promotion(possiblePromotion, "R"))
					availableMoves.append(Promotion(possiblePromotion, "B"))
					availableMoves.append(Promotion(possiblePromotion, "N"))
					availableMoves.append(Promotion(possiblePromotion, "Q"))
				else:
					availableMoves.append(possiblePromotion)
			
			if pos + (forwardQ - forwardOne) == self.fen.getEnPassantPos():
				endSpace = self.getSpace(pos + (forwardQ - forwardOne))
				availableMoves.append(EnPassant(self, space, endSpace, pos, endPos))
				enPassantIndex = len(availableMoves)-1

		endPos = pos + forwardK
		if not (piecePinned and forwardK != pinDirection) and self.isMoveInbounds(pos, forwardK):
			endSpace = self.getSpace(endPos)
			if endSpace != "--" and endSpace[0] != color:
				possiblePromotion = Move(self, space, endSpace, pos, endPos)
				if (endPos//8) == int(3.5 + (3.5 * (forwardOne//8))):
					availableMoves.append(Promotion(possiblePromotion, "R"))
					availableMoves.append(Promotion(possiblePromotion, "B"))
					availableMoves.append(Promotion(possiblePromotion, "N"))
					availableMoves.append(Promotion(possiblePromotion, "Q"))
				else:
					availableMoves.append(possiblePromotion)
			if pos + (forwardK - forwardOne) == self.fen.getEnPassantPos():
				endSpace = self.getSpace(pos + (forwardK - forwardOne))
				availableMoves.append(EnPassant(self, space, endSpace, pos, endPos))
				enPassantIndex = len(availableMoves)-1
		
		# for i in range(len(availableMoves)-1, -1, -1):
		# 	testedMove = availableMoves[i]

		# 	self.makeMove(testedMove)

		# 	if self.isSquareCovered(self.kingMap[color], color)[0]:
		# 		availableMoves.pop(i)
			
		# 	self.undoMove()
		self.removeInvalidMoves(availableMoves, (inCheck, pins, checks, kingPos,))

		# test enPassantMove
		if enPassantIndex != -1:
			enPassantMove = availableMoves[enPassantIndex]

			enPassantMove.makeMove()

			if self.isSquareCovered(kingPos, color)[0]:
				# print("removed enpassant")
				availableMoves.pop(enPassantIndex)
			
			enPassantMove.undo()
		
		return availableMoves





	def getKnightMoves(self, pos):
		directions = [6, 15, 17, 10, -6, -15, -17, -10]
		moveDepths = [1]

		return self.getPieceMoves(pos, directions, moveDepths)
	def getBishopMoves(self, pos):
		moveDepths = [x for x in range(1, 8)]
		directions = [-9, -7, 7, 9]

		return self.getPieceMoves(pos, directions, moveDepths)
	def getRookMoves(self, pos):
		moveDepths = [x for x in range(1,8)]
		directions = [-1, 8, 1, -8]

		return self.getPieceMoves(pos, directions, moveDepths)
	def getQueenMoves(self, pos):
		moveDepths = [x for x in range(1, 8)]
		directions = [-1, 8, 1, -8, -9, -7, 7, 9]

		return self.getPieceMoves(pos, directions, moveDepths)

	def getPieceMoves(self, startingPos, directions, moveDepths):
		color = self.getSpace(startingPos)[0]
		for piece in self.pieceLocationSet:
			if piece[0] == color + "K":
				kingPos = piece[1]

		inCheck, pins, checks = self.isSquareCovered(kingPos, color)
		piecePinned = False
		availableMoves = []


		for x in range(len(pins)-1, -1, -1):
			# print("STARTING ITER")
			# print(pins[x])
			# print(i, j)
			if pins[x][0] == startingPos:
				piecePinned = True
				pinDirection = (pins[x][1])
				# print("pin found")
				# print(pins[x])
				pins.pop(x)
				break

		# print(f"piecePinned = {piecePinned}")
		for direction in directions:
			if piecePinned and not (direction == pinDirection or direction == (-pinDirection)):
				# print(f"direction == pinDirection = {direction == pinDirection}")
				continue

			for depth in moveDepths:
				if not self.isMoveInbounds(startingPos, direction, depth):
					break

				startPos = startingPos
				endPos = startingPos + direction * depth
				startSpace = self.getSpace(startPos)
				endSpace = self.getSpace(endPos)
				if endSpace == "--":
					availableMoves.append(Move(self, startSpace, endSpace, startPos, endPos))
					continue
				
				if endSpace[0] != startSpace[0]:
					availableMoves.append(Move(self, startSpace, endSpace, startPos, endPos))
				break
		
		# print(startingPos)
		self.removeInvalidMoves(availableMoves, (inCheck, pins, checks, kingPos))
		
		return availableMoves

	def isMoveInbounds(self, pos, dir, depth=1) -> bool:
		if not (0 <= pos + dir*depth < 64):
			return False

		index = self.directionsToSquaresFromEdge[dir]

		return not (self.numSquaresToEdge[pos][index] < depth)

	def isSquareCovered(self, pos, color) -> tuple[bool, tuple, tuple]: 
		pins = []
		checks = []
		inCheck = False

		directions = (-8, 1, 8, -1, 9, 7, -9, -7)

		for j in range(len(directions)):
			dir = directions[j]
			possiblePin = ()
			for i in range(1, 8):
				if not self.isMoveInbounds(pos, dir, i):
					break
				testedPos = pos + dir*i

				endSpace = self.getSpace(testedPos)

				if endSpace == "--":
					continue

				if endSpace[0] == color and endSpace[1] != 'K':
					if possiblePin == ():
						possiblePin = (testedPos, dir)
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
							checks.append((testedPos, dir))
							# print("Check found")
							# print((testedPos, dir))

							break
						else: # pinned piece blocking check
							pins.append(possiblePin)
							# print("Pin found")
							# print(possiblePin)
							break
					else:
						break

		knightMoves = (-10, 6, -17, 15, -15, 17, -6, 10)
		for m in knightMoves:
			if not self.isMoveInbounds(pos, m):
				continue
			testedPos = pos + m

			endPiece = self.getSpace(testedPos)
			if endPiece == "--":
				continue
			if endPiece[0] != color and endPiece[1] == "N":
				inCheck = True
				checks.append((testedPos, m))
					
		# print("End of pin check")
		# print(inCheck, pins, checks)

		return (inCheck, pins, checks)

	def getKingMoves(self, pos):
		moveDepths = [1]
		directions = [-1, 8, 1, -8, -9, -7, 7, 9]
		
		
		availableMoves = []

		startPos = pos
		startSpace = self.getSpace(startPos)
		color = startSpace[0]

		for direction in directions:
			if not self.isMoveInbounds(startPos, direction):
				continue

			endPos = startPos + direction
			endSpace = self.getSpace(endPos)

			squareCovered, throw1, throw2 = self.isSquareCovered(endPos, color)
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
			"q": (2, 3),
			"k": (5, 6),
			"Q": (58, 59),
			"K": (61, 62)
		}

		clearSpaces = {
			"q": (1, 2, 3),
			"k": (5, 6),
			"Q": (57, 58, 59),
			"K": (61, 62)
		}

		rookKingPos = {
			"q": (4, 0),
			"k": (4, 7),
			"Q": (60, 56),
			"K": (60, 63)
		}

		if self.isSquareCovered(pos, color)[0]:
			return availableMoves

		if castle == ["-"]:
			return availableMoves

		if color == "b":
			if not self.isSquareCovered(unCheckableSpaces['q'][0], color)[0] and not self.isSquareCovered(unCheckableSpaces['q'][1], color)[0] and \
				self.getSpace(clearSpaces['q'][0]) == "--" and self.getSpace(clearSpaces['q'][1]) == "--" and self.getSpace(clearSpaces['q'][2]) == "--" and \
				self.getSpace(rookKingPos['q'][0])[1] == "K" and self.getSpace(rookKingPos['q'][1])[1] == "R" and ('q' in self.fen.castling):
					availableMoves.append(Castle(self, startSpace, self.getSpace(rookKingPos['q'][1]), rookKingPos['q'][0], rookKingPos['q'][1]))

			if not self.isSquareCovered(unCheckableSpaces['k'][0], color)[0] and not self.isSquareCovered(unCheckableSpaces['k'][1], color)[0] and \
				self.getSpace(clearSpaces['k'][0]) == "--" and self.getSpace(clearSpaces['k'][1]) == "--" and \
				self.getSpace(rookKingPos['k'][0])[1] == "K" and self.getSpace(rookKingPos['k'][1])[1] == "R" and ('k' in self.fen.castling):
					availableMoves.append(Castle(self, startSpace, self.getSpace(rookKingPos['k'][1]), rookKingPos['k'][0], rookKingPos['k'][1]))

		if color == "w":
			if not self.isSquareCovered(unCheckableSpaces['Q'][0], color)[0] and not self.isSquareCovered(unCheckableSpaces['Q'][1], color)[0] and \
				self.getSpace(clearSpaces['Q'][0]) == "--" and self.getSpace(clearSpaces['Q'][1]) == "--" and self.getSpace(clearSpaces['Q'][2]) == "--" and \
				self.getSpace(rookKingPos['Q'][0])[1] == "K" and self.getSpace(rookKingPos['Q'][1])[1] == "R" and ('Q' in self.fen.castling):
					availableMoves.append(Castle(self, startSpace, self.getSpace(rookKingPos['Q'][1]), rookKingPos['Q'][0], rookKingPos['Q'][1]))

			if not self.isSquareCovered(unCheckableSpaces['K'][0], color)[0] and not self.isSquareCovered(unCheckableSpaces['K'][1], color)[0] and \
				self.getSpace(clearSpaces['K'][0]) == "--" and self.getSpace(clearSpaces['K'][1]) == "--" and \
				self.getSpace(rookKingPos['K'][0])[1] == "K" and self.getSpace(rookKingPos['K'][1])[1] == "R" and ('K' in self.fen.castling):
					availableMoves.append(Castle(self, startSpace, self.getSpace(rookKingPos['K'][1]), rookKingPos['K'][0], rookKingPos['K'][1]))	




		return availableMoves

	def getAllMoves(self) -> list[Move]:
		color = self.fen.colorToMove
		totalMoves = []

		for piece in self.pieceLocationSet:
			if piece[0] == color + "K":
				self.kingMap[color] = piece[1]

		# for activePiece in self.pieceLocationSet:
		# 	# if activePiece[0][0] == "-":
		# 	# 	print(activePiece)
		# 	# if activePiece[0][1] == "-":
		# 	# 	print(activePiece)
		# 	if activePiece[0][0] == color:
		# 		totalMoves.extend(self.pieceMoveFunctions[activePiece[0][1]](activePiece[1]))

		for i in range(len(self.board)):
			if self.board[i][0] == color:
				if self.board[i][1] == "K":
					self.kingMap[self.board[i][0]] = i

				totalMoves.extend(self.pieceMoveFunctions[self.board[i][1]](i))
		
		return totalMoves


	def evalBoard(self):
		total = 0
		perspective = 1 if self.fen.colorToMove == "w" else -1

		# for i in range(8):
		# 	for j in range(8):
		# 		if self.board[i][j] == "--":
		# 			continue

		# 		if self.board[i][j][1] == "K":
		# 			continue
				
		# 		total += self.valueDict[self.board[i][j][1]]

		for k, v in self.pieceLocationSet:
			if k[1] == "K":
				continue
			total += self.valueDict[k[1]]
		
		return total * perspective				

	def makeMove(self, move :Move):
		# if None == move:
		# 	return
		self.fen.history.append(self.fen.getFenString(self.board))
		move.makeMove()
		self.fen.switchTurns(self.board)
		if move.pieceMoved[1] == "K":
			# print("here")
			self.kingMap[move.pieceMoved[0]] = move.endPos
		self.checkForEnPassant(move)
		self.checkCastling(move)
		# self.checkForCheckmate()
		self.moveHistory.append(move)
		# self.fen.refreshBoard(self.board)

	def undoMove(self):
		self.fen.future.append(self.fen.getFenString(self.board))
		move = self.moveHistory.pop(-1)
		move.undo()
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

	def selectionLogic(self, index :int):
		if self.selectedIndex != None: # index is selected

			space = self.getSpace(self.selectedIndex)
			if index == self.selectedIndex: # if selected index is clicked
				self.selectedIndex = None
				self.selectedMoves = []
				return

			tempMove = Move(self, space, self.getSpace(index), self.selectedIndex, index)

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

			if self.getSpace(index) == "--": # selected index is not a piece
				self.selectedIndex = None
				self.selectedMoves = []
				return

			# guarenteed that clicked index is a different piece than is selected
			if self.getSpace(index)[0] == self.fen.colorToMove:
				self.selectedIndex = index
				self.selectedMoves = self.pieceMoveFunctions[self.getSpace(index)[1]](index)
			else:
				self.selectedIndex = None
				self.selectedMoves = []

			# for move in self.selectedMoves:
			# 	print(move)
		if self.selectedIndex == None:
			if self.getSpace(index) != "--":
				self.selectedIndex = index
				self.selectedMoves = self.pieceMoveFunctions[self.getSpace(index)[1]](index)

	def getSpace(self, pos :int):
		return self.board[pos]

