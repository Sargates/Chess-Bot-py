from board import Board
from pieces.move import Move
import random

class AI:
	def __init__(self, board :Board) -> None:
		self.board = Board()

		self.board.__dict__ == board.__dict__

	def print(self):
		string = ""
		for i in range(8):
			for j in range(8):
				string += str(self.board.board[i * 8 + j]) + " "
			string += "\n"
		
		print(string)
	
	def search(self, depth):
		allMoves = self.board.getAllMoves("b")

		index = random.randint(0, len(allMoves)-1)
		selectedMove = allMoves[index]

		selectedMove.makeMove()
		