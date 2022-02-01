from .move import *

class Piece:
	def __init__(self, color) -> None:
		self.ID = ""
		self.timesMoved = 0
		self.color = color
		self.moveDepths = []
		self.directions = []
		self.pinDirection = ()
		self.type = ""
		self.lastMoves = []

	def __str__(self) -> str:
		return self.ID
	
	def getXY(self, position):
		return (position % 8, position // 8)
	
	def removeInvalidMoves(self, board, moves :list[Move], kingInfo):
		inCheck, pins, checks, kingPos = kingInfo

		if inCheck ^ bool(len(checks)):
			print("inCheck and len(checks) desync")
		if not inCheck:
			return

		requiredSquares = []
		if len(checks) == 0:
			return

		if len(checks) == 1:
			check = checks[0]
			# if crashing come back here
			# not checking if move is valid
			direction = check[3] * 8 + check[2]
			endPos = check[1] * 8 + check[0]
			i = 1


			while kingPos + direction * i != endPos + direction:
				requiredSquares.append(kingPos + direction * i)
				i += 1
			
			# print(requiredSquares)
			# print([str(move) for move in moves])
			for i in range(len(moves)-1, -1, -1):
				move = moves[i]

				# print(move)
				# print(move.endPos in requiredSquares)
				# print((move.pieceMoved.type == "K" and move.endPos in [m.endPos for m in self.getEnemyMoves(board)]))
				if not move.endPos in requiredSquares or (move.pieceMoved.type == "K" and move.endPos in [m.endPos for m in self.getEnemyMoves(board)]):
					# print("\t", move)
					moves.pop(i)
					continue
		else:
			moves = []
	
	def getMoves(self, board, position, attacking=False) -> list[Move]:
		availableMoves = []

		i, j = self.getXY(position)
		# print(position)
		pinDirection = ()

		# board.refreshChecksandPins()
		king = board.kingDict[self.color]
		inCheck, pins, checks, kingPos = king.getChecksandPins(board, king.getPos(board)) + (king.getPos(board),)
		piecePinned = False
		for x in range(len(pins)-1, -1, -1):
			# print(pins[x])
			# print(i, j)
			if pins[x][0] == i and pins[x][1] == j:
				piecePinned = True
				pinDirection = (pins[x][2], pins[x][3])
				# print("pin found")
				# print(pins[x])
				# pins.remove(pins[x])
				pins.pop(x)
				break


		# print(f"piecePinned = {piecePinned}")
		for direction in self.directions:
			# print(f"direction == pinDirection = {direction == pinDirection}")
			if piecePinned and direction != pinDirection:
				continue

			for depth in self.moveDepths:
				if not self.moveInbounds(*self.getXY(position), direction, depth):
					break

				x = direction[0] * depth
				y = direction[1] * depth

				endPos = position + (8*y + x)
				space = board.getSpace(endPos)
				if space == "--":
					availableMoves.append(Move(board, self, space, position, endPos))
					continue
				
				if space.color != self.color:
					availableMoves.append(Move(board, self, space, position, endPos))
					break
				
				if attacking:
					availableMoves.append(Move(board, self, space, position, endPos))
					break
				break
		
		# check if in check
		if not attacking:
			board.refreshChecksandPins()
			self.removeInvalidMoves(board, availableMoves, king.getChecksandPins(board, king.getPos(board)) + (king.getPos(board),))

		return availableMoves

	def getAttackingMoves(self, board, position) -> list[Move]:
		return self.getMoves(board, position, True)

	def moveInbounds(self, x, y, direction, depth):
		temp = direction[0] * depth
		newX = x + temp
		newY = y + direction[1] * depth

		if not (0 <= newX < 8):
			return False

		if not (0 <= newY < 8):
			return False
		
		
		
		return True

