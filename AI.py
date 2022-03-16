from tkinter import E
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
		self.maxDepth = 2
		self.depthList = {x: 0 for x in range(5)}
		self.stateList = {}
		self.captures = 0

		
		
	
	def getTotalMoves(self, depth :int, board :Board, m=None, moveList :list[str]=[]):
		if m == None:
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

			
			fkjhadsljfhasdkjlfh = print(f"{move}: {oneStepDeep}") if (depth == m and depth != 1) else None

			numPositions += oneStepDeep
			# print(f"{m}\t{numPositions}", end="\r")
			

			board.undoMove()


		return numPositions

	def getMove(self, board :Board) -> Move:
		self.totalMoves = 0
		allMoves = board.getAllMoves()

		bestMove = None
		bestEval = -(2**31)

		kingPos = board.kingMap[board.fen.colorToMove]
		print(len(allMoves))

		for move in allMoves:
			board.makeMove(move)

			iterEval = -self.search(self.maxDepth, board)
			# print(f"{move}: {1}, {iterEval}")

			if bestEval < iterEval:
				bestEval = iterEval
				bestMove = move
				

			board.undoMove()
		
		return bestMove
	
	def search(self, depth, board :Board) -> int:
		if depth == 0:
			return board.evalBoard()
		allMoves = board.getAllMoves()

		if len(allMoves) == 0:
			return -(2**31)

	
		kingPos = board.kingMap[board.fen.colorToMove]
		
		if board.isSquareCovered(*kingPos, board.fen.colorToMove)[0]:
			return -(2**31)+1



		eval = -(2**31)

		for move in allMoves:
			board.makeMove(move)

			eval = max(eval, -self.search(depth-1, board))
			# print(f"{move}\t{eval}", end="\n")
			tabDepth = (self.maxDepth-depth)*'\t'
			# print(f"{tabDepth}{move}: {self.maxDepth-depth+1}, {eval}")

			board.undoMove()


		return eval
	
	def evalBoard(self, board :Board):
		return board.evalBoard()