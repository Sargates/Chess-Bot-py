from board import Board
from move import Castle, EnPassant, Move, Promotion
import random, time


class AI:
	heirarchy = {
		"p": 1,
		"N": 2,
		"B": 3,
		"R": 4,
		"Q": 5,
		"K": 6
	}

	# change depth that AI searches on my personal desktop 
	# it takes about 4~8 seconds searching 3 moves deep, 
	# avg moves/depth is ~45
	maxDepth = 3

	def __init__(self) -> None:
		self.totalMoves = 0
		self.depthList = {x: 0 for x in range(self.maxDepth)}
		self.stateList = {}
		self.captures = 0

	def getTotalMoves(self, depth :int, board :Board, m=None, moveList :list[str]=[]):
		if m == None:
			m = depth

		if m - depth == 0:
			startTime = time.time()

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

			

			numPositions += oneStepDeep
			print(f"{m}\t{len(moveList)}", end="\r")
			

			board.undoMove()

		if m - depth == 0:
			endTime = time.time()
			print(f"Depth {depth}: {endTime - startTime}, {len(moveList)}")

		return numPositions

	def getMove(self, board :Board) -> Move:
		startTime = time.time()
		self.totalMoves = 0
		allMoves = board.getAllMoves()

		"""
		Big thanks to Sebastian Lague on Youtube for
		help on the search algorithm for the best move 
		based on board evaluation
		https://youtu.be/U4ogK0MIzqk?t=732
		"""

		bestMove = None
		bestEval = -(2**31)-1


		for move in allMoves:

			# print(f"{move}: {len(board.getAllMoves())}")
			board.makeMove(move)
			iterEval = -self.search(self.maxDepth-1, board, -(2**31), (2**31))
			board.undoMove()
			board.fen.future = []


			if bestEval < iterEval:
				bestEval = iterEval
				bestMove = move

		

		endTime = time.time()

		print(endTime - startTime)
		return bestMove
	
	def search(self, depth, board :Board, alpha :int, beta :int) -> int:
		if depth == 0:
			return board.evalBoard()

		allMoves = board.getAllMoves()


		kingPos = board.kingMap[board.fen.colorToMove]
	
		if len(allMoves) == 0:
			if board.isSquareCovered(kingPos, board.fen.colorToMove)[0]:
				return -(2**31)
			return 0

		for move in allMoves:
			board.makeMove(move)
			eval = -self.search(depth-1, board, -beta, -alpha)
			board.undoMove()
			board.fen.future = []


			if eval >= beta:
				return beta
			alpha = max(alpha, eval)

		return alpha
	
	def evalBoard(self, board :Board):
		return board.evalBoard()