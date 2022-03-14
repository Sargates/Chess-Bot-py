import pygame
from pygame import Vector2
from .box import Box

class Slider:


	def __init__(self, object :object, variable :str, width :float, height :float, position :Vector2, minValue :float, maxValue :float) -> None:
		self.object = object
		self.variable = variable

		self.width = width
		self.height = height
		self.position = position
		self.minValue = minValue
		self.maxValue = maxValue

		self.progress = 0.5

		sBoxW = max(10, width/40)
		sBoxH = height/1.5
		sBoxX = self.position.x + (width - sBoxW) * self.progress
		sBoxY = self.position.y + (height - sBoxH)

		self.sliderBox = Box(sBoxW, sBoxH, Vector2(sBoxX, sBoxY), (128, 128, 128))

		self.sBarW = width
		self.sBarH = min(4, height/15)
		self.sBarX = self.position.x 
		self.sBarY = self.position.y + (height/2) - (self.sBarH/2)

	def slide(self):
		a = self.position.x
		b = self.position.x + self.width
		
		if self.sliderBox.position.x < a:
			self.sliderBox.position.x = a
		if b < self.sliderBox.position.x:
			self.sliderBox.position.x = b
			

		p = (self.sliderBox.position.x - a) / (b - a)

		self.progress = p

		self.sliderBox.position.y = self.position.y + (self.height - self.sliderBox.b)/2

		self.object.__dict__[self.variable] = self.progress * (self.maxValue - self.minValue)

	def render(self, screen :pygame.Surface):
		self.sliderBox.render(screen, True)
		self.slide()
		pygame.draw.rect(screen, (32,32,32), (self.sBarX, self.sBarY, self.sBarW, self.sBarH))
		pygame.draw.rect(screen, self.sliderBox.color, (self.sliderBox.position.x, self.sliderBox.position.y, self.sliderBox.a, self.sliderBox.b))
	
	def changeValue(self, value):
		self.object.__dict__[self.variable] = value