from pieces.bishop import Bishop
from pieces.king   import King
from pieces.knight import Knight
from pieces.pawn   import Pawn
from pieces.queen  import Queen
from pieces.rook   import Rook

class Fen:
	# rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1
	ranksToRows = {'1': 7, '2': 6, '3': 5, '4': 4,
				   '5': 3, '6': 2, '7': 1, '8': 0}
	rowsToRanks = {v: k for k, v in ranksToRows.items()}
	filesToCols = {'a': 0, 'b': 1, 'c': 2, 'd': 3,
				   'e': 4, 'f': 5, 'g': 6, 'h': 7}
	colsToFiles = {v: k for k, v in filesToCols.items()}
	

	def __init__(self, string :str) -> None:
		board, colorToMove, castling, enPassant, halfMoveCount, fullMoveCount = string.split(" ")

		self.board = board
		self.colorToMove = colorToMove
		self.castling = castling
		self.enPassant = enPassant
		self.halfMoveCount = int(halfMoveCount)
		self.fullMoveCount = int(fullMoveCount)
		
		self.history = []
		self.future = []

	def refresh(self):
		board, colorToMove, castling, enPassant, halfMoveCount, fullMoveCount = self.string.split(" ")

		self.board = board
		self.colorToMove = colorToMove
		self.castling = castling
		self.enPassant = enPassant
		self.halfMoveCount = int(halfMoveCount)
		self.fullMoveCount = int(fullMoveCount)

	def undo(self):
		state = self.history.pop(-1)
		self.string = state
		self.refresh()
		self.future.append(state)
	
	def redo(self):
		state = self.future.pop(-1)
		self.string = state
		self.refresh()
		self.history.append(state)

	def getEnPassantPos(self):
		if self.enPassant == "-":
			return -1
		return self.ranksToRows[self.enPassant[1]] * 8 + self.filesToCols[self.enPassant[0]]
	
	def setEnPassant(self, index):
		if index == -1:
			self.enPassant = "-"
			return
		self.enPassant = self.colsToFiles[index%8] + self.rowsToRanks[index // 8]
	
	def promotePawn(self, b, position):
		b[position] = Queen(b[position].color)
	
	def reset(self):
		string = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
		self.__init__(string)

	def smartPieceDict(self, string):
	
		if string == "r":
			return   Rook("b")
		if string == "n":
			return Knight("b")
		if string == "b":
			return Bishop("b")
		if string == "q":
			return  Queen("b")
		if string == "k":
			return   King("b")
		if string == "p":
			return   Pawn("b")
		if string == "P":
			return   Pawn("w")
		if string == "R":
			return   Rook("w")
		if string == "N":
			return Knight("w")
		if string == "B":
			return Bishop("w")
		if string == "Q":
			return  Queen("w")
		if string == "K":
			return   King("w")  

	def boardParse(self):
		ranks = self.board.split("/")
		board = ["--" for x in range(64)]
		i=0
		for y in range(len(ranks)):
			for symbol in ranks[y]:
				if symbol.isdigit():
					i += int(symbol)
					continue
				board[i] = self.smartPieceDict(symbol)
				i += 1
		
		return board
	
	def refreshBoard(self, board):
		boardString = ""
		t = 0
		for i in range(8):
			for j in range(8):
				pos = i * 8 + j
				if board[pos] == "--":
					t += 1
					continue
				
				if t != 0:
					boardString += str(t)
					t = 0

				if board[pos].color == "b":
					boardString += board[pos].type.lower()
				else:
					boardString += board[pos].type.upper()
				

			if t != 0:
				boardString += str(t)
			

			t = 0

			if i != 7:
				boardString += "/"
		
		self.board = boardString
		
		return boardString
	
	def getFenString(self, board) -> str:
		self.refreshBoard(board)	
		return f"{self.board} {self.colorToMove} {self.castling} {self.enPassant} {self.halfMoveCount} {self.fullMoveCount}"

	def switchTurns(self, board):
		self.future = []
		if self.colorToMove == "w":
			self.history.append(self.getFenString(board))
			self.colorToMove = "b"
			return
		self.history.append(self.getFenString(board))
		self.colorToMove = "w"
		self.fullMoveCount += 1
		