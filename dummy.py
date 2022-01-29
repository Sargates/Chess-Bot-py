from pieces.bishop import Bishop
from pieces.king   import King
from pieces.knight import Knight
from pieces.pawn   import Pawn
from pieces.queen  import Queen
from pieces.rook   import Rook

class Fen:
	# rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1
	pieceDict = {
		"r":   Rook("b"),
		"n": Knight("b"),
		"b": Bishop("b"),
		"q":  Queen("b"),
		"k":   King("b"),
		"p":   Pawn("b"),
		"P":   Pawn("w"),
		"R":   Rook("w"),
		"N": Knight("w"),
		"B": Bishop("w"),
		"Q":  Queen("w"),
		"K":   King("w")  
	}

	def __init__(self, string :str) -> None:
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


f = Fen("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")


board = f.boardParse()
string = ""
for i in range(len(board)):
	if i % 8 == 0:
		string += "\n"
	string += str(board[i])
	string += "  "

print(string)