#Jonathan Wasson 463117
#Honours project
#checks MDPS and adapts game



import random, time, pygame, sys, copy, math
from random import randrange
from pygame.locals import *

def get_unique_state(s):
	state = 0
	for i in range(10):
		temp = int(s[0][i])*(20^i)
		state = temp + state
	state = state + int(s[1])*(20^11)
	state = state + int(s[2])*(7^12)
	state = state + int(s[3])*(4^13)
	state = state + int(s[4])*(10^14)
	#state = state + int(s[5])*(20^15)
	return state

def get_MDP(filename):
	InputFile = []
	with open(filename,"r") as myfile:
		for line in myfile:
    		#data management
			data = line.split(",")
			s1 = data[0].split(" ")
			p = data[1]
			s1[0] = s1[0].split("/")
			probabilities = p.split("/")
			probabilities[0] = probabilities[0][1:]
			probabilities[5] = probabilities[5][:-2]
			for n in range(len(probabilities)):
				probabilities[n] = int(probabilities[n])
			#print probabilities	

			#get unique index
			state = get_unique_state(s1)
			InputFile.append([state,probabilities])

	return InputFile


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


#overall probabilities
#note that the first entry corresponds to human then badai then goodai
MDPPROBABILITIES = [0.33333,0.33333,0.33333]
MDPCHECK = 1

#MDP of each AI
MDPBAD = get_MDP("MDPbadai.txt")
MDPHUMAN = get_MDP("MDPhuman.txt")
MDPGOOD = get_MDP("MDPgoodai.txt")

#counts how many steps it takes to converge
CONVERGENCECOUNT = 0

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
	pygame.display.set_caption('Tetris')
	showTextScreen('Tetris')
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
		#bad ai
		pygame.event.post(easy_ai(board,currentBlock))

		#good ai
		#pygame.event.post(good_ai(board,currentBlock))



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
					change_probability(action,board,currentBlock,score)

				elif (event.key == K_RIGHT or event.key == K_d) and isValidPosition(board, currentBlock, adjX=1):
					action = "Right"
					tempBlock = currentBlock.copy()
					currentBlock['x'] += 1
					movingRight = True
					movingLeft = False
					lastMoveSidewaysTime = time.time()
					change_probability(action,board,currentBlock,score)

				# rotating the piece (if there is room to rotate)
				elif (event.key == K_UP or event.key == K_w):
					action = "Up"
					tempBlock = currentBlock.copy()
					currentBlock['rotation'] = (currentBlock['rotation'] + 1) % len(PIECES[currentBlock['shape']])
					if not isValidPosition(board, currentBlock):
						currentBlock['rotation'] = (currentBlock['rotation'] - 1) % len(PIECES[currentBlock['shape']])
					change_probability(action,board,currentBlock,score)
				elif (event.key == K_q): # rotate the other direction
					action = "Up"
					tempBlock = currentBlock.copy()
					currentBlock['rotation'] = (currentBlock['rotation'] - 1) % len(PIECES[currentBlock['shape']])
					if not isValidPosition(board, currentBlock):
						currentBlock['rotation'] = (currentBlock['rotation'] + 1) % len(PIECES[currentBlock['shape']])
					change_probability(action,board,currentBlock,score)

				# making the piece fall faster with the down key
				elif (event.key == K_DOWN or event.key == K_s):
					tempBlock = currentBlock.copy()
					movingDown = True
					if isValidPosition(board, currentBlock, adjY=1):
						currentBlock['y'] += 1
					lastMoveDownTime = time.time()
					action = "Down"
					change_probability(action,board,currentBlock,score)


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
					change_probability(action,board,currentBlock,score)


		# handle moving the piece because of user input
		if (movingLeft or movingRight) and time.time() - lastMoveSidewaysTime > MOVESIDEWAYSFREQ:
			if movingLeft and isValidPosition(board, currentBlock, adjX=-1):
				tempBlock = currentBlock.copy()
				currentBlock['x'] -= 1
				action = "Left"
				change_probability(action,board,currentBlock,score)
			elif movingRight and isValidPosition(board, currentBlock, adjX=1):
				tempBlock = currentBlock.copy()
				currentBlock['x'] += 1
				action = "Right"
				change_probability(action,board,currentBlock,score)
			lastMoveSidewaysTime = time.time()

		if movingDown and time.time() - lastMoveDownTime > MOVEDOWNFREQ and isValidPosition(board, currentBlock, adjY=1):
			tempBlock = currentBlock.copy()
			currentBlock['y'] += 1
			lastMoveDownTime = time.time()
			action = "Down"
			change_probability(action,board,currentBlock,score)

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
	Speed = 0.27 - (level * 0.02)
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


def get_action_num(action):
	if action == "Left":
		return 0
	if action == "Right":
		return 1
	if action == "Up":
		return 2
	if action == "Down":
		return 3
	if action == "Space":
		return 4
	return 5


def get_probabilities(probabilities):
	prob_sum = 0
	for i in range(len(probabilities)):
		prob_sum = prob_sum + probabilities[i]
	for j in range(len(probabilities)):
		probabilities[j] = float(probabilities[j])/prob_sum
	return probabilities

def update_probabilities(probAgent, probAction):
	probUp = math.log(probAgent) + math.log(probAction)
	#probUp = float(probAction)*float(probAgent)
	return probUp
def fetch_prob(MDP,state):
	#probabilities = [0.16666666,0.16666666,0.16666666,0.16666666,0.16666666,0.16666666]
	probabilities = [0,0,0,0,0,0]
	for i in range(len(MDP)):
		if MDP[i][0] == state:
			probabilities = get_probabilities(MDP[i][1])
	return probabilities

#gets boards state and the action made
def	change_probability(action,board,currentBlock,score):
	global MDPHUMAN
	global MDPGOOD
	global MDPBAD
	global MDPPROBABILITIES
	global CONVERGENCECOUNT
	global MDPCHECK

	#variable to check how accurate process is
	accuracy = 0.1

	#increments counter
	CONVERGENCECOUNT = CONVERGENCECOUNT + 1

	#get boards current state
	statestring = []

	heights = get_heights(board)
	statestring.append(heights)

	shape = get_shape_num(currentBlock.get("shape"))
	statestring.append(shape)
	rotation = currentBlock.get("rotation")
	statestring.append(rotation	)
	X = currentBlock.get("x")
	statestring.append( X)
	Y = currentBlock.get("y")
	statestring.append( Y	)

	statenum = get_unique_state(statestring)
	action = get_action_num(action)
	#find the state in the MDP
	#aabd fetch the appropriate probabilities
	prob1 = fetch_prob(MDPHUMAN,statenum)
	prob2 = fetch_prob(MDPBAD,statenum)
	prob3 = fetch_prob(MDPGOOD,statenum)	


	#update the probabilities of each MDP
	#first we get P(A|a) = P(a|A)P(A)
	if prob1[action] > 0.0:
		temp1 = update_probabilities(MDPPROBABILITIES[0],prob1[action])
		if temp1 < 0.0:
			temp1 = -(temp1)
	else:
		temp1 = MDPPROBABILITIES[0]

	if prob2[action] > 0.0:	
		temp2 = update_probabilities(MDPPROBABILITIES[1],prob2[action])
		if temp2 < 0.0:
			temp2 = -(temp2)
	else:
		temp2 = MDPPROBABILITIES[1]

	if prob3[action] > 0.0:	
		temp3 = update_probabilities(MDPPROBABILITIES[2],prob3[action])
		if temp3 < 0.0:
			temp3 = -(temp3)
	else:
		temp3 = MDPPROBABILITIES[2]

	#then we normalise and update
	sumprob = temp1 + temp2 + temp3
	MDPPROBABILITIES[0] = (temp1 / sumprob)
	MDPPROBABILITIES[1] = (temp2 / sumprob)
	MDPPROBABILITIES[2] = (temp3 / sumprob)

	#check to see if accurate enough to make decisions
	#and then make appropriate changes to game

	if MDPPROBABILITIES[0] > (1 - accuracy):
		#MDPPROBABILITIES = [0.33333,0.33333,0.33333]
		MDPCHECK = 0
		write_answer('Skilled')
	if MDPPROBABILITIES[1] > (1 - accuracy):
		#MDPPROBABILITIES = [0.33333,0.33333,0.33333]
		MDPCHECK = 1
		write_answer('Unskilled')
	if MDPPROBABILITIES[2] > (1 - accuracy):
		#MDPPROBABILITIES = [0.33333,0.33333,0.33333]
		MDPCHECK = 2
		write_answer('Moderate')

	print MDPPROBABILITIES[0]
	print MDPPROBABILITIES[1]
	print MDPPROBABILITIES[2]
	#store the updates for data collection
	write_prob(score)

