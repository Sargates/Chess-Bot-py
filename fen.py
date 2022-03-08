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

	pieceDict = {
		"r": "bR",
		"n": "bN",
		"b": "bB",
		"q": "bQ",
		"k": "bK",
		"p": "bp",
		"R": "wR",
		"N": "wN",
		"B": "wB",
		"Q": "wQ",
		"K": "wK",
		"P": "wp",
	}

	def __init__(self, string :str) -> None:
		board, colorToMove, castling, enPassant, halfMoveCount, fullMoveCount = string.split(" ")

		self.string = string
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
		self.future.append(self.string)
		self.string = state
		self.refresh()
	
	def redo(self):
		state = self.future.pop(-1)
		self.history.append(state)
		self.string = state
		self.refresh()

	def refreshCastling(self, board):
		castle = ""
		for pos in board.updateKingPos():
			king = board.getSpace(pos)
			if not ((king.color == "w" and pos == 60) or (king.color == "b" and pos == 4)):
				# print(1)
				continue

			if king.timesMoved != 0:
				# print(2)
				continue

			qRook = board.getSpace(pos-4)
			kRook = board.getSpace(pos+3)
			inCheck, pins, checks = king.getChecksandPins(board, pos)

			if inCheck:
				continue

			if kRook != "--" and kRook.timesMoved == 0:
				if king.color == "w":
					castle += "K"
				else:
					castle += "k"
			if qRook != "--" and qRook.timesMoved == 0:
				if king.color == "w":
					castle += "Q"
				else:
					castle += "q"
		
		if castle == "":
			castle = "-"
		self.castling = castle

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
		b[position] = b[position][0]+"Q"
	
	def reset(self):
		string = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
		self.__init__(string)

	def boardParse(self):
		ranks = self.board.split("/")
		board = ["--" for x in range(64)]
		i=0
		for y in range(len(ranks)):
			for symbol in ranks[y]:
				if symbol.isdigit():
					i += int(symbol)
					continue
				board[i] = self.pieceDict[symbol]
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
		self.string = f"{self.board} {self.colorToMove} {self.castling} {self.enPassant} {self.halfMoveCount} {self.fullMoveCount}"
		return self.string

	def switchTurns(self, board):
		self.future = []
		string = self.getFenString(board)
		# print(string)
		self.history.append(string)
		if self.colorToMove == "w":
			self.colorToMove = "b"
			return
		self.colorToMove = "w"
		self.fullMoveCount += 1
		