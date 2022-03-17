from wsgiref.types import StartResponse
from PygameExtensions import *

class Move:
	def __init__(self, board, pieceMoved :str, pieceTaken :str, startPos :tuple[int], endPos :tuple[int]) -> None:
		self.pieceMoved = pieceMoved
		self.pieceTaken = pieceTaken
		self.startPos = startPos
		self.endPos = endPos
		self.b = board
	
	def __str__(self) -> str:
		return self.b.fen.getChessMove(self)
	
	def __eq__(self, other :object) -> bool:
		if not self.pieceMoved == other.pieceMoved:
			return False
		if not self.startPos == other.startPos:
			return False
		if not self.endPos == other.endPos:
			return False
		
		return True
	
	def makeMove(self):
		self.b.pieceLocationSet.add((self.pieceMoved, self.endPos))
		self.b.pieceLocationSet.remove((self.pieceMoved, self.startPos))
		if self.pieceTaken != "--":
			self.b.pieceLocationSet.remove((self.pieceTaken, self.endPos))

		self.b.board[self.endPos] = self.pieceMoved
		self.b.board[self.startPos] = "--"


	def undo(self):
		self.b.pieceLocationSet.add((self.pieceMoved, self.startPos))
		self.b.pieceLocationSet.remove((self.pieceMoved, self.endPos))
		if self.pieceTaken != "--":
			self.b.pieceLocationSet.add((self.pieceTaken, self.endPos))

		self.b.board[self.endPos]   = self.pieceTaken
		self.b.board[self.startPos] = self.pieceMoved

	
	def redo(self):
		self.makeMove()
	
	def setBoard(self, b):
		self.b = b

class EnPassant(Move):
	def __init__(self, board, startSquare, endSquare, startPos, endPos) -> None:
		super().__init__(board, startSquare, endSquare, startPos, endPos)
		self.takenIndex = endPos-8 if endSquare[0] == "w" else endPos+8
		# print(self.takenIndex)
		
	def __str__(self) -> str:
		return f"{self.pieceMoved}, {self.pieceTaken}, {self.startPos}, {self.endPos}, Enpassant"

	def makeMove(self):
		self.b.pieceLocationSet.add((self.pieceMoved, self.endPos))
		self.b.pieceLocationSet.remove((self.pieceTaken, self.takenIndex))


		self.b.board[self.endPos] = self.pieceMoved
		self.b.board[self.startPos] = "--"
		self.b.board[self.takenIndex] = "--"

	def undo(self):
		self.b.pieceLocationSet.add((self.pieceTaken, self.takenIndex))
		self.b.pieceLocationSet.remove((self.pieceMoved, self.endPos))
		self.b.pieceLocationSet.add((self.pieceMoved, self.startPos))

		self.b.board[self.endPos]   = "--"
		self.b.board[self.startPos] = self.pieceMoved
		self.b.board[self.takenIndex] = self.pieceTaken
	
	def redo(self):
		self.makeMove()

class Castle():
	def __init__(self, board, king, rook, kingPos, rookPos) -> None:
		self.dirVector = (rookPos - kingPos) // abs(rookPos - kingPos)

		self.kingMove = Move(board, king, "--", kingPos, kingPos + self.dirVector * 2)
		self.rookMove = Move(board, rook, "--", rookPos, kingPos + self.dirVector)
		self.pieceMoved = king
		self.pieceTaken = "--"
		self.startPos = kingPos
		self.endPos = kingPos + self.dirVector * 2

		# print(self.kingMove, self.rookMove, self.pieceMoved, self.pieceTaken, self.startPos, self.endPos)
	
	def __str__(self) -> str:
		return self.kingMove.b.fen.getChessMove(self.kingMove)
		
	
	def makeMove(self):
		self.kingMove.makeMove()
		self.rookMove.makeMove()
	
	def undo(self):
		self.kingMove.undo()
		self.rookMove.undo()
	
	def redo(self):
		self.makeMove()

class Promotion():
	def __init__(self, pawnMove :Move, type :str) -> None:
		self.pawnMove = pawnMove
		self.type = type

		for k, v in pawnMove.__dict__.items():
			self.__dict__[k] = v

	def __str__(self) -> str:
		# print(self.pawnMove.startPos)
		# print(self.pawnMove.endPos)
		# print(self.type)
		return self.b.fen.getChessMove(self.pawnMove) + self.type.lower()

	def makeMove(self):
		self.pawnMove.makeMove()

		self.pawnMove.b.board[self.pawnMove.endPos] = self.pawnMove.b.board[self.pawnMove.endPos][0] + self.type
		self.pawnMove.b.waitingOnPromotion = False

		self.pawnMove.b.pieceLocationSet.remove((self.pieceMoved, self.endPos))
		self.pawnMove.b.pieceLocationSet.add((self.pawnMove.pieceMoved[0] + self.type, self.pawnMove.endPos))
		
		RenderPipeline.removeAsset(self.pawnMove.b.promotionDict["R"])
		RenderPipeline.removeAsset(self.pawnMove.b.promotionDict["B"])
		RenderPipeline.removeAsset(self.pawnMove.b.promotionDict["N"])
		RenderPipeline.removeAsset(self.pawnMove.b.promotionDict["Q"])

		self.pawnMove.b.resetPublicBoard()


	def undo(self):
		self.pawnMove.b.pieceLocationSet.remove((self.pawnMove.pieceMoved[0] + self.type, self.pawnMove.endPos))
		self.pawnMove.b.pieceLocationSet.add((self.pieceMoved, self.endPos))

		self.pawnMove.undo()
	

	
	def redo(self):
		self.makeMove()

	
	# def promotePawn(self, type):
		

