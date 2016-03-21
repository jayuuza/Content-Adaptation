# Tetromino was coded with help from:
# Al Sweigart al@inventwithpython.com
# http://inventwithpython.com/pygame
# Released under a "Simplified BSD" license

import random, time, pygame, sys, copy
from random import randrange
from pygame.locals import *

FPS = 25
WINDOWWIDTH = 640
WINDOWHEIGHT = 480
BOXSIZE = 20
BOARDWIDTH = 10
BOARDHEIGHT = 20
BLANK = '.'

MOVESIDEWAYSFREQ = 0.15
MOVEDOWNFREQ = 0.1

XMARGIN = int((WINDOWWIDTH - BOARDWIDTH * BOXSIZE) / 2)
TOPMARGIN = WINDOWHEIGHT - (BOARDHEIGHT * BOXSIZE) - 5

#               R    G    B
WHITE       = (255, 255, 255)
GRAY        = (185, 185, 185)
BLACK       = (  0,   0,   0)
RED         = (155,   0,   0)
LIGHTRED    = (175,  20,  20)
GREEN       = (  0, 155,   0)
LIGHTGREEN  = ( 20, 175,  20)
BLUE        = (  0,   0, 155)
LIGHTBLUE   = ( 20,  20, 175)
YELLOW      = (155, 155,   0)
LIGHTYELLOW = (175, 175,  20)

BORDERCOLOR = BLUE
BGCOLOR = BLACK
TEXTCOLOR = WHITE
TEXTSHADOWCOLOR = GRAY
COLORS      = (     BLUE,      GREEN,      RED,      YELLOW)
LIGHTCOLORS = (LIGHTBLUE, LIGHTGREEN, LIGHTRED, LIGHTYELLOW)
assert len(COLORS) == len(LIGHTCOLORS) # each color must have light color

TEMPLATEWIDTH = 5
TEMPLATEHEIGHT = 5

S_SHAPE_TEMPLATE = [['.....',
					 '.....',
					 '..OO.',
					 '.OO..',
					 '.....'],
					['.....',
					 '..O..',
					 '..OO.',
					 '...O.',
					 '.....']]

Z_SHAPE_TEMPLATE = [['.....',
					 '.....',
					 '.OO..',
					 '..OO.',
					 '.....'],
					['.....',
					 '..O..',
					 '.OO..',
					 '.O...',
					 '.....']]

I_SHAPE_TEMPLATE = [['..O..',
					 '..O..',
					 '..O..',
					 '..O..',
					 '.....'],
					['.....',
					 '.....',
					 'OOOO.',
					 '.....',
					 '.....']]

O_SHAPE_TEMPLATE = [['.....',
					 '.....',
					 '.OO..',
					 '.OO..',
					 '.....']]

J_SHAPE_TEMPLATE = [['.....',
					 '.O...',
					 '.OOO.',
					 '.....',
					 '.....'],
					['.....',
					 '..OO.',
					 '..O..',
					 '..O..',
					 '.....'],
					['.....',
					 '.....',
					 '.OOO.',
					 '...O.',
					 '.....'],
					['.....',
					 '..O..',
					 '..O..',
					 '.OO..',
					 '.....']]

L_SHAPE_TEMPLATE = [['.....',
					 '...O.',
					 '.OOO.',
					 '.....',
					 '.....'],
					['.....',
					 '..O..',
					 '..O..',
					 '..OO.',
					 '.....'],
					['.....',
					 '.....',
					 '.OOO.',
					 '.O...',
					 '.....'],
					['.....',
					 '.OO..',
					 '..O..',
					 '..O..',
					 '.....']]

T_SHAPE_TEMPLATE = [['.....',
					 '..O..',
					 '.OOO.',
					 '.....',
					 '.....'],
					['.....',
					 '..O..',
					 '..OO.',
					 '..O..',
					 '.....'],
					['.....',
					 '.....',
					 '.OOO.',
					 '..O..',
					 '.....'],
					['.....',
					 '..O..',
					 '.OO..',
					 '..O..',
					 '.....']]

