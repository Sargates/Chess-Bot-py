class Move:
	def __init__(self, board, pieceMoved, pieceTaken, startPos, endPos) -> None:
		self.pieceMoved = pieceMoved
		self.pieceTaken = pieceTaken
		self.startPos = startPos
		self.endPos = endPos
		self.b = board
	
	def __str__(self) -> str:
		return f"{self.pieceMoved}, {self.pieceTaken}, {self.startPos}, {self.endPos}"
	
	def __eq__(self, other :object) -> bool:
		if not self.pieceMoved == other.pieceMoved:
			return False
		if not self.startPos == other.startPos:
			return False
		if not self.endPos == other.endPos:
			return False
		
		return True
	
	def makeMove(self):
		self.b.board[self.endPos[1]][self.endPos[0]] = self.pieceMoved
		self.b.board[self.startPos[1]][self.startPos[0]] = "--"

	def undo(self):
		self.b.board[self.endPos]   = self.pieceTaken
		self.b.board[self.startPos] = self.pieceMoved
	
	def redo(self):
		self.makeMove()
	
	def setBoard(self, b):
		self.b = b

class Castle():
	def __init__(self, board, king, rook, kingPos, rookPos) -> None:
		dirVector = (rookPos - kingPos) // abs(rookPos - kingPos)

		self.kingMove = Move(board, king, "--", kingPos, kingPos + dirVector * 2)
		self.rookMove = Move(board, rook, "--", rookPos, kingPos + dirVector)
		self.pieceMoved = king
		self.pieceTaken = "--"
		self.startPos = kingPos
		self.endPos = kingPos + dirVector * 2

		# print(self.kingMove, self.rookMove, self.pieceMoved, self.pieceTaken, self.startPos, self.endPos)
	
	def makeMove(self):
		self.kingMove.makeMove()
		self.rookMove.makeMove()
	
	def undo(self):
		self.kingMove.undo()
		self.rookMove.undo()
	
	def redo(self):
		self.makeMove()

class EnPassant(Move):
	def __init__(self, board, startSquare, endSquare, startPos, endPos) -> None:
		super().__init__(board, startSquare, endSquare, startPos, endPos)
		self.takenIndex = endPos-8 if endSquare[0] == "w" else endPos+8
		# print(self.takenIndex)
		
	def __str__(self) -> str:
		return f"{self.pieceMoved}, {self.pieceTaken}, {self.startPos}, {self.endPos}"

	def makeMove(self):
		self.b.board[self.endPos] = self.pieceMoved
		self.b.board[self.startPos] = "--"
		self.b.board[self.takenIndex] = "--"
		self.pieceMoved.timesMoved += 1

	def undo(self):
		self.b.board[self.endPos]   = "--"
		self.b.board[self.startPos] = self.pieceMoved
		self.b.board[self.takenIndex] = self.pieceTaken
		self.pieceMoved.timesMoved -= 1
	
	def redo(self):
		self.makeMove()