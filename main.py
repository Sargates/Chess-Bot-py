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


board = Board()
ai = AI()

pygame.init()


def getPosToIndex(x, y):
	newX = (x - 40 * (WIDTH//256)) // (22 * (WIDTH//256))
	newY = (y - 40 * (WIDTH//256)) // (22 * (WIDTH//256))
	
	if (0 <= newX < 8 and 0 <= newY < 8):
		return (newX, newY)
	
	return -1

def getIndexToPos(x1, y1):
	x = (x1)  * 22 * WIDTH/256 + 40 *(WIDTH/256)
	y = (y1) * 22 * WIDTH/256 + 40 *(WIDTH/256)
	
	x += SQ_SIZE/2
	y += SQ_SIZE/2

	return (x, y)

def renderBoard(b :Board):
	SCREEN.blit(pygame.transform.scale(b.boardImage, (HEIGHT, HEIGHT)), ((WIDTH/2)-(HEIGHT/2), 0))

def renderPieces(b :Board):
	# if b.aiInProgress:
	# 	return

	for i in range(len(b.publicBoard)):
		for j in range(len(b.publicBoard[i])):
			space = b.publicBoard[i][j]
			# print(j, i, "", space)
			if space != "--":
				xPosition = j
				yPosition = i
				SCREEN.blit((b.images[b.idToIndex[space]]), (OFFSET + (xPosition*SQ_SIZE)+SQ_SIZE/2 - PIECE_OFFSET, OFFSET + (yPosition*SQ_SIZE)+SQ_SIZE/2 - PIECE_OFFSET))

def renderHighlighted(b :Board):
	highlightedScreen = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
	for index in b.highlightedSquares:
		x, y = getIndexToPos(*index)
		square = pygame.Rect(x-SQ_SIZE/2, y-SQ_SIZE/2, SQ_SIZE, SQ_SIZE)

		pygame.draw.rect(highlightedScreen, (255, 0, 0, 100), square, 0)
	
	SCREEN.blit(highlightedScreen, (0, 0))

def renderMoves(b :Board):
	if b.selectedIndex != None:
		piece = b.getSpace(*b.selectedIndex)
		if piece == "--":
			b.selectedIndex = None
			return

		for move in b.selectedMoves:
			pygame.draw.circle(SCREEN, (255, 0, 0), getIndexToPos(*move.endPos), SQ_SIZE/5)

def renderSelected(b :Board):
	if b.selectedIndex != None:
		x, y = getIndexToPos(*b.selectedIndex)
		square = pygame.Rect(x-SQ_SIZE/2, y-SQ_SIZE/2, SQ_SIZE, SQ_SIZE)
		pygame.draw.rect(SCREEN, (255, 0, 0), square, 2)

def render(board : Board):

	while True:
		if exitEvent.is_set():
			break
		SCREEN.fill((255, 255, 255))
		
		RenderPipeline.execRenderMethods()
		RenderPipeline.renderAssets()

		pygame.display.update()

def main():


	run = True
	RenderPipeline.printMessages = False

	RenderPipeline.setScreen(SCREEN)
	RenderPipeline.addMethod(renderBoard, board)
	RenderPipeline.addMethod(renderHighlighted, board)
	RenderPipeline.addMethod(renderSelected, board)
	RenderPipeline.addMethod(renderPieces, board)
	RenderPipeline.addMethod(renderMoves, board)

	renderThread = threading.Thread(target=render, args=(board,), name="Render Thread")
	renderThread.start()

	while run:
		mousePos = pygame.mouse.get_pos()

		for e in pygame.event.get():
			if e.type == pygame.QUIT:
				exitEvent.set()
				renderThread.join()
				pygame.quit()
				quit()
			if e.type == pygame.MOUSEBUTTONDOWN:
				index = getPosToIndex(*mousePos)
				# print(index)
				if board.waitingOnPromotion:
					continue

				if (index != -1):
					if e.button == 1: # left click
						board.highlightedSquares = set()
						board.selectionLogic(index)
						# board.publicBoard = board.board.copy()


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
					board.undoMove()


					board.fen.refreshBoard(board.board)
					board.resetPublicBoard()

				elif e.key == pygame.K_y and len(board.moveFuture) > 0:
					board.makeMove(board.moveFuture.pop(-1))
					board.makeMove(board.moveFuture.pop(-1))
					board.fen.redo()
					board.fen.redo()

					board.fen.refreshBoard(board.board)
					board.resetPublicBoard()

				elif e.key == pygame.K_v: # debug hotkey

					print()

					moveLists = {

					}

					

					# RenderPipeline.printMessages = False
					# for k, v in ai.depthList.items():
					# 	moveLists[k] = []
					# 	ai.depthList[k] = ai.getTotalMoves(k, board, k, moveLists[k])
					# 	print(f"{k}\t{ai.depthList[k]}")

					print()

					aiMove = ai.getMove(board)

					board.makeMove(aiMove)
					board.resetPublicBoard()
					# for string in board.fen.history:
					# 	print(string)
					# print()

					print(f"Current FEN String\n{board.fen.getFenString(board.board)}")
		
		# if (board.checkMate or board.matchDraw) and not checkmatePrinting:
		# 	print("Game Over")
		# 	print("Ending FEN String\n", board.fen.getFenString(board.board))
		# 	print(f"checkMate = {board.checkMate}")
		# 	print(f"matchDraw = {board.matchDraw}")
		# 	continue

		if board.fen.colorToMove == "b" and not (board.checkMate or board.matchDraw):
			aiMove = ai.getMove(board)

			board.makeMove(aiMove)
			# print(board.publicBoard == board.board)
			# board.publicBoard = board.board.copy()
			board.resetPublicBoard()
			print("done")

		

		# render(board)
			


main()