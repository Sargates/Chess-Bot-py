from board import Board
from move import Move
import random


class AI:
	heirarchy = {
		"p": 1,
		"N": 2,
		"B": 3,
		"R": 4,
		"Q": 5,
		"K": 6

	}

	def __init__(self) -> None:
		self.totalMoves = 0
		self.maxDepth = 5
		self.depthList = {x: 0 for x in range(3)}
		self.stateList = {}
		self.captures = 0

		
		
	
	def getTotalMoves(self, depth :int, board :Board, m=None, moveList :list[str]=[]):
		if m == None:
			print(m)
			m = depth

		if depth == 0:
			return 1

		allMoves = board.getAllMoves()
		# allMoves.sort(key= lambda x: self.heirarchy[x.pieceMoved[1]])
		numPositions = 0

		for move in allMoves:
			chessMove = board.fen.getChessMove(move)

			board.makeMove(move)
			moveList.append((m-depth)*"\t" + chessMove)

			# print((m-depth)*"\t" + chessMove)
			oneStepDeep = self.getTotalMoves(depth-1, board, m, moveList)

			if depth == m:
				print(f"{chessMove}: {oneStepDeep}")

			numPositions += oneStepDeep
			# print(f"{m}\t{numPositions}", end="\r")
			

			board.undoMove()


		return numPositions
		

		

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