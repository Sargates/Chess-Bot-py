from .piece import Piece
from .move import *

class King(Piece):
	def __init__(self, color) -> None:
		super().__init__(color)
		self.directions = [(-1, 0), (0, 1), (1, 0), (0, -1), (-1, -1), (1, -1), (-1, 1), (1, 1)]
		self.moveDepths = [1]
		self.type = "K"
		self.ID = color + self.type
		self.inCheck = False
	
	def getMoves(self, board, position) -> list[Move]:
		availableMoves = []

		x, y = self.getXY(position)

		enemyMoves = []
		for i in range(len(board.board)):
			if board.board[i] == "--" or board.board[i].color == self.color:
				continue

			if board.board[i].type == "K":
				continue

			for move in board.board[i].getAttackingMoves(board, i):
				if not move in enemyMoves:
					enemyMoves.append(move)

		
		
		takenSquares = {enemyMoves[x].endPos for x in range(len(enemyMoves))}
		takenSquares = sorted(list(takenSquares))

		for move in enemyMoves:
			print(move)

		for direction in self.directions:
			for depth in self.moveDepths:
				if not self.moveInbounds(*self.getXY(position), direction, 1):
					break

				x = direction[0]
				y = direction[1]

				endPos = position + (8*y + x)
				space = board.getSpace(endPos)

				# print(endPos)

				if endPos in takenSquares:
					continue

				if space == "--":
					availableMoves.append(Move(self, space, position, endPos))
					continue
				
				if space.color != self.color:
					availableMoves.append(Move(self, space, position, endPos))
				break

		return availableMoves

	def getPos(self, b):
		for i in range(len(b.board)):
			piece = b.board[i]
			if piece == self:
				return i
	
	def getChecksandPins(self, board, position):
		pins = []
		checks = []
		inCheck = False

		directions = ((0, -1), (1, 0), (0, 1), (-1, 0), (1, 1), (1, -1), (-1, -1), (-1, 1))

		for j in range(len(directions)):
			dir = directions[j]
			possiblePin = ()
			for i in range(1, 8):
				endPos = self.getXY(position + (dir[1] * 8 + dir[0]) * i)
				if not self.moveInbounds(*self.getXY(position), dir, i):
					break
				endSpace = board.getSpace(position + (dir[1] * 8 + dir[0]) * i)
				if endSpace == "--":
					continue
				if endSpace.color == self.color and endSpace.type != 'K':
					if possiblePin == ():
						possiblePin = (endPos[0], endPos[1], dir[0], dir[1])
						# print("Possible Pin")
						# print(possiblePin)
					else:
						break
				elif endSpace.color != self.color:
					type = endSpace.type
					# 5 possibilities here in this complex conditional
					# 1. orthoganally away from king and piece is rook
					# 2. diagonally away from king and piece is bishop
					# 3. 1 square away diagonally from king and piece is a pawn
					# 4. any direction and piece is a queen
					# 5. anydirection 1 square away and piece is a king( this is necessary to prevent a king move to a square controlled by another king)
					if (0 <= j <= 3 and type == 'R') or \
							(4 <= j <= 7 and type == 'B') or \
							(i == 1 and type == 'p' and ((self.color != 'w' and 6 <= j <= 7) or (self.color == 'b' and 4 <= j <= 5))) or \
							(type == 'Q') or (i == 1 and type == 'K'):
						if possiblePin == (): # no piece blocking, so check the king
							inCheck = True
							checks.append((endPos[0], endPos[1], dir[0], dir[1]))
							# print("CHECK APPENED VVV")
							# print(checks)
							break
						else: # pinned piece blocking check
							pins.append(possiblePin)
							# print("PIN APPENED VVV")
							# print(pins)
							break
					else:
						break

		knightMoves = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2,-1), (2, 1))
		for m in knightMoves:
			endPos = self.getXY(position + (m[1] * 8 + m[0]))
			if self.moveInbounds(*self.getXY(position), m, i):
				endPiece = board.getSpace(position + (m[1] * 8 + m[0]))
				if endPiece == "--":
					continue
				if endPiece.color != self.color and endPiece.type == "N":
					inCheck = True
					checks.append((endPos[0], endPos[1], m[0], m[1]))
			else:
				break
					
		# print("End of pin check")
		return inCheck, pins, checks