PIECES = {'S': S_SHAPE_TEMPLATE,
		  'Z': Z_SHAPE_TEMPLATE,
		  'J': J_SHAPE_TEMPLATE,
		  'L': L_SHAPE_TEMPLATE,
		  'I': I_SHAPE_TEMPLATE,
		  'O': O_SHAPE_TEMPLATE,
		  'T': T_SHAPE_TEMPLATE}

def main():
	global FPSCLOCK, DISPLAYSURF, BASICFONT, BIGFONT
	pygame.init()
	FPSCLOCK = pygame.time.Clock()
	DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
	BASICFONT = pygame.font.Font('freesansbold.ttf', 18)
	BIGFONT = pygame.font.Font('freesansbold.ttf', 100)
	pygame.display.set_caption('Tetromino')
	showTextScreen('Tetromino')
	while True: # game loop
		runGame()

		#showTextScreen('Game Over')
	pygame.event.post(pygame.event.Event(KEYDOWN,key=K_w))



def runGame():
	# setup variables for the start of the game

	board = getBlankBoard()
	lastMoveDownTime = time.time()
	lastMoveSidewaysTime = time.time()
	lastFallTime = time.time()
	movingDown = False 
	movingLeft = False
	movingRight = False
	score = 0
	Speed = 0.20
	#if (inSpeed == "Fast"):
	#	Speed = 0.08
	#elif (inSpeed == "Medium"):
	# 	Speed = 0.20
	#else:
	#	Speed = 0.40
	level, Speed = incrementSpeedAndLevel(score,Speed)
	currentBlock = getNewBlock()
	prevBlock = currentBlock
	nextBlock = getNewBlock()
	#Moves = ["Start"]

	while True: # game loop 
		if currentBlock == None:
			currentBlock = nextBlock
			nextBlock = getNewBlock()
			lastFallTime = time.time() # reset lastFallTime
			#write_state(board, Moves, prevBlock, score)
			#Moves = []
			#write_action(prevBoard, board, action, prevBlock, currentBlock,score-1,score)
			if not isValidPosition(board, currentBlock):
				return # can't fit a new piece on the board, so game over

		checkForQuit()
		#ai players move if necessary
		pygame.event.post(easy_ai(board,currentBlock))
		for event in pygame.event.get(): # event handling loop
			
			#if event.type == pygame.MOUSEBUTTONUP and event.button == LEFT:

			if event.type == KEYUP:
				if (event.key == K_p):
					# Pausing the game
					DISPLAYSURF.fill(BGCOLOR)
					
					showTextScreen('Paused') # pause until a key press
					
					lastFallTime = time.time()
					lastMoveDownTime = time.time()
					lastMoveSidewaysTime = time.time()
				elif (event.key == K_LEFT or event.key == K_a):
					movingLeft = False
				elif (event.key == K_RIGHT or event.key == K_d):
					movingRight = False
				elif (event.key == K_DOWN or event.key == K_s):
					movingDown = False

			elif event.type == KEYDOWN:
				# moving the piece sideways
				if (event.key == K_LEFT or event.key == K_a) and isValidPosition(board, currentBlock, adjX=-1):
					action = "Left"
					tempBlock = currentBlock.copy()
					currentBlock['x'] -= 1
					movingLeft = True
					movingRight = False
					lastMoveSidewaysTime = time.time()
					write_action(board, board, action, tempBlock, currentBlock, score,score)

				elif (event.key == K_RIGHT or event.key == K_d) and isValidPosition(board, currentBlock, adjX=1):
					action = "Right"
					tempBlock = currentBlock.copy()
					currentBlock['x'] += 1
					movingRight = True
					movingLeft = False
					lastMoveSidewaysTime = time.time()
					write_action(board, board, action, tempBlock, currentBlock, score,score)

				# rotating the piece (if there is room to rotate)
				elif (event.key == K_UP or event.key == K_w):
					action = "Up"
					tempBlock = currentBlock.copy()
					currentBlock['rotation'] = (currentBlock['rotation'] + 1) % len(PIECES[currentBlock['shape']])
					if not isValidPosition(board, currentBlock):
						currentBlock['rotation'] = (currentBlock['rotation'] - 1) % len(PIECES[currentBlock['shape']])
					write_action(board, board, action, tempBlock, currentBlock, score,score)
				elif (event.key == K_q): # rotate the other direction
					action = "Up"
					tempBlock = currentBlock.copy()
					currentBlock['rotation'] = (currentBlock['rotation'] - 1) % len(PIECES[currentBlock['shape']])
					if not isValidPosition(board, currentBlock):
						currentBlock['rotation'] = (currentBlock['rotation'] + 1) % len(PIECES[currentBlock['shape']])
					write_action(board, board, action, tempBlock, currentBlock, score,score)

				# making the piece fall faster with the down key
				elif (event.key == K_DOWN or event.key == K_s):
					tempBlock = currentBlock.copy()
					movingDown = True
					if isValidPosition(board, currentBlock, adjY=1):
						currentBlock['y'] += 1
					lastMoveDownTime = time.time()
					action = "Down"
					write_action(board, board, action, tempBlock, currentBlock, score,score)


				# move the current piece all the way down
				elif event.key == K_SPACE:
					tempBlock = currentBlock.copy()
					movingDown = False
					movingLeft = False
					movingRight = False
					for i in range(1, BOARDHEIGHT):
						if not isValidPosition(board, currentBlock, adjY=i):
							break
					currentBlock['y'] += i - 1
					action = "Space"
					write_action(board, board, action, tempBlock, currentBlock, score,score)


		# handle moving the piece because of user input
		if (movingLeft or movingRight) and time.time() - lastMoveSidewaysTime > MOVESIDEWAYSFREQ:
			if movingLeft and isValidPosition(board, currentBlock, adjX=-1):
				tempBlock = currentBlock.copy()
				currentBlock['x'] -= 1
				action = "Left"
				write_action(board, board, action, tempBlock, currentBlock, score,score)
			elif movingRight and isValidPosition(board, currentBlock, adjX=1):
				tempBlock = currentBlock.copy()
				currentBlock['x'] += 1
				action = "Right"
				write_action(board, board, action, tempBlock, currentBlock, score,score)
			lastMoveSidewaysTime = time.time()

		if movingDown and time.time() - lastMoveDownTime > MOVEDOWNFREQ and isValidPosition(board, currentBlock, adjY=1):
			tempBlock = currentBlock.copy()
			currentBlock['y'] += 1
			lastMoveDownTime = time.time()
			action = "Down"
			write_action(board, board, action, tempBlock, currentBlock, score,score)

		# let the piece fall if it is time to fall
		if time.time() - lastFallTime > Speed:
			# see if the piece has landed
			if not isValidPosition(board, currentBlock, adjY=1):
				# falling piece has landed, set it on the board
				prevBoard = list(board[:])
				addToBoard(board, currentBlock)
				score += removeCompleteLines(board)
				level, Speed = incrementSpeedAndLevel(score,Speed)
				prevBlock = currentBlock.copy()

				currentBlock = None
			else:
				# piece did not land, just move the piece down
				currentBlock['y'] += 1
				lastFallTime = time.time()
		
		# drawing everything on the screen
		DISPLAYSURF.fill(BGCOLOR)
		drawBoard(board)
		drawStatus(score, level)
		drawnextBlock(nextBlock)
		if currentBlock != None:
			drawPiece(currentBlock)	   
		pygame.display.update()
		FPSCLOCK.tick(FPS)

def makeTextObjs(text, font, color):
	surf = font.render(text, True, color)
	return surf, surf.get_rect()

def terminate():
	pygame.quit()
	sys.exit()

def checkForKeyPress():
	# Go through event queue looking for a KEYUP event.
	# Grab KEYDOWN events to remove them from the event queue.
	checkForQuit()
	for event in pygame.event.get([KEYDOWN, KEYUP]):
		if event.type == KEYDOWN:
			continue
		return event.key
	return None
def get_coords_of_block(Block):
	shape = Block.get("shape")
	posX = Block.get("x")
	posY = Block.get("y")
	rotation = Block.get("rotation")
	xcoords = []
	ycoords = []
	for x in range(TEMPLATEWIDTH):
		for y in range(TEMPLATEHEIGHT):
			if PIECES[shape][rotation][x][y] != BLANK:
				xcoords.append(posX+x)
				ycoords.append(posY+y)
	return xcoords, ycoords


def easy_ai(board, currentBlock):
	heights = get_heights(board)
	lowest = 20
	index = 0
	for i in range(len(heights)):
		if (heights[i] < lowest):
			lowest = heights[i]
			index = i
	shape = currentBlock.get("shape")
	xcoords, ycoords = get_coords_of_block(currentBlock)
	smallest = ycoords[0]
	posSmall = 0
	for n in range(len(ycoords)):
		if ycoords[n] > smallest:
			smallest = ycoords[n]
			posSmall = n

	posX = xcoords[posSmall]
	posY = smallest
	orientation = currentBlock.get("rotation")

	if (index < posX):
		return pygame.event.Event(KEYDOWN,key=K_a)
	elif (index > posX):
		return pygame.event.Event(KEYDOWN,key=K_d)
	elif (index == posX):
		return pygame.event.Event(KEYDOWN,key=K_s)
	else:
		return pygame.event.Event(KEYUP,key=K_w)


def showTextScreen(text):
	# This function displays large text in the
	# center of the screen until a key is pressed.
	# Draw the text drop shadow
	titleSurf, titleRect = makeTextObjs(text, BIGFONT, TEXTSHADOWCOLOR)
	titleRect.center = (int(WINDOWWIDTH / 2), int(WINDOWHEIGHT / 2))
	DISPLAYSURF.blit(titleSurf, titleRect)

	# Draw the text
	titleSurf, titleRect = makeTextObjs(text, BIGFONT, TEXTCOLOR)
	titleRect.center = (int(WINDOWWIDTH / 2) - 3, int(WINDOWHEIGHT / 2) - 3)
	DISPLAYSURF.blit(titleSurf, titleRect)

	# Draw the additional "Press a key to play." text.
	pressKeySurf, pressKeyRect = makeTextObjs('Press a key to play.', BASICFONT, TEXTCOLOR)
	pressKeyRect.center = (int(WINDOWWIDTH / 2), int(WINDOWHEIGHT / 2) + 100)
	DISPLAYSURF.blit(pressKeySurf, pressKeyRect)

	while checkForKeyPress() == None:
		pygame.display.update()
		FPSCLOCK.tick()

def checkForQuit():
	for event in pygame.event.get(QUIT): # get all the QUIT events
		terminate() # terminate if any QUIT events are present
	for event in pygame.event.get(KEYUP): # get all the KEYUP events
		if event.key == K_ESCAPE:
			terminate() # terminate if the KEYUP event was for the Esc key
		pygame.event.post(event) # put the other KEYUP event objects back

def incrementSpeedAndLevel(score,Speed):
	level = int(score / 10) + 1
	#Speed = 0.27 - (level * 0.02)
	return level, Speed

def get_shape_num(shape):
	if shape == "S":
		return 0
	elif shape == "Z":
		return 1
	elif shape == "J":
		return 2
	elif shape == "L":
		return 3
	elif shape == "I":
		return 4
	elif shape == "O":
		return 5
	elif shape == "T":
		return 6
	return 0

def write_action(board, nextboard, action, currentBlock, nextBlock, Score, NextScore):
	with open("aimedium.txt", "a") as myfile:
		heights = get_heights(board)
		blocks = ""

		heights2 = get_heights(nextboard)
		blocks2 = ""

		#include each columns height
		for i in range(BOARDWIDTH):
			blocks = blocks + "/" + str(heights[i])
		blocks = blocks[1:]

		for i in range(BOARDWIDTH):
			blocks2 = blocks2 + "/" + str(heights2[i])
		blocks2 = blocks2[1:]

		currentshape = str(currentBlock.get("shape"))
		nextshape = str(nextBlock.get("shape"))
		currentshape = get_shape_num(currentshape)
		nextshape  = get_shape_num(nextshape )

		currentrotation = currentBlock.get("rotation")
		nextrotation = nextBlock.get("rotation")

		currentx = currentBlock.get("x")
		nextx = nextBlock.get("x")

		currenty = currentBlock.get("y")
		nexty = nextBlock.get("y")

		currentstate = blocks + " " + str(currentshape) + " " + str(currentrotation) + " " + str(currentx) + " " + str(currenty) + " " + str(Score)
		nextstate = blocks2 + " " + str(nextshape) + " " + str(nextrotation) + " " + str(nextx) + " " + str(nexty) + " " + str(NextScore)


		state = currentstate + "," + action + "," + nextstate + "\n"
		myfile.write(state)

# def write_state(board, Moves, Block, Score):
# 	with open("fasteasy.txt", "a") as myfile:
# 		heights = get_heights(board)
# 		blocks = ""
# 		numEmptyBlocks = calc_num_gaps(heights, board)
# 		state = convert_state(heights)
# 		boardstate = str(state)

# 		#include each columns height
# 		#for i in range(BOARDWIDTH):
# 		#	blocks = blocks + " " + str(heights[i])
# 		#blocks = blocks + " " + boardstate + " " + str(numEmptyBlocks) + "\n"
# 		if not Moves:
# 			M = "NoAction"
# 		else:
# 			M = Moves[0]
# 		for i in range(len(Moves)-1):
# 			M = M + " " + Moves[i+1]
# 		shape = Block.get("shape")
# 		blocks = boardstate + " " + str(shape) + " " + str(numEmptyBlocks) + " " + str(Score) + " " + M + "\n"
# 		myfile.write(blocks)


def get_heights(board):
	heights = [0]*10
	for i in range(BOARDWIDTH):
		totalblocks = 0
		topheight = 20
		#gets the heights of the columns
		y = 0
		while y <= 19:
			if board[i][y] != BLANK:
				topheight = y
				break
			y = y + 1
		heights[i] = 20 - topheight
	return heights

# #calculate the gaps in the stack of blocks
# def calc_num_gaps(heights, board):
# 	numEmptyBlocks = 0
# 	for i in range(BOARDWIDTH):	
# 		j = 1
# 		while j <= int(heights[i]):
# 			if board[i][20 - j] == BLANK:
# 				numEmptyBlocks = numEmptyBlocks + 1
# 			j = j + 1
# 	return numEmptyBlocks

#converts the number of blocks into base 20
# def convert_state(heights):
# 	state = 0
# 	for i in range(BOARDWIDTH):
# 		temp = heights[i]*(20^i)
# 		state = temp + state
# 	return state

def getNewBlock():
	# return a random new piece in a random rotation and color
	shape = random.choice(list(PIECES.keys()))
	newPiece = {'shape': shape,
				'rotation': random.randint(0, len(PIECES[shape]) - 1),
				'x': int(BOARDWIDTH / 2) - int(TEMPLATEWIDTH / 2),
				'y': -2, # start it above the board (i.e. less than 0)
				'color': random.randint(0, len(COLORS)-1)}
	return newPiece

def addToBoard(board, piece):
	# fill in the board based on piece's location, shape, and rotation
	for x in range(TEMPLATEWIDTH):
		for y in range(TEMPLATEHEIGHT):
			if PIECES[piece['shape']][piece['rotation']][y][x] != BLANK:
				board[x + piece['x']][y + piece['y']] = piece['color']

def getBlankBoard():
	# create and return a new blank board data structure
	board = []
	for i in range(BOARDWIDTH):
		board.append([BLANK] * BOARDHEIGHT)
	return board

def isOnBoard(x, y):
	return x >= 0 and x < BOARDWIDTH and y < BOARDHEIGHT

def isValidPosition(board, piece, adjX=0, adjY=0):
	# Return True if the piece is within the board and not colliding
	for x in range(TEMPLATEWIDTH):
		for y in range(TEMPLATEHEIGHT):
			isAboveBoard = y + piece['y'] + adjY < 0
			if isAboveBoard or PIECES[piece['shape']][piece['rotation']][y][x] == BLANK:
				continue
			if not isOnBoard(x + piece['x'] + adjX, y + piece['y'] + adjY):
				return False
			if board[x + piece['x'] + adjX][y + piece['y'] + adjY] != BLANK:
				return False
	return True

def isCompleteLine(board, y):
	# Return True if the line filled with boxes with no gaps.
	for x in range(BOARDWIDTH):
		if board[x][y] == BLANK:
			return False
	return True

def removeCompleteLines(board):
	# Remove any completed lines on the board, move everything above them down, and return the number of complete lines.
	numLinesRemoved = 0
	y = BOARDHEIGHT - 1 # start y at the bottom of the board
	while y >= 0:
		if isCompleteLine(board, y):
			# Remove the line and pull boxes down by one line.
			for pullDownY in range(y, 0, -1):
				for x in range(BOARDWIDTH):
					board[x][pullDownY] = board[x][pullDownY-1]
			# Set very top line to blank.
			for x in range(BOARDWIDTH):
				board[x][0] = BLANK
			numLinesRemoved += 1
		else:
			y -= 1 # move on to check next row up
	return numLinesRemoved

def convertToPixelCoords(boxx, boxy):
	# Convert the given xy coordinates of the board to xy
	# coordinates of the location on the screen.
	return (XMARGIN + (boxx * BOXSIZE)), (TOPMARGIN + (boxy * BOXSIZE))

def drawBox(boxx, boxy, color, pixelx=None, pixely=None):
	# draw a single box (each tetromino piece has four boxes)
	# at xy coordinates on the board. Or, if pixelx & pixely
	# are specified, draw to the pixel coordinates stored in
	# pixelx & pixely (this is used for the "Next" piece).
	if color == BLANK:
		return
	if pixelx == None and pixely == None:
		pixelx, pixely = convertToPixelCoords(boxx, boxy)
	pygame.draw.rect(DISPLAYSURF, COLORS[color], (pixelx + 1, pixely + 1, BOXSIZE - 1, BOXSIZE - 1))
	pygame.draw.rect(DISPLAYSURF, LIGHTCOLORS[color], (pixelx + 1, pixely + 1, BOXSIZE - 4, BOXSIZE - 4))

def drawBoard(board):
	# draw the border around the board
	pygame.draw.rect(DISPLAYSURF, BORDERCOLOR, (XMARGIN - 3, TOPMARGIN - 7, (BOARDWIDTH * BOXSIZE) + 8, (BOARDHEIGHT * BOXSIZE) + 8), 5)

	# fill the background of the board
	pygame.draw.rect(DISPLAYSURF, BGCOLOR, (XMARGIN, TOPMARGIN, BOXSIZE * BOARDWIDTH, BOXSIZE * BOARDHEIGHT))
	# draw the individual boxes on the board
	for x in range(BOARDWIDTH):
		for y in range(BOARDHEIGHT):
			drawBox(x, y, board[x][y])

def drawStatus(score, level):
	# draw the score text
	scoreSurf = BASICFONT.render('Score: %s' % score, True, TEXTCOLOR)
	scoreRect = scoreSurf.get_rect()
	scoreRect.topleft = (WINDOWWIDTH - 150, 20)
	DISPLAYSURF.blit(scoreSurf, scoreRect)

	# draw the level text
	levelSurf = BASICFONT.render('Level: %s' % level, True, TEXTCOLOR)
	levelRect = levelSurf.get_rect()
	levelRect.topleft = (WINDOWWIDTH - 150, 50)
	DISPLAYSURF.blit(levelSurf, levelRect)

def drawPiece(piece, pixelx=None, pixely=None):
	shapeToDraw = PIECES[piece['shape']][piece['rotation']]
	if pixelx == None and pixely == None:
		# if pixelx & pixely hasn't been specified, use the location stored in the piece data structure
		pixelx, pixely = convertToPixelCoords(piece['x'], piece['y'])

	# draw each of the boxes that make up the piece
	for x in range(TEMPLATEWIDTH):
		for y in range(TEMPLATEHEIGHT):
			if shapeToDraw[y][x] != BLANK:
				drawBox(None, None, piece['color'], pixelx + (x * BOXSIZE), pixely + (y * BOXSIZE))

def drawnextBlock(piece):
	# draw the "next" text
	nextSurf = BASICFONT.render('Next:', True, TEXTCOLOR)
	nextRect = nextSurf.get_rect()
	nextRect.topleft = (WINDOWWIDTH - 120, 80)
	DISPLAYSURF.blit(nextSurf, nextRect)
	# draw the "next" piece
	drawPiece(piece, pixelx=WINDOWWIDTH-120, pixely=100)

if __name__ == '__main__':
	main()