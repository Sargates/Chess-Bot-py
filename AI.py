from board import Board
from pieces.move import Move
import random


class AI:
	def __init__(self) -> None:
		self.totalMoves = 0
		self.maxDepth = 5
		self.depthList = {x: 0 for x in range(self.maxDepth, 0, -1)}
		pass
	
	def getTotalMoves(self, depth :int, board :Board):
		allMoves = board.getAllMoves()
		

		if depth == 0:
			return

		self.depthList[depth] += len(allMoves)

		print(self.depthList, end="\r")



		for move in allMoves:
			board.makeMove(move)

			self.getTotalMoves(depth-1, board)

			board.undoMove()


	def getMove(self, board :Board) -> Move:
		self.totalMoves = 0
		allMoves = board.getAllMoves()

		bestMove = None
		bestEval = -(2**31)

		self.depthList[self.maxDepth] += len(allMoves)

		for move in allMoves:
			board.makeMove(move)

			iterEval = -self.search(self.maxDepth, board)
			if bestEval < iterEval:
				bestEval = iterEval
				bestMove = move

			board.undoMove()
		
		return bestMove
	
	def search(self, depth, board :Board) -> int:
		allMoves = board.getAllMoves()

		self.depthList[depth] += len(allMoves)

		if depth == 0:
			return board.evalBoard()		

		kingPositions = board.getKingPos()
		index = 0 if board.fen.colorToMove == "w" else 1
		
		if board.isSquareCovered(*kingPositions[index], board.fen.colorToMove):
			return -(2**31)

		eval = -(2**31)

		for move in allMoves:
			board.makeMove(move)

			eval = max(eval, -self.search(depth-1, board))

			board.undoMove()


		return eval
	
	def evalBoard(self, board :Board):
		return board.evalBoard()