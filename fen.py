from move	import Move

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
		self.setState(string)

		self.history = []
		self.future = []
	
	def setState(self, string :str) -> None:
		board, colorToMove, castling, enPassant, halfMoveCount, fullMoveCount = string.split(" ")

		self.string = string
		self.board = board
		self.colorToMove = colorToMove
		self.castling = [char for char in castling]
		self.enPassant = enPassant
		self.halfMoveCount = int(halfMoveCount)
		self.fullMoveCount = int(fullMoveCount)

	def getChessMove(self, move :Move) -> str:
		return self.colsToFiles[move.startPos%8]+self.rowsToRanks[move.startPos//8] + self.colsToFiles[move.endPos%8]+self.rowsToRanks[move.endPos//8]

	def refresh(self):
		board, colorToMove, castling, enPassant, halfMoveCount, fullMoveCount = self.string.split(" ")

		self.board = board
		self.colorToMove = colorToMove
		self.castling = [char for char in castling]
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
		self.history.append(self.string)
		self.string = state
		self.refresh()

	def refreshCastling(self):
		if self.castling == []:
			self.castling = ["-"]

	def getEnPassantPos(self):
		if self.enPassant == "-":
			return None
		return self.filesToCols[self.enPassant[0]] + self.ranksToRows[self.enPassant[1]]*8
	
	def setEnPassant(self, index):
		if index == None:
			self.enPassant = "-"
			return
		self.enPassant = self.colsToFiles[index%8] + self.rowsToRanks[index//8]
	
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

				if board[pos][0] == "b":
					boardString += board[pos][1].lower()
				else:
					boardString += board[pos][1].upper()

			if t != 0:
				boardString += str(t)

			t = 0
			if i != 7:
				boardString += "/"
		
		self.board = boardString
		
		return boardString
	
	def getFenString(self, board) -> str:
		self.refreshBoard(board)
		self.string = f"{self.board} {self.colorToMove} {''.join(self.castling)} {self.enPassant} {self.halfMoveCount} {self.fullMoveCount}"
		return self.string

	def switchTurns(self, board):
		string = self.getFenString(board)
		# print(string)
		self.history.append(string)
		if self.colorToMove == "w":
			self.colorToMove = "b"
			return
		self.colorToMove = "w"
		self.fullMoveCount += 1
		