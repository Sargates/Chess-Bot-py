import pygame, os


from pieces.move   import *
from pieces.piece import Piece

from fen import Fen

WIDTH = HEIGHT = 768
WINDOWSIZE = (WIDTH, HEIGHT)
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
SQ_SIZE = ((256 - 80)/8) * (WIDTH/256)
OFFSET = 40 * (WIDTH/256)
PIECE_OFFSET = (10/11) * SQ_SIZE / 2

pygame.init()

class Board:

	board = ["--" for x in range(64)]
	selectedIndex = -1
	selectedMoves = []
	moveHistory = []
	futureMoves = []
	highlightedSquares = set()
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
	infoDict = {}

	def loadImages(self):
		self.images = []

		for piece in ['bB', 'bK', 'bN', 'bp', 'bQ', 'bR', 'wB', 'wK', 'wN', 'wp', 'wQ', 'wR']:
			self.images.append(pygame.transform.scale(pygame.image.load(os.path.join(os.path.dirname(os.path.abspath(__file__)) + "/img/" + piece + '.png')), (int(SQ_SIZE * 10/11), int(SQ_SIZE * 10/11))))
		
		self.boardImage = pygame.transform.scale(pygame.image.load(os.path.join(os.path.dirname(os.path.abspath(__file__)) + "/img/board_alt.png")), (WIDTH, HEIGHT))

	def __init__(self) -> None:
		self.loadImages()



		self.fen = Fen("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")

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
	
	def checkForCheckmate(self):
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
			
			totalMoves = []
			for piece in team:
				moves = piece[0].getMoves(self, piece[1])
				if piece[0].type == "K":
					king.removeInvalidMoves(self, moves, king.getChecksandPins(self, king.getPos(self)) + (king.getPos(self),))
				totalMoves.extend(moves)

			if totalMoves == []:
				print("Checkmate!")
				
				self.reset()


	
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

	def selectionLogic(self, index :int):
		if self.selectedIndex != -1: # index is selected

			space = self.getSpace(self.selectedIndex)
			if index == self.selectedIndex: # if selected index is clicked
				self.selectedIndex = -1
				self.selectedMoves = []
				return

			move = Move(space, self.getSpace(index), self.selectedIndex, index)

			if move in self.selectedMoves: # if index in in avialable moves
				self.moveHistory.append(move)
				move.makeMove()
				self.refreshChecksandPins()

				self.selectedIndex = -1
				self.selectedMoves = []
				self.futureMoves = []
				print(self.whiteInfo)
				print(self.blackInfo)
				self.fen.switchTurns()
				self.checkForCheckmate()
				return

			if self.getSpace(index) == "--": # selected index is not a piece
				self.selectedIndex = -1
				self.selectedMoves = []
				return
			
			# guarenteed that clicked index is a different piece than is selected
			if self.getSpace(index).color == self.fen.colorToMove:
				self.selectedIndex = index
				self.selectedMoves = self.getSpace(self.selectedIndex).getMoves(self, self.selectedIndex)

			for move in self.selectedMoves:
				print(move)


			return
			

		# index is not selected
		if self.getSpace(index) != "--":
			if self.getSpace(index).color == self.fen.colorToMove:
				self.selectedIndex = index
				self.selectedMoves = self.getSpace(self.selectedIndex).getMoves(self, self.selectedIndex)

		for move in self.selectedMoves:
				print(move)

			

	def getSpace(self, index) -> Piece:
		return self.board[index]



def getPosToIndex(x, y):
	newX = (x - 40 * (WIDTH/256)) // (22 * (WIDTH/256))
	newY = (y - 40 * (WIDTH/256)) // (22 * (WIDTH/256))
	
	if (0 <= newX < 8 and 0 <= newY < 8):
		return int(newY * 8 + newX)
	
	return -1

def getIndexToPos(index):
	x = (index % 8)  * 22 * WIDTH/256 + 40 *(WIDTH/256)
	y = (index // 8) * 22 * WIDTH/256 + 40 *(WIDTH/256)
	
	x += SQ_SIZE/2
	y += SQ_SIZE/2

	return (x, y)

def renderBoard(b :Board):
	SCREEN.blit(pygame.transform.scale(b.boardImage, (HEIGHT, HEIGHT)), ((WIDTH/2)-(HEIGHT/2), 0))

def renderPieces(b :Board):
	for i in range(len(b.board)):
		space = b.board[i]
		if space != "--":
			xPosition = (i % 8)
			yPosition = (i // 8)
			SCREEN.blit((b.images[b.idToIndex[space.ID]]), (OFFSET + (xPosition*SQ_SIZE)+SQ_SIZE/2 - PIECE_OFFSET, OFFSET + (yPosition*SQ_SIZE)+SQ_SIZE/2 - PIECE_OFFSET))

def renderHighlighted(b :Board):
	highlightedScreen = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
	for index in b.highlightedSquares:
		x, y = getIndexToPos(index)
		square = pygame.Rect(x-SQ_SIZE/2, y-SQ_SIZE/2, SQ_SIZE, SQ_SIZE)

		pygame.draw.rect(highlightedScreen, (255, 0, 0, 100), square, 0)
	
	SCREEN.blit(highlightedScreen, (0, 0))

def renderMoves(b :Board):
	if b.selectedIndex != -1:
		piece = b.getSpace(b.selectedIndex)
		if piece == "--":
			b.selectedIndex = -1
			return

		for move in b.selectedMoves:
			pygame.draw.circle(SCREEN, (255, 0, 0), getIndexToPos(move.endPos), SQ_SIZE/5)


def renderSelected(b :Board):
	if b.selectedIndex != -1:
		x, y = getIndexToPos(b.selectedIndex)
		square = pygame.Rect(x-SQ_SIZE/2, y-SQ_SIZE/2, SQ_SIZE, SQ_SIZE)
		pygame.draw.rect(SCREEN, (255, 0, 0), square, 2)

def render(board : Board):

	renderBoard(board)
	renderHighlighted(board)
	renderSelected(board)
	renderPieces(board)
	renderMoves(board)

	pygame.display.update()

def main():

	board = Board()
	Move.setBoard(board)

	run = True
	while run:
		mousePos = pygame.mouse.get_pos()

		for e in pygame.event.get():
			if e.type == pygame.QUIT:
				pygame.quit()
				quit()
			if e.type == pygame.MOUSEBUTTONDOWN:
				index = getPosToIndex(*mousePos)
				if (index != -1):
					if e.button == 1:
						board.highlightedSquares = set()
						board.selectionLogic(index)
				if e.button == 3:
					if not index in board.highlightedSquares:
						board.highlightedSquares.add(index)
						print(f"  Highlighted Index {index}")
					else:
						board.highlightedSquares.remove(index)
						print(f"Unhighlighted Index {index}")
						
			if e.type == pygame.KEYDOWN:
				if e.key == pygame.K_z and len(board.moveHistory) > 0:
					move = board.moveHistory.pop(-1)
					move.undo()
					board.futureMoves.append(move)
					board.fen.switchTurns()
				elif e.key == pygame.K_y and len(board.futureMoves) > 0:
					move = board.futureMoves.pop(-1)
					move.redo()
					board.moveHistory.append(move)
					board.fen.switchTurns()
				elif e.key == pygame.K_v:
					print(board.whiteInfo)
					print(board.blackInfo)

					print(board.getSpace(board.selectedIndex).timesMoved)

					# for pin in board.whiteInfo[1] + board.blackInfo[1]:
					# 	print(board.getSpace(pin[1]*8 + pin[0]))

		
		render(board)
			


main()