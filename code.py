from matplotlib.pylab import plt

import helper as h
import value_iteration as vit
import data as d

MODEL = 4

# Model 1
if MODEL == 1:
	# GOAL INFERENCE

	probG = [{i: 1.0/3 for i in d.goalPos.keys()}]

	# at each time step, calculate the probability of each goal up to that point
	for t, st in enumerate(d.states[:-1]):
		currProbs = probG[t].copy()
		ns = d.states[t+1]
		action = (ns[0]-st[0], ns[1]-st[1])
		for goal in d.goalPos:
			# prob of taking action needed to go st->ns
			currProbs[goal] *= vit.actionProb(action, st, goal)

		currProbs = h.normalizeVals(currProbs)
		probG.append(currProbs)

	probGA = [e["A"] for e in probG]
	probGB = [e["B"] for e in probG]
	probGC = [e["C"] for e in probG]

	plt.plot(probGA[2:], label="A")
	plt.plot(probGB[2:], label="B")
	plt.plot(probGC[2:], label="C")
	plt.legend()
	plt.show()


# Model 2
if MODEL == 2:
	beta = 1.5
	kappa = 0.9

	probG = [{i: (1.0-kappa)/3 for i in goalPos.keys()}]
	numStates = len(states)
	for state in states:
		probG.append({state: kappa/numStates})



	# with probability kappa, complex goal that has intermediate point as goal first
	# distribution over goals within each type uniform

# Model 3 without backward-forward algorithm

if MODEL == 3:

	# goals can change over time
	# k goals, 

	# GOAL INFERENCE

	probG = [{i: 1.0/3 for i in d.goalPos.keys()}]
	k = len(d.goalPos.keys())

	# at each time step, calculate the probability of each goal up to that point
	for t, st in enumerate(d.states[:-1]):
		currProbs = probG[t].copy()
		ns = d.states[t+1]
		action = (ns[0]-st[0], ns[1]-st[1])
		for goal in d.goalPos:
			# prob of taking action needed to go st->ns
			probGoal = 0
			for g in probG[t]:
				p1 = probG[t][g]
				p2 = 1-d.gamma if g == goal else d.gamma/(k-1)
				probGoal += p1*p2
			currProbs[goal] = vit.actionProb(action, st, goal)*probGoal

		currProbs = h.normalizeVals(currProbs)
		probG.append(currProbs)

	probGA = [e["A"] for e in probG]
	probGB = [e["B"] for e in probG]
	probGC = [e["C"] for e in probG]

	plt.plot(probGA, label="A")
	plt.plot(probGB, label="B")
	plt.plot(probGC, label="C")
	plt.legend()
	plt.show()

# Model 3

if MODEL == 4:

	# GOAL INFERENCE

	probG = [{i: 1.0/3 for i in d.goalPos.keys()}]
	k = len(d.goalPos.keys())

	forwardProbs = {goal: [1 for _ in range(len(d.states)-2)] for goal in d.goalPos}
	for goal in d.goalPos:
		for t in range(1, len(d.states)):
			if t == 1 or t == 2:
				continue
			ns = d.states[-t+2]
			rsum = 0
			for g in d.goalPos:
				st = d.states[-t+1]
				action = (ns[0]-st[0], ns[1]-st[1])
				p1 = vit.actionProb(action, st, g)

				p2 = 1-d.gamma if g == goal else d.gamma/(k-1)
				
				rsum += p1*forwardProbs[goal][-t+1]*p2
			forwardProbs[goal][-t+2] = rsum

	# at each time step, calculate the probability of each goal up to that point
	for t, st in enumerate(d.states[:-1]):
		currProbs = probG[t].copy()
		ns = d.states[t+1]
		action = (ns[0]-st[0], ns[1]-st[1])
		for goal in d.goalPos:
			# prob of taking action needed to go st->ns
			probGoal = 0
			for g in probG[t]:
				p1 = probG[t][g]
				p2 = 1-d.gamma if g == goal else d.gamma/(k-1)
				probGoal += p1*p2
			probBack = vit.actionProb(action, st, goal)*probGoal
			if t < len(d.states)-2:
				currProbs[goal] = probBack*forwardProbs[goal][t]
			else:
				currProbs[goal] = probBack

		currProbs = h.normalizeVals(currProbs)
		probG.append(currProbs)

	probGA = [e["A"] for e in probG]
	probGB = [e["B"] for e in probG]
	probGC = [e["C"] for e in probG]

	plt.plot(probGA, label="A")
	plt.plot(probGB, label="B")
	plt.plot(probGC, label="C")
	plt.legend()
	plt.show()

