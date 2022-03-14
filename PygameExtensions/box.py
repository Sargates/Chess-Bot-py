import pygame
from pygame import Vector2

class Box:
	def __init__(self, 
			rect :pygame.Rect, 
			color :pygame.Color=pygame.Color(64, 64, 64),
			image :pygame.Surface=None,
			isDraggable :bool=True,
			action=None,
			args :tuple=(),
			) -> None:
		self.rect = rect
		self.color = color
		self.image = image

		alpha = 255 if len(color) < 4 else color[3]

		self.highLightColor = (255/2 + color[0]/2, 255/2 + color[1]/2, 255/2 + color[2]/2, 255/2 + alpha/2)
		self.defaultColor = color

		self.isDragging = False
		self.anchorDelta = Vector2(self.rect.x, self.rect.y)

		self.isDraggable = isDraggable
		self.action = action
		self.args = args

		self.isClicked = False
	
	def __eq__(self, __o: object) -> bool:
		if not self.image == __o.image:
			return False
		
		if not self.action == __o.action:
			return False
		
		if not self.color == __o.color:
			return False
		
		if not self.rect == __o.rect:
			return False
		
		return True

	def __str__(self) -> str:
		return f"Box of size {self.rect.width, self.rect.height} positioned at {self.rect.x, self.rect.y}"
	
	def checkDragging(self):
		currentPos = pygame.mouse.get_pos()
		newPos = Vector2(currentPos) + self.anchorDelta
		self.rect.x = newPos.x
		self.rect.y = newPos.y

	def render(self, screen :pygame.Surface, isChild=False):
		mouseButtons = pygame.mouse.get_pressed()

		if self.hoveringOver() and mouseButtons[0] and not self.isClicked:
			self.isClicked = True

			if self.action != None:
				self.action(*self.args)

			if self.isDraggable:
				anchorPos = Vector2(pygame.mouse.get_pos())
				pos = Vector2(self.rect.x, self.rect.y)
				self.anchorDelta = pos-anchorPos
				self.isDragging = True

		if not mouseButtons[0]:
			self.isDragging = False
			self.isClicked = False
			self.anchorDelta = Vector2(self.rect.x, self.rect.y)
			

		if self.isDragging:
			self.checkDragging()

		if not isChild:
			pygame.draw.rect(screen, self.color, self.rect)
			if self.image != None:
				screen.blit(self.image, self.rect)

	def hoveringOver(self) -> bool:
		# 1 = left click
		# 2 = middle click
		# 3 = right click
		self.color = self.defaultColor

		x, y = pygame.mouse.get_pos()

		if 0 <= x - self.rect.x <= self.rect.width and 0 <= y - self.rect.y <= self.rect.height:
			self.color = self.highLightColor
			return True
		
		return False
	
	def setImage(self, image :pygame.Surface):
		self.image = image
	
	def setAction(self, method):
		self.action = method
	
	def setArgs(self, args):
		self.args = args