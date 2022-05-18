import pygame, threading
from PygameExtensions import *
from board import Board
from move import Move
from AI import AI

WIDTH = HEIGHT = 768
WINDOWSIZE = (WIDTH, HEIGHT)
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("The cool")
SQ_SIZE = ((256 - 80)/8) * (WIDTH/256)
OFFSET = 40 * (WIDTH/256)
PIECE_OFFSET = (10/11) * SQ_SIZE / 2

exitEvent = threading.Event()
aiRunning = threading.Event()


board = Board()
ai = AI()

pygame.init()


def getPosToIndex(x, y):
	newX = (x - 40 * (WIDTH//256)) // (22 * (WIDTH//256))
	newY = (y - 40 * (WIDTH//256)) // (22 * (WIDTH//256))
	
	if (0 <= newX < 8 and 0 <= newY < 8):
		return newX + newY * 8
	
	return -1

def getIndexToPos(pos):
	x = (pos%8)  * 22 * WIDTH/256 + 40 *(WIDTH/256)
	y = (pos//8) * 22 * WIDTH/256 + 40 *(WIDTH/256)
	
	x += SQ_SIZE/2
	y += SQ_SIZE/2

	return (x, y)

def renderBoard(b :Board):
	SCREEN.blit(pygame.transform.scale(b.boardImage, (HEIGHT, HEIGHT)), ((WIDTH/2)-(HEIGHT/2), 0))

def printBoard(board :list[str]):
	string = ""

	for i in range(64):
		if (i % 8) == 0:
			string += "\n"

		string += board[i] + " "

	
	return string

def renderPieces(b :Board):
	# print("penis")
	# if b.aiInProgress:
	# 	return

	for i in range(len(b.publicBoard)):
		space = b.publicBoard[i]
		# print(j, i, "", space)
		# if space == "":
		# 	print(i)
		# 	print("SPACE == \"\"")
		# 	for move in board.moveHistory.copy():
		# 		print(move)

		# 	print(printBoard(b.publicBoard.copy()))

		# 	for piece in b.pieceLocationSet.copy():
		# 		print(piece)
		if space != "--":
			SCREEN.blit((b.images[b.idToIndex[space]]), (OFFSET + (i%8*SQ_SIZE)+SQ_SIZE/2 - PIECE_OFFSET, OFFSET + (i//8*SQ_SIZE)+SQ_SIZE/2 - PIECE_OFFSET))

def renderHighlighted(b :Board):
	highlightedScreen = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
	for index in b.highlightedSquares:
		x, y = getIndexToPos(index)
		square = pygame.Rect(x-SQ_SIZE/2, y-SQ_SIZE/2, SQ_SIZE, SQ_SIZE)

		pygame.draw.rect(highlightedScreen, (255, 0, 0, 100), square, 0)
	
	SCREEN.blit(highlightedScreen, (0, 0))

def renderMoves(b :Board):
	if b.selectedIndex != None:
		piece = b.getSpace(b.selectedIndex)
		if piece == "--":
			b.selectedIndex = None
			return

		for move in b.selectedMoves:
			pygame.draw.circle(SCREEN, (255, 0, 0), getIndexToPos(move.endPos), SQ_SIZE/5)

def renderSelected(b :Board):
	if b.selectedIndex != None:
		x, y = getIndexToPos(b.selectedIndex)
		square = pygame.Rect(x-SQ_SIZE/2, y-SQ_SIZE/2, SQ_SIZE, SQ_SIZE)
		pygame.draw.rect(SCREEN, (255, 0, 0), square, 2)

def render():

	while True:
		if exitEvent.is_set():
			break
		
		SCREEN.fill((255, 255, 255))
		
		RenderPipeline.execRenderMethods()
		RenderPipeline.renderAssets()

		pygame.display.update()

def handleAI():
	while True:
		if not aiRunning.is_set():
			continue


		# moveLists = {}
		# for k, v in ai.depthList.items():
		# 	moveLists[k] = []
		# 	ai.depthList[k] = ai.getTotalMoves(k, board, k, moveLists[k])
		# 	print(f"{k}\t{ai.depthList[k]}")
		
		allMoves = ai.getMove(board)
		board.makeMove(allMoves)
		board.resetPublicBoard()

		aiRunning.clear()
		print("aiRunning = False")



def main():


	run = True
	RenderPipeline.printMessages = False

	RenderPipeline.setScreen(SCREEN)
	RenderPipeline.addMethod(renderBoard, board)
	RenderPipeline.addMethod(renderHighlighted, board)
	RenderPipeline.addMethod(renderSelected, board)
	RenderPipeline.addMethod(renderPieces, board)
	RenderPipeline.addMethod(renderMoves, board)

	useAI = [bool(0)]

	def cum(list, index):
		list[index] = not list[index]

	RenderPipeline.addAsset(Box(pygame.Rect(678, 678, 60, 60), color=(255, 0, 0), isDraggable=False, action=cum, args=(useAI, 0)))

	renderThread = threading.Thread(target=render, name="Render Thread")
	renderThread.start()

	aiThread = threading.Thread(target=handleAI, name="AI Thread")
	aiThread.start()



	while run:
		mousePos = pygame.mouse.get_pos()

		for e in pygame.event.get():
			if e.type == pygame.QUIT:
				exitEvent.set()
				renderThread.join()
				aiThread.join()
				pygame.quit()
				quit()
			if e.type == pygame.MOUSEBUTTONDOWN:
				index = getPosToIndex(*mousePos)
				# print(index)
				board.resetPublicBoard()
				if board.waitingOnPromotion:
					continue

				if (index != -1):
					if e.button == 1: # left click
						board.highlightedSquares = set()
						board.selectionLogic(index)
						# board.pieceLocationSet



					if e.button == 3: # right click
						if not index in board.highlightedSquares:
							board.highlightedSquares.add(index)
							print(f"  Highlighted Index {index}")
						else:
							board.highlightedSquares.remove(index)
							print(f"Unhighlighted Index {index}")
						
			if e.type == pygame.KEYDOWN:
				if e.key == pygame.K_z and len(board.moveHistory) > 0:
					board.undoMove()
					# board.undoMove()


					board.fen.refreshBoard(board.board)
					board.resetPublicBoard()

				elif e.key == pygame.K_y and len(board.moveFuture) > 0:
					board.makeMove(board.moveFuture.pop(-1))
					# board.makeMove(board.moveFuture.pop(-1))
					# board.fen.redo()
					board.fen.redo()

					board.fen.refreshBoard(board.board)
					board.resetPublicBoard()

				elif e.key == pygame.K_v: # debug hotkey

					print(useAI)

					# aiMove = ai.getMove(board)

					# board.makeMove(aiMove)

					# board.resetPublicBoard()

					# allMoves = board.getAllMoves()

					# for move in allMoves:
					# 	print(move)


					# moveLists = {}
					# for k, v in ai.depthList.items():
					# 	moveLists[k] = []
					# 	ai.depthList[k] = ai.getTotalMoves(k, board, k, moveLists[k])
					# 	print(f"{k}\t{ai.depthList[k]}")
					# aiRunning.set()

					# print()

					# aiMove = ai.getMove(board)
					# board.makeMove(aiMove)
					# print(f"Move made, {aiMove}")
					# board.resetPublicBoard()



					# for string in board.fen.history:
					# 	print(string)
					# print()

					print(f"Current FEN String\n{board.fen.getFenString(board.board)}")

		if useAI[0] and board.fen.colorToMove == "b" and not aiRunning.is_set():
			aiRunning.set()
			print("aiRunning = True")


		

		# render(board)
			


main()