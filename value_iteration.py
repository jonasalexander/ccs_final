import math
from copy import deepcopy

from data import world, goalPos, beta, gamma, kappa
import helper as h

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

stateVals = {goal: {} for goal in goalPos}

def q(action, state, goal):
	ns = (state[0]+action[0], state[1]+action[1])
	return stateVals[goal][ns]-cost(action)

def actionProb(action, state, goal):
	index = None
	probs = []
	for i, a in enumerate(legalActions(state)):
		ns = (state[0]+a[0], state[1]+a[1])
		if a == action:
			index = i
		probs.append(math.exp(beta*q(a, state, goal)))
	probs = h.normalize(probs)
	return probs[index]

# Initialize with length of direct path estimate
for goal in goalPos:
	y, x = goalPos[goal]
	for i in range(len(world)):
		for j in range(len(world[i])):
			if world[i][j] == -1:
				continue
			s = (i, j)
			stateVals[goal][s] = -1*lengthOfPath(s, goal)

# Update state values iteratively
for i in range(20):
	# policy is given by old q values
	oldValues = deepcopy(stateVals)
	for goal in goalPos:
		y, x = goalPos[goal]
		for state in oldValues[goal]:
			if state == (y, x):
				stateVals[goal][state] = 0
				continue
			probs = []
			vals = []
			for a in legalActions(state):
				ns = (state[0]+a[0], state[1]+a[1])
				qa = oldValues[goal][ns]-cost(a)
				probs.append(math.exp(beta*qa))
				vals.append(qa)
			probs = h.normalize(probs)
			stateVals[goal][state] = sum([v1*v2 for v1,v2 in zip(probs,vals)])


