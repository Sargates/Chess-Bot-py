from .piece import Piece

class Bishop(Piece):
	def __init__(self, color) -> None:
		super().__init__(color)
		self.moveDepths = [x for x in range(1, 8)]
		self.directions = [(-1, -1), (1, -1), (-1, 1), (1, 1)]
		self.type = "B"
		self.ID = color + self.type