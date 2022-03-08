from board import Board
from pieces.move import Move
import random


class AI:
	def __init__(self) -> None:
		self.totalMoves = 0
		self.depthList = {x: 0 for x in range(10, 0, -1)}
		pass
	
	def getTotalMoves(self, depth :int, board :Board):
		allMoves = board.getAllMoves()
		
		if depth == 0:
			return

		self.depthList[depth] += len(allMoves)
		print(self.depthList, end="\r")



		for move in allMoves:
			board.makeMoveOnBoard(move, True)

			self.getTotalMoves(depth-1, board)

			board.unmakeMoveOnBoard()


	def getMove(self, board :Board) -> Move:
		self.totalMoves = 0
		allMoves = board.getAllMoves()

		bestMove = None
		bestEval = -(2**31)
		for move in allMoves:
			board.makeMoveOnBoard(move, True)

			iterEval = -self.search(0, board)
			if bestEval < iterEval:
				bestEval = iterEval
				bestMove = move

			board.unmakeMoveOnBoard()
		
		return bestMove
	
	def search(self, depth, board :Board) -> int:
		allMoves = board.getAllMoves()

		if depth == 0:
			self.totalMoves += len(allMoves)
			return board.evalBoard()

		eval = -(2**31)

		for move in allMoves:
			board.makeMoveOnBoard(move, True)

			eval = max(eval, -self.search(depth-1, board))

			board.unmakeMoveOnBoard()


		return eval
	
	def evalBoard(self, board :Board):
		return board.evalBoard()