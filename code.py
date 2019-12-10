import math
import numpy as np
from matplotlib.pylab import plt
import random
from copy import deepcopy

def normalize(probs):
	s = sum(probs)
	return [i/float(s) for i in probs]

def normalizeVals(probDict):
	s = sum(probDict.values())
	return {i: probDict[i]/float(s) for i in probDict}

# Model 1

beta = 2

states = [(7, 0), (6, 1), (5, 2), (5, 3), (4, 4), (3, 5), (2, 6), (2, 7), \
		(2, 8), (2, 9), (2, 10), (1, 11), (0, 12)]#, (0, 12), (0, 12), (0, 12),\
		#(0, 12), (0, 12), (0, 12), (0, 12), (0, 12), (0, 12), (0, 12), (0, 12)]

goalPos = {"A": (0, 15), "B": (7, 15), "C": (0, 2)}

world = np.zeros(shape=(8, 16)) # y then x
for goal in goalPos:
	y, x = goalPos[goal]
	world[y][x] = 1

for i in [3, 4, 5, 6, 7]:
	for j in [7, 8]:
		world[i][j] = -1

start = (7, 0)

# LEARN VALUE FUNCTION

def legalActions(state):
	y, x = state
	if world[y][x] == -1:
		return []

	actions = [(0, 0)]
	
	up, down, left, right = False, False, False, False
	if y != 0 and world[y-1][x] != -1:
		up = True
		actions.append((-1, 0))
	if y != len(world)-1 and world[y+1][x] != -1:
		down = True
		actions.append((1, 0))

	if x != 0 and world[y][x-1] != -1:
		left = True
		actions.append((0, -1))
	if x != len(world[0])-1 and world[y][x+1] != -1:
		right = True
		actions.append((0, 1))

	if up and left and world[y-1][x-1] != -1:
		actions.append((-1, -1))
	if up and right and world[y-1][x+1] != -1:
		actions.append((-1, 1))
	if down and left and world[y+1][x-1] != -1:
		actions.append((1, -1))
	if down and right and world[y+1][x+1] != -1:
		actions.append((1, 1))

	return actions

def cost(action):
	return 0 if action == (0, 0) else 1

pathLengths = {goal: {} for goal in goalPos}

for goal in goalPos:
	y, x = goalPos[goal]
	q = [((y, x), 0)]
	pathLengths[goal][(y, x)] = 0
	explored = set([(y, x)])
	while q:
		next, dist = q.pop(0)
		for a in legalActions(next):
			ns = (next[0]+a[0], next[1]+a[1])
			if ns in explored:
				continue
			pathLengths[goal][ns] = dist+cost(a)
			explored.add(ns)
			q.append((ns, dist+cost(a)))

def lengthOfPath(state, goal):
	return pathLengths[goal][state]

stateValues = {goal: {} for goal in goalPos}

def q(action, state, goal):
	ns = (state[0]+action[0], state[1]+action[1])
	return stateValues[goal][ns]-cost(action)

def actionProb(action, state, goal):
	index = None
	probs = []
	for i, a in enumerate(legalActions(state)):
		ns = (state[0]+a[0], state[1]+a[1])
		if a == action:
			index = i
		probs.append(math.exp(beta*q(a, state, goal)))
	probs = normalize(probs)
	return probs[index]

# initialize with straight line path estimate
for goal in goalPos:
	y, x = goalPos[goal]
	for i in range(len(world)):
		for j in range(len(world[i])):
			if world[i][j] == -1:
				continue
			s = (i, j)
			stateValues[goal][s] = -1*lengthOfPath(s, goal)

for i in range(len(world)):
	l = []
	for j in range(len(world[i])):
		state = (i, j)
		if state in stateValues["A"]:
			l.append('%.1f' % stateValues["A"][state])
		else:
			l.append("0")
		
	print " ".join(l)
print "\n"

# Update state values iteratively
for i in range(20):
	# policy is given by old q values
	oldValues = deepcopy(stateValues)
	for goal in goalPos:
		y, x = goalPos[goal]
		for state in oldValues[goal]:
			# probability of each action that I'll take from this state
			# times value of the state I'd end up in
			if state == (y, x):
				stateValues[goal][state] = 0
				continue
			probs = []
			vals = []
			for a in legalActions(state):
				ns = (state[0]+a[0], state[1]+a[1])
				#print state, a, ns
				qa = oldValues[goal][ns]-cost(a)
				probs.append(math.exp(beta*qa))
				vals.append(qa)
			probs = normalize(probs)
			if state in []:
				print state, legalActions(state)
				print vals
				print probs
				print sum([g*h for g,h in zip(probs,vals)])
			stateValues[goal][state] = sum([g*h for g,h in zip(probs,vals)])



#print stateValues["A"][(5, 3)], stateValues["A"][(4, 3)]
#print stateValues["A"][(1, 6)], stateValues["B"][(1, 6)], stateValues["C"][(1, 6)]
"""
for i in range(len(world)):
	l = []
	for j in range(len(world[i])):
		state = (i, j)
		if state in stateValues["A"]:
			l.append('%.1f' % stateValues["A"][state])
		else:
			l.append("0")
		
	print " ".join(l)
print "A \n"

for i in range(len(world)):
	l = []
	for j in range(len(world[i])):
		state = (i, j)
		if state in stateValues["B"]:
			l.append('%.1f' % stateValues["B"][state])
		else:
			l.append("0")
		
	print " ".join(l)
print "B \n"

for i in range(len(world)):
	l = []
	for j in range(len(world[i])):
		state = (i, j)
		if state in stateValues["C"]:
			l.append('%.1f' % stateValues["C"][state])
		else:
			l.append("0")
		
	print " ".join(l)

print "A: ", actionProb((0, 1), (5, 2), "A")
print "C: ", actionProb((0, 1), (5, 2), "C")
"""
# Goal inference
#beta = 0.2

probG = [{i: 1.0/3 for i in goalPos.keys()}]

# at each time step, calculate the probability of each goal up to that point
for t, st in enumerate(states[:-1]):
	currProbs = probG[t].copy()
	ns = states[t+1]
	action = (ns[0]-st[0], ns[1]-st[1])
	for goal in goalPos:
		# prob of taking action needed to go st->ns
		currProbs[goal] *= actionProb(action, st, goal)

	#print currProbs
	currProbs = normalizeVals(currProbs)
	print action, st, currProbs
	probG.append(currProbs)

#print probG

probGA = [e["A"] for e in probG]
probGB = [e["B"] for e in probG]
probGC = [e["C"] for e in probG]

plt.plot(probGA, label="A")
plt.plot(probGB, label="B")
plt.plot(probGC, label="C")
plt.legend()
plt.show()

"""
# Model 2

beta = 1.5
kappa = 0.9



# with probability kappa, complex goal that has intermediate point as goal first
# distribution over goals within each type uniform


# Model 3

beta = 2
gamma = 0.1

# goals can change over time
# k goals, 
"""

