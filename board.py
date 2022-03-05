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

	pieceValue = {
		  Pawn: 1, 
		Bishop: 3, 
		Knight: 3, 
		  Rook: 5, 
		 Queen: 9, 
	}

	checkMate = False
	matchDraw = False

	def loadImages(self):
		self.images = []

		for piece in ['bB', 'bK', 'bN', 'bp', 'bQ', 'bR', 'wB', 'wK', 'wN', 'wp', 'wQ', 'wR']:
			self.images.append(pygame.transform.scale(pygame.image.load(os.path.join(os.path.dirname(os.path.abspath(__file__)) + "/img/" + piece + '.png')), (int(SQ_SIZE * 10/11), int(SQ_SIZE * 10/11))))
		
		self.boardImage = pygame.transform.scale(pygame.image.load(os.path.join(os.path.dirname(os.path.abspath(__file__)) + "/img/board_alt.png")), (WIDTH, HEIGHT))

	def __init__(self) -> None:
		self.loadImages()


		self.board = ["--" for x in range(64)]
		self.selectedIndex = -1
		self.selectedMoves = []
		self.moveHistory = []
		self.futureMoves = []
		self.highlightedSquares = set()



		self.fen = Fen("8/4npk1/5p1p/1Q5P/1p4P1/4r3/7q/3K1R2 w - - 1 49")
		
		# self.fen = Fen("8/6k1/5p1p/4Q2P/1n4P1/8/8/3K4 w - - 1 49")
		# self.fen = Fen("8/8/3k1nQP/8/6P1/8/8/3K4 b - - 1 49")
		# self.fen = Fen("1Q6/8/8/8/8/8/k1K5/8 w - - 18 50")
		# self.fen.reset()

		self.board = self.fen.boardParse()

		pos = self.updateKingPos()
		self.whiteKing = self.board[pos[0]]
		self.blackKing = self.board[pos[1]]

		self.whiteInfo = self.whiteKing.getChecksandPins(self, self.whiteKing.getPos(self)) + (60,)
		self.blackInfo = self.blackKing.getChecksandPins(self, self.blackKing.getPos(self)) + ( 4,)

		self.kingDict = {
			"w": self.whiteKing,
			"b": self.blackKing
		}

		self.infoDict = {
			"w": self.whiteKing.getChecksandPins(self, self.whiteKing.getPos(self)) + (self.whiteKing.getPos(self),),
			"b": self.blackKing.getChecksandPins(self, self.blackKing.getPos(self)) + (self.blackKing.getPos(self),)
		}
	
	def reset(self):
		for i in range(len(self.board)-1, -1, -1):
			del self.board[i]

		self.fen.reset()

		self.board = self.fen.boardParse()

		self.whiteKing = self.board[60]
		self.blackKing = self.board[ 4]

		self.whiteInfo = self.whiteKing.getChecksandPins(self, self.whiteKing.getPos(self)) + (60,)
		self.blackInfo = self.blackKing.getChecksandPins(self, self.blackKing.getPos(self)) + ( 4,)

		self.kingDict = {
			"w": self.whiteKing,
			"b": self.blackKing
		}

		self.infoDict = {
			"w": self.whiteKing.getChecksandPins(self, self.whiteKing.getPos(self)) + (self.whiteKing.getPos(self),),
			"b": self.blackKing.getChecksandPins(self, self.blackKing.getPos(self)) + (self.blackKing.getPos(self),)
		}
	
	def refreshChecksandPins(self):
		kingPos = self.updateKingPos()
		self.whiteInfo = self.whiteKing.getChecksandPins(self, kingPos[0]) + (kingPos[0],)
		self.blackInfo = self.blackKing.getChecksandPins(self, kingPos[1]) + (kingPos[1],)
	
	def checkForPromotion(self, move :Move):
		if move.pieceMoved.type == "p":
			# print(move, self.getSpace(move.endPos))
			if move.endPos // 8 in [0, 7]:
				print("promoting")
				self.fen.promotePawn(self.board, move.endPos)
				print("Promoted")
				print(move, self.getSpace(move.endPos))
		pass

	def checkForEnPassant(self, move :Move):
		if move.pieceMoved.type == "p":
			if abs(move.endPos - move.startPos) == 16:
				index = move.startPos + 8 if move.pieceMoved.color == "b" else move.startPos - 8
				self.fen.setEnPassant(index)
				# print(self.fen.enPassant)
				return
		self.fen.setEnPassant(-1)
		
		pass

	def checkForCheckmate(self, quiet=False):
		# print("big cum")
		for j in range(2):
			king = [self.whiteKing, self.blackKing][j]

			team = []
			for i in range(len(self.board)):
				space = self.board[i]
				if space == "--":
					continue
				if space.color != king.color:
					continue
				team.append((space, i))
			inCheck, pins, checks = king.getChecksandPins(self, king.getPos(self))
			
			totalMoves = []
			for piece in team:
				moves = piece[0].getAttackingMoves(self, piece[1])

				king.removeInvalidMoves(self, moves, king.getChecksandPins(self, king.getPos(self)) + (king.getPos(self),))
	
				totalMoves.extend(moves)
			if totalMoves == [] and not quiet:
				if inCheck:
					self.checkMate = True
					return

				self.matchDraw = True

	def updateKingPos(self):
		for i in range(len(self.board)):
			space = self.getSpace(i)
			if space == "--":
				continue

			if space.type != "K":
				continue

			if space.color == "b":
				blackPos = i
			else:
				whitePos = i
		
		return (whitePos, blackPos)
	
	def getAllMoves(self) -> list[Move]:
		# color 0 = Black, 1 = White
		moveList = []
		color = self.fen.colorToMove
		for i in range(len(self.board)):
			space = self.board[i]
			if space == "--":
				continue
		
			if space.color != color:
				continue

			allMoves = space.getMoves(self, i)

			space.removeInvalidMoves(self.board, allMoves, self.infoDict[color])

			moveList.extend(allMoves)
		
		self.kingDict[color]
		return moveList
	
	def evalBoard(self):
		total = 0
		perspective = -1 if self.fen.colorToMove == "b" else 1
		for space in self.board:
			if space == "--":
				continue

			if space.type == "K":
				continue

			if space.color == "b":
				total -= self.pieceValue[type(space)]
				continue

			total += self.pieceValue[type(space)]

		return total * perspective
	
	def makeMoveOnBoard(self, move :Move, quiet=False):
		self.moveHistory.append(move)
		if not quiet:
			if move.pieceMoved.type == "p":
				self.fen.halfMoveCount = 0
			else:
				self.fen.halfMoveCount += 1
		
		self.futureMoves = []

		self.fen.switchTurns(self.board)
		move.makeMove()
		self.checkForPromotion(move)
		self.checkForEnPassant(move)
		self.refreshChecksandPins()
		self.fen.refreshCastling(self)
		self.checkForCheckmate(quiet)
	
	def unmakeMoveOnBoard(self):
		move = self.moveHistory.pop(-1)
		self.futureMoves.append(move)
		self.fen.undo()
		move.undo()
		self.checkForPromotion(move)
		self.checkForEnPassant(move)
		self.refreshChecksandPins()
		self.fen.refreshCastling(self)
		self.checkForCheckmate()


	def selectionLogic(self, index :int):
		if self.selectedIndex != -1: # index is selected

			space = self.getSpace(self.selectedIndex)
			if index == self.selectedIndex: # if selected index is clicked
				self.selectedIndex = -1
				self.selectedMoves = []
				return

			tempMove = Move(self, space, self.getSpace(index), self.selectedIndex, index)
			
			if tempMove in self.selectedMoves: # if index in in avialable moves
				move = self.selectedMoves[self.selectedMoves.index(tempMove)]
				self.makeMoveOnBoard(move)

				self.selectedIndex = -1
				self.selectedMoves = []
				"""
				# print(self.whiteInfo)
				# print(self.blackInfo)
				# print(f"\n{self.fen.getFenString(self.board)}")
				"""
				return

			if self.getSpace(index) == "--": # selected index is not a piece
				self.selectedIndex = -1
				self.selectedMoves = []
				return
			
			# guarenteed that clicked index is a different piece than is selected
			if self.getSpace(index).color == self.fen.colorToMove:
				self.selectedIndex = index
				self.selectedMoves = self.getSpace(self.selectedIndex).getMoves(self, self.selectedIndex)
			else:
				self.selectedIndex = -1
				self.selectedMoves = []

			# for move in self.selectedMoves:
				# print(move)


			return
			

		# index is not selected
		if self.getSpace(index) != "--":
			if self.getSpace(index).color == self.fen.colorToMove:
				self.selectedIndex = index
				self.selectedMoves = self.getSpace(self.selectedIndex).getMoves(self, self.selectedIndex)

		# for move in self.selectedMoves:
		# 		print(move)

			

	def getSpace(self, index) -> Piece:
		return self.board[index]
