from .piece import Piece
from .move import *

class Pawn(Piece):

	def __init__(self, color) -> None:
		super().__init__(color)
		self.forward = (0, -1) if color == "w" else (0, 1)
		self.directions = (self.forward, (self.forward[0]-1, self.forward[1]), (self.forward[0]+1, self.forward[1]))
		self.type = "p"
		self.ID = color + self.type
		self.enPassant = False
	
	def getMoves(self, board, position, ):
		availableMoves = []

		i, j = self.getXY(position)
		pinDirection = ()

		board.refreshChecksandPins()
		pins = board.infoDict[self.color][1]
		piecePinned = False
		# print(i, j)
		for x in range(len(pins)-1, -1, -1):
			# print(pins[x][0])
			# print(pins[x][1])
			# print()
			if pins[x][0] == i and pins[x][1] == j:
				# print(f"pin found, {i, j}")
				piecePinned = True
				# print(piecePinned)
				pinDirection = (pins[x][2], pins[x][3])
				board.whiteInfo[1].remove(pins[x])
				# pins.pop(x)
				break

		# Advancement moves
		x = self.forward[0]
		y = self.forward[1]
		endPos = position + (8*y + x)
		space = board.getSpace(endPos)
		# print(piecePinned)
		# print(self.directions[0])
		# print(self.directions[1])
		# print(self.directions[2])

		if not (piecePinned and self.directions[0] != pinDirection) and self.moveInbounds(*self.getXY(position), self.directions[0], 1) and space == "--":
			availableMoves.append(Move(self, space, position, endPos))
		
			x = self.forward[0] * 2
			y = self.forward[1] * 2
			endPos = position + (8*y + x)
			space = board.getSpace(endPos)
			if self.timesMoved == 0 and space == "--":
				availableMoves.append(Move(self, space, position, endPos))

		# Attacking moves
		if not (piecePinned and self.directions[1] != pinDirection) and self.moveInbounds(*self.getXY(position), self.directions[1], 1):
			x = self.forward[0] - 1
			y = self.forward[1]
			endPos = position + (8*y + x)
			space = board.getSpace(endPos)

			if space != "--" and space.color != self.color:
				availableMoves.append(Move(self, space, position, endPos))
		

		if not (piecePinned and self.directions[2] != pinDirection) and self.moveInbounds(*self.getXY(position), self.directions[2], 1):
			x = self.forward[0] + 1
			y = self.forward[1]
			endPos = position + (8*y + x)
			space = board.getSpace(endPos)

			if space != "--" and space.color != self.color:
				availableMoves.append(Move(self, space, position, endPos))
		

		return availableMoves

	def getAttackingMoves(self, board, position) -> list[Move]:
		availableMoves = []

		i, j = self.getXY(position)
		pinDirection = ()

		board.refreshChecksandPins()
		pins = board.whiteInfo[1]
		piecePinned = False
		# print(i, j)
		for x in range(len(pins)-1, -1, -1):
			# print(pins[x][0])
			# print(pins[x][1])
			# print()
			if pins[x][0] == i and pins[x][1] == j:
				# print(f"pin found, {i, j}")
				piecePinned = True
				# print(piecePinned)
				pinDirection = (pins[x][2], pins[x][3])
				board.whiteInfo[1].remove(pins[x])
				# pins.pop(x)
				break

		# Advancement moves
		x = self.forward[0]
		y = self.forward[1]
		endPos = position + (8*y + x)
		space = board.getSpace(endPos)
		
		if self.moveInbounds(*self.getXY(position), self.directions[1], 1):
			x = self.forward[0] - 1
			y = self.forward[1]
			endPos = position + (8*y + x)
			space = board.getSpace(endPos)
		
			availableMoves.append(Move(self, space, position, endPos))
		

		if self.moveInbounds(*self.getXY(position), self.directions[2], 1):
			x = self.forward[0] + 1
			y = self.forward[1]
			endPos = position + (8*y + x)
			space = board.getSpace(endPos)
			
			availableMoves.append(Move(self, space, position, endPos))

		return availableMoves
