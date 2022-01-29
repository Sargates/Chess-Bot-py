from .piece import Piece

class Knight(Piece):
	def __init__(self, color) -> None:
		super().__init__(color)
		self.directions = [(-2, 1), (-1, 2), (1, 2), (2, 1), (2, -1), (1, -2), (-1, -2), (-2, -1)]
		self.moveDepths = [1]
		self.type = "N"
		self.ID = color + self.type