def get_differences_in_height(heights):
	distances = []
	for i in range(len(heights)-1):
		distances.append(heights[i+1]-heights[i])
	return distances


def get_move(pointa,pointb):
	key = K_s
	if (pointa < pointb):
		key = K_a
	elif (pointa > pointb):
		key = K_d
	elif (pointa == pointb):
	 	key = K_SPACE
	else:
	 	key = K_w
	return key


def lowest_block(heights):
	lowest = 2323232323
	for i in range(len(heights)):
		if heights[i] < lowest:
			lowest = heights[i]

	return heights.index(lowest)


def get_empty_space(shape,orientation):
	if shape == "S":
		if orientation == 0:
			return 1
		else:	
			return  2
	elif shape == "Z":
		if orientation == 0:
			return 1
		else:	
			return  1
	elif shape == "J":
		if orientation == 0:
			return 1
		elif orientation == 1:
			return 2
		elif orientation == 2:
			return 1
		else:
			return 1
	elif shape == "L":
		if orientation == 0:
			return 1
		elif orientation == 1:
			return 2
		elif orientation == 2:
			return 1
		else:
			return 1
	elif shape == "I":
		if orientation == 0:
			return 2
		else:	
			return  0
	elif shape == "O":
		return 1
	elif shape == "T":
		if orientation == 0:
			return 1
		elif orientation == 1:
			return 2
		elif orientation == 2:
			return 1
		else:
			return 1

	return 0

def find_move(shape,orientation,distances,x,y,lowest):
	#indicates the possible perfect places that it can be put
	move = K_s
	blanks = get_empty_space(shape,orientation)
	x = x + blanks
	if shape == "S":
		move = K_SPACE
		for i in range(len(distances)):
			if (distances[i] == -1):
				if (orientation == 1):
					return get_move(i,x)
				else: 
					return K_w

		for i in range(len(distances)-1):
			if (distances[i] == 0):
				if (distances[i+1] == 1):
					if (orientation == 0):
						return get_move(i,x)
					else:
						return K_w

	elif shape == "Z":
		move = K_SPACE
		for i in range(len(distances)):
			if (distances[i] == 1):
				if (orientation == 1):
					return get_move(i,x)
				else: 
					return K_w
		for i in range(len(distances)-1):
			if (distances[i] == -1):
				if (distances[i+1] == 0):
					if (orientation == 0):
						return get_move(i,x)
					else:
						return K_w
	elif shape == "J":
		move = K_w
		for i in range(len(distances)-1):
			if orientation == 0:
				if distances[i] == 0:
					if distances[i+1] == 0:
						return get_move(i,x)
			elif orientation == 2:
				if distances[i]==0:
					if distances[i+1]==-1:
						return get_move(i,x)
		for i in range(len(distances)):
			if orientation == 1:
				if distances[i] == 2:
					return get_move(i,x)
			elif orientation == 3:
				if distances[i]==0:
					return get_move(i,x)


	elif shape == "L":
		move = K_w
		for i in range(len(distances)-1):
			if orientation == 0:
				if distances[i] == 0:
					if distances[i+1] == 0:
						return get_move(i,x)
			elif orientation == 2:
				if distances[i]==1:
					if distances[i+1]==0:
						return get_move(i,x)
		for i in range(len(distances)):
			if orientation == 1:
				if distances[i] == 0:
					return get_move(i,x)
			elif orientation == 3:
				if distances[i]==-2:
					return get_move(i,x)

	elif shape == "I":
		move = K_w
		if orientation == 0:
			move = get_move(lowest,x)
		if orientation == 1:
			for i in range(len(distances)-2):
				if (distances[i]==0):
					if (distances[i+1]==0):
						if (distances[i+2]==0):
							if (orientation==1):
								return get_move(i,x)
							else:
								return K_w
		else:
			return get_move(lowest,x)


	elif shape == "O":
		move = K_SPACE
		for i in range(len(distances)):
			if (distances[i] == 0):
				return get_move(i,x)

	elif shape == "T":
		move = K_SPACE
		for i in range(len(distances)-1):
				if orientation == 0:
					if distances[i] == 0:
						if distances[i+1] == 0:
							return get_move(i,x)

				elif orientation == 2:
					if distances[i]==-1:
						if distances[i+1]==1:
							return get_move(i,x)

		for i in range(len(distances)):
			if orientation == 1:
				if distances[i] == 1:
					return get_move(i,x)

			elif orientation == 3:
				if distances[i] == -1:
					return get_move(i,x)


	return move



def good_ai(board, currentBlock):
	heights = get_heights(board)
	distances = get_differences_in_height(heights)
	shape = currentBlock.get("shape")
	orientation = currentBlock.get("rotation")
	posX = currentBlock.get("x")
	posY = currentBlock.get("y")
	lowest = lowest_block(heights)
	move = find_move(shape,orientation,distances,posX,posY,lowest)


	return pygame.event.Event(KEYDOWN,key=move)


def write_answer(answer):
	global CONVERGENCECOUNT
	if answer == 'Unskilled':
		guess = 'Correct'
	else:
		guess = 'Incorrect'
	with open("Accuracy.txt","a") as myfile:
		myfile.write(answer  + ',   ' + guess + ',   ' + str(CONVERGENCECOUNT)  + '\n')
	CONVERGENCECOUNT = 0

def write_prob(score):
	global MDPPROBABILITIES
	human = 26
	bad = 0
	good = 1
	if score > bad:
		performance = 'Improved'
	else:
		performance = 'Decreased'
	with open("GameChanges.txt","a") as myfile:
		myfile.write(str(MDPPROBABILITIES[0]) + ', ' + str(MDPPROBABILITIES[1]) + ', '+ str(MDPPROBABILITIES[2])+', '+ str(score) + ', '+ performance + '\n')


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
	# lowest = 20
	# index = 0
	# for i in range(len(heights)):
	# 	if (heights[i] < lowest):
	# 		lowest = heights[i]
	# 		index = i
	# shape = currentBlock.get("shape")
	# xcoords, ycoords = get_coords_of_block(currentBlock)
	# smallest = ycoords[0]
	# posSmall = 0
	# for n in range(len(ycoords)):
	# 	if ycoords[n] > smallest:
	# 		smallest = ycoords[n]
	# 		posSmall = n
	shape = currentBlock.get("shape")
	posX = currentBlock.get("x")
	posY = currentBlock.get("y")
	orientation = currentBlock.get("rotation")	
	posSmall = 0
	Small = 20	
	for n in range(len(heights)):
		if heights[n] < Small:
			Small = heights[n]
			posSmall = n

	n = posSmall
	posX = posX + get_empty_space(shape, orientation)
	orientation = currentBlock.get("rotation")

	if (n < posX):
		return pygame.event.Event(KEYDOWN,key=K_a)
	elif (n > posX):
		return pygame.event.Event(KEYDOWN,key=K_d)
	elif (n == posX):
		return pygame.event.Event(KEYDOWN,key=K_SPACE )
	else:
		return pygame.event.Event(KEYUP,key=K_w)


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

def shapeDist():
	global MDPCHECK
	if MDPCHECK == 0:
		return random.choice(["Z","S","L","J"])
	elif MDPCHECK == 1:
		return random.choice(["O","I"])
	elif MDPCHECK == 2:
		return random.choice(["O","I","L","J"])
	else:
		return random.choice(list(PIECES.keys()))


def getNewBlock():
	# return a random new piece in a random rotation and color
	#shape = random.choice(list(PIECES.keys()))
	shape = shapeDist()
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