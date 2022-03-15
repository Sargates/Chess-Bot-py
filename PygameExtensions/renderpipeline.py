import pygame

class RenderPipeline:
	pipeline = []
	methods = []
	screen = None
	printMessages = True

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
			jflkadsjflskd = print(f"Added method: {object}") if RenderPipeline.printMessages else None
			return
		
		jflkadsjflskd = print(f"Failed to add: {object}") if RenderPipeline.printMessages else None
	
	@staticmethod
	def removeAsset(object):
		if not object in RenderPipeline.pipeline:
			jflkadsjflskd = print(f"Failed to remove: {object}") if RenderPipeline.printMessages else None
			return
		
		RenderPipeline.pipeline.pop(RenderPipeline.pipeline.index(object))
		jflkadsjflskd = print(f"Removed object: {object}") if RenderPipeline.printMessages else None
	
	@staticmethod
	def addMethod(*method):
		if not method in RenderPipeline.methods:
			RenderPipeline.methods.append(method)
			jflkadsjflskd = print(f"Added method: {method}") if RenderPipeline.printMessages else None
			return
		
		jflkadsjflskd = print(f"Failed to add: {method}") if RenderPipeline.printMessages else None
	
	@staticmethod
	def removeMethod(method):
		for m in RenderPipeline.methods:
			if m[0] == method:
				RenderPipeline.methods.pop(RenderPipeline.methods.index(m))
				jflkadsjflskd = print(f"Removed method: {m}") if RenderPipeline.printMessages else None
				break
		else:
			jflkadsjflskd = print(f"Failed to remove: {method}") if RenderPipeline.printMessages else None
			return