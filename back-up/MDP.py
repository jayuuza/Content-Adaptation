import sys


#converts the number of blocks into base 20
def convert_state(s):
	state = 0
	for i in range(10):
		temp = int(s[0][i])*(20^i)
		state = temp + state
	state = state + int(s[1])*(20^11)
	state = state + int(s[2])*(7^12)
	state = state + (int(s[3])+2)*(4^13)
	state = state + (int(s[4])+2)*(10^14)
	#state = state + int(s[5])*(20^15)
	return state

def writeto_MDP():
	global MDP
	with open("fastMDP.txt","a") as myfile:
		for i in range(len(MDP)):
			if MDP[i]!= None:
				cstate = MDP[i][0]
				probabilities = MDP[i][1]
				pout = '['
				for n in range(len(probabilities)):
					pout = pout + str(probabilities[n]) + '/'
				pout = pout[:-1] + ']'
				outline = cstate + ',' + pout + '\n'
				myfile.write(outline)

def check_state(state):
	global MDP
	# try:
	# 	print MDP.index(state)
	# 	MDP.index(state)
	# 	return True
	# except ValueError:
	# 	return False	
	if MDP[state] == None:
		return False
	else:
		return True

def get_data():
	InputFile = []
	with open("fast.txt", "r") as inpFile:
	    	for line in inpFile:
	    			InputFile.append(line)
	return InputFile

#updates the probability counter for each action with actions stored in this order [left,right,up,down,space,none]
def update_probabilities(actionProb,action):
	if action == "Left":
		actionProb[0] = actionProb[0] + 1
	elif action == "Right":
		actionProb[1] = actionProb[1] + 1
	elif action == "Up":
		actionProb[2] = actionProb[2] + 1
	elif action == "Down":
		actionProb[3] = actionProb[3] + 1
	elif action == "Space":
		actionProb[4] = actionProb[4] + 1
	elif action == "NoAction":
		actionProb[5] = actionProb[5] + 1
	return actionProb


def make_MDP(InputFile):
	global MDP
	for i in range(len(InputFile)):
    	#data management
		data = InputFile[i].split(",")
		s1 = data[0].split(" ")
		a = data[1]
		s2 = data[2].split(" ")
		s1[0] = s1[0].split("/")
		s2[0] = s2[0].split("/")

		#get unique index
		state = convert_state(s1)

		#update the MDP
		#check to see if the state doesnt exist
		#otherwise update the state
		if check_state(state) == False:
			probabilities = [0,0,0,0,0,0]
			probabilities = update_probabilities(probabilities,a)
			MDP[state] = [data[0],probabilities]
		else:
			probabilities = MDP[state][1]
			probabilities = update_probabilities(probabilities,a)
			MDP[state][1] = probabilities

		#add state to key list for quick lookup of all indices in the MDP

		#print MDP[229]
	



MDP = [None]*6000
keyList = []
Input = get_data()


make_MDP(Input)
#print keyList
writeto_MDP()		