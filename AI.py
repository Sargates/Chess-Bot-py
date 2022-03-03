from re import search
from board import Board
from pieces.move import Move
import random

class AI:
	def __init__(self) -> None:
		self.eval = None
		pass

	def getMove(self, board :Board):
		return self.search(1, board)
	
	def search(self, depth, board :Board):
		allMoves = board.getAllMoves()
		if depth == 0:
			return allMoves[0]

		for move in allMoves:
			board.makeMoveOnBoard(move)

			tempMove = search(depth-1, board)
			if evaluation > board.evalBoard():
				pass

			board.unmakeMoveOnBoard(move)

		# selectedMove = allMoves[]

		return selectedMove
	
	def evalBoard(self, board :Board):
		return board.evalBoard()