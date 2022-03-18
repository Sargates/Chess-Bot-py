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

	def __init__(self) -> None:
		self.totalMoves = 0
		self.maxDepth = 4
		self.depthList = {x: 0 for x in range(5)}
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
			# if move.pieceTaken[1] == "K":
			# 	# print(move)
			# 	print("Move caused fatal error 1")
			# 	break

			# if move.pieceTaken[1] == "":
			# 	print(move)
			# 	print("Move caused fatal error 2")
			# 	break

			# if type(move) == Move:
			# 	print(move, "i like penis 1")
			# if type(move) == Promotion:
			# 	print(move, "i like penis 2")
			# if type(move) == Castle:
			# 	print(move, "i like penis 3")
			# if type(move) == EnPassant:
			# 	print(move, "i like penis 4")

			board.makeMove(move)
			moveList.append((m-depth)*"\t" + chessMove)

			# print((m-depth)*"\t" + chessMove)
			oneStepDeep = self.getTotalMoves(depth-1, board, m, moveList)

			

			numPositions += oneStepDeep
			# print(f"{m}\t{numPositions}", end="\r")
			

			board.undoMove()

		if m - depth == 0:
			endTime = time.time()
			print(f"Depth {depth}: {endTime - startTime}")

		return numPositions

	def getMove(self, board :Board) -> Move:
		startTime = time.time()
		self.totalMoves = 0
		allMoves = board.getAllMoves()

		bestMove = None
		bestEval = -(2**31)

		# kingPos = board.kingMap[board.fen.colorToMove]
		# print(len(allMoves))

		for move in allMoves:
			# print(board.fen.getChessMove(move))
			# print(move.pieceMoved)
			board.makeMove(move)

			# print(f"{move}: {1}")
			iterEval = -self.search(self.maxDepth-1, board)

			if bestEval < iterEval:
				bestEval = iterEval
				bestMove = move
				

			board.undoMove()
		

		endTime = time.time()

		print(endTime - startTime)
		return bestMove
	
	def search(self, depth, board :Board) -> int:
		if depth == 0:
			return board.evalBoard()

		allMoves = board.getAllMoves()


	
		if len(allMoves) == 0:
			return -(2**31)

		kingPos = board.kingMap[board.fen.colorToMove]
		
		# if depth == self.maxDepth - 1:
		# 	print(kingPos, board.getSpace(kingPos))
		
		if board.isSquareCovered(kingPos, board.fen.colorToMove)[0]:
			return -(2**31)+1

		eval = -(2**31)


		for move in allMoves:
			board.makeMove(move)


			tabDepth = (self.maxDepth-depth)*'\t'
			# frafarsfesf = print(f"{tabDepth}{move}: {self.maxDepth-depth+1}") if depth > self.maxDepth - 2 else None
			eval = max(eval, -self.search(depth-1, board))
			# print(f"{move}\t{eval}", end="\n")

			board.undoMove()


		return eval
	
	def evalBoard(self, board :Board):
		return board.evalBoard()