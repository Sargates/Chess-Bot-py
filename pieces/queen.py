from .piece import Piece

class Queen(Piece):
	def __init__(self, color) -> None:
		super().__init__(color)
		self.type = "Q"
		self.ID = color + self.type
		self.moveDepths = [x for x in range(1, 8)]
		self.directions = [(-1, 0), (0, 1), (1, 0), (0, -1), (-1, -1), (1, -1), (-1, 1), (1, 1)]
