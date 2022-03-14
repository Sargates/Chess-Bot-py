import pygame

class RenderPipeline:
	pipeline = []
	methods = []
	screen = None

	@staticmethod
	def setScreen(s :pygame.Surface):
		RenderPipeline.screen = s
	
	@staticmethod
	def renderAssets():
		for object in RenderPipeline.pipeline:
			object.render(RenderPipeline.screen)
	
	@staticmethod
	def execRenderMethods():
		for tuple in RenderPipeline.methods:
			method = tuple[0]
			if len(tuple) == 1:
				method()
				continue
			method(*tuple[1:])

	@staticmethod
	def addAsset(object):
		if not object in RenderPipeline.pipeline:
			RenderPipeline.pipeline.append(object)
			print(f"Added method: {object}")
			return
		
		print(f"Failed to add: {object}")
	
	@staticmethod
	def removeAsset(object):
		if not object in RenderPipeline.pipeline:
			print(f"Failed to remove: {object}")
			return
		
		RenderPipeline.pipeline.pop(RenderPipeline.pipeline.index(object))
		print(f"Removed object: {object}")
	
	@staticmethod
	def addMethod(*method):
		if not method in RenderPipeline.methods:
			RenderPipeline.methods.append(method)
			print(f"Added method: {method}")
			return
		
		print(f"Failed to add: {method}")
	
	@staticmethod
	def removeMethod(method):
		for m in RenderPipeline.methods:
			if m[0] == method:
				RenderPipeline.methods.pop(RenderPipeline.methods.index(m))
				print(f"Removed method: {m}")
				break
		else:
			print(f"Failed to remove: {method}")
			return