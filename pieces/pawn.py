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
		king = board.kingDict[self.color]
		kingPos = king.getPos(board)
		inCheck, pins, checks = king.getChecksandPins(board, king.getPos(board))

		piecePinned = False
		# print(pins)
		for x in range(len(pins)-1, -1, -1):
			# print(pins[x][0])
			# print(pins[x][1])
			# print()
			if pins[x][0] == i and pins[x][1] == j:
				# print(f"pin found, {i, j}")
				piecePinned = True
				# print(piecePinned)
				pinDirection = (pins[x][2], pins[x][3])
				pins.remove(pins[x])
				# pins.pop(x)
				break

		# Advancement moves
		# print(piecePinned)
		# print(self.directions[0])
		# print(self.directions[1])
		# print(self.directions[2])

		x = self.forward[0]
		y = self.forward[1]
		endPos = position + (8*y + x)
		space = board.getSpace(endPos)
		if not (piecePinned and self.directions[0] != pinDirection) and self.moveInbounds(*self.getXY(position), self.directions[0], 1) and space == "--":
			availableMoves.append(Move(board, self, space, position, endPos))
		
		posX, posY = self.getXY(position)

		x = self.forward[0]
		y = self.forward[1] * 2
		endPos = position + (8*y + x)
		if not (piecePinned and self.directions[0] != pinDirection) and posY == int(self.forward[1] * (-2.5) + 3.5) and board.getSpace(endPos) == "--" and board.getSpace(endPos-8 * self.forward[1]) == "--":
			availableMoves.append(Move(board, self, space, position, endPos))
		
			

		# Attacking moves
		if not (piecePinned and self.directions[1] != pinDirection) and self.moveInbounds(*self.getXY(position), self.directions[1], 1):
			x = self.directions[1][0]
			y = self.directions[1][1]
			endPos = position + (8*y + x)
			space = board.getSpace(endPos)

			if space != "--" and space.color != self.color:
				availableMoves.append(Move(board, self, space, position, endPos))
			
			
			if endPos == board.fen.getEnPassantPos():
				space = board.getSpace(endPos - self.forward[1] * 8)
				availableMoves.append(EnPassant(board, self, space, position, endPos))

		if not (piecePinned and self.directions[2] != pinDirection) and self.moveInbounds(*self.getXY(position), self.directions[2], 1):
			x = self.directions[2][0]
			y = self.directions[2][1]
			endPos = position + (8*y + x)
			space = board.getSpace(endPos)

			if space != "--" and space.color != self.color:
				availableMoves.append(Move(board, self, space, position, endPos))
			
			if endPos == board.fen.getEnPassantPos():
				space = board.getSpace(endPos - self.forward[1] * 8)
				availableMoves.append(EnPassant(board, self, space, position, endPos))
		

		# print("cum")
		board.refreshChecksandPins()
		self.removeInvalidMoves(board, availableMoves, king.getChecksandPins(board, king.getPos(board)) + (king.getPos(board),))

		return availableMoves

	def getAttackingMoves(self, board, position) -> list[Move]:
		availableMoves = []

		i, j = self.getXY(position)
		pinDirection = ()

		board.refreshChecksandPins()
		king = board.kingDict[self.color]
		inCheck, pins, checks, kingPos = board.infoDict[self.color]

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
		
			availableMoves.append(Move(board, self, space, position, endPos))
		

		if self.moveInbounds(*self.getXY(position), self.directions[2], 1):
			x = self.forward[0] + 1
			y = self.forward[1]
			endPos = position + (8*y + x)
			space = board.getSpace(endPos)
			
			availableMoves.append(Move(board, self, space, position, endPos))

		return availableMoves
