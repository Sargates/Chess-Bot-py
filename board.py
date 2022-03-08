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

	def getAllMoves(self, ):
		pass

	def evalBoard(self, ):
		pass

	def makeMove(self, ):
		pass

	def undoMove(self, ):
		pass

	def selectionLogic(self, ):
		pass

	def getSpace(self, x, y):
		return self.board[y][x]

