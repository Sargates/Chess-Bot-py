from pieces.bishop import Bishop
from pieces.king   import King
from pieces.knight import Knight
from pieces.pawn   import Pawn
from pieces.queen  import Queen
from pieces.rook   import Rook

class Fen:
	# rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1
	

	def __init__(self, string :str) -> None:
		self.string = string
		board, colorToMove, castling, enPassant, halfMoveCount, fullMoveCount = string.split(" ")
		
		self.board = board
		self.colorToMove = colorToMove
		self.castling = castling
		self.enPassant = enPassant
		self.halfMoveCount = halfMoveCount
		self.fullMoveCount = fullMoveCount
	
	def reset(self):
		string = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
		self.string = string
		board, colorToMove, castling, enPassant, halfMoveCount, fullMoveCount = string.split(" ")
		
		self.board = board
		self.colorToMove = colorToMove
		self.castling = castling
		self.enPassant = enPassant
		self.halfMoveCount = halfMoveCount
		self.fullMoveCount = fullMoveCount
		
	def __str__(self):
		return self.board + " " + self.colorToMove + " " + self.castling + " " + self.enPassant + " " + self.halfMoveCount + " " + self.fullMoveCount
	
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


	def switchTurns(self):
		if self.colorToMove == "w":
			self.colorToMove = "b"
			return
		self.colorToMove = "w"
		