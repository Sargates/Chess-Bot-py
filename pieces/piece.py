from tabnanny import check
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

	def __str__(self) -> str:
		return self.ID
	
	def getXY(self, position):
		return (position % 8, position // 8)
	
	def removeInvalidMoves(self, board, moves :list(Move), kingInfo :tuple(int)):
		inCheck, pins, checks, kingPos = kingInfo
		if not inCheck:
			return
		
		
		if len(checks) == 1:
			check = checks[0]
			# if crashing come back here
			# not checking if move is valid
			direction = check[3] * 8 + check[2]
			endPos = check[1] * 8 + check[0]
			i = 0

			requiredSquares = []
			while kingPos + direction * i != endPos + direction:
				requiredSquares.append(kingPos + direction * i)
				i += 1
			
			for move in moves:
				if not move.endPos in requiredSquares:
					moves.remove(move)
		else:
			moves = []


	
	def getMoves(self, board, position) -> list[Move]:
		availableMoves = []

		x, y = self.getXY(position)
		print(position)
		pinDirection = ()

		board.refreshChecksandPins()
		king = board.kingDict[self.color]
		inCheck, pins, checks, kingPos = board.infoDict[self.color]
		piecePinned = False
		for x in range(len(pins)-1, -1, -1):
			print(pins[x])
			print(x, y)
			if pins[x][0] == x and pins[x][1] == y:
				piecePinned = True
				pinDirection = (pins[x][2], pins[x][3])
				board.whiteInfo[1].remove(pins[x])
				print("pin found")
				print(pins[x])
				# pins.pop(x)
				break


		print(f"piecePinned = {piecePinned}")
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
					availableMoves.append(Move(self, space, position, endPos))
					continue
				
				if space.color != self.color:
					availableMoves.append(Move(self, space, position, endPos))
				break
		
		# check if in check
		
		
			self.removeInvalidMoves(board, availableMoves, board.infoDict[self.color])

		return availableMoves

	def getAttackingMoves(self, board, position) -> list[Move]:
		return self.getMoves(board, position)

	def moveInbounds(self, x, y, direction, depth):
		temp = direction[0] * depth
		newX = x + temp
		newY = y + direction[1] * depth

		if not (0 <= newX < 8):
			return False

		if not (0 <= newY < 8):
			return False
		
		
		
		return True

