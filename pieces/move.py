class Move:
	def __init__(self, pieceMoved, pieceTaken, startPos, endPos) -> None:
		self.pieceMoved = pieceMoved
		self.pieceTaken = pieceTaken
		self.startPos = startPos
		self.endPos = endPos
	
	def __str__(self) -> str:
		return f"{self.pieceMoved}, {self.pieceTaken}, {self.startPos}, {self.endPos}"
	
	def __eq__(self, other) -> bool:
		if not self.pieceMoved == other.pieceMoved:
			return False
		if not self.pieceTaken == other.pieceTaken:
			return False
		if not self.startPos == other.startPos:
			return False
		if not self.endPos == other.endPos:
			return False
		
		return True
	
	def makeMove(self):
		self.b.board[self.endPos] = self.pieceMoved
		self.b.board[self.startPos] = "--"
		self.pieceMoved.timesMoved += 1

	def undo(self):
		self.b.board[self.endPos]   = self.pieceTaken
		self.b.board[self.startPos] = self.pieceMoved
		self.pieceMoved.timesMoved -= 1
	
	def redo(self):
		self.b.board[self.endPos] = self.pieceMoved
		self.b.board[self.startPos] = "--"
		self.pieceMoved.timesMoved += 1
	
	@staticmethod
	def setBoard(b):
		Move.b = b

class Castle():
	def __init__(self, pieceMoved, pieceTaken, startPos, endPos) -> None:
		pass

class EnPassant():
	def __init__(self) -> None:
		pass