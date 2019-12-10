import numpy as np

# Environment

experiment = 6
if experiment == 1:
	splitBar = False
	states = [(7, 0), (6, 1), (5, 2), (5, 3), (4, 4), (3, 5), (2, 6), (2, 7), (2, 8), (2, 9), (2, 10), (1, 11), (0, 12)]

	goalPos = {"A": (0, 15), "B": (7, 15), "C": (0, 2)}

elif experiment == 6:
	splitBar = True
	states = [(7, 0), (6, 1), (5, 2), (5, 3), (5, 4), (5, 5), (5, 6), (5, 7), (5, 8), (5, 9), (4, 9), (3, 9), (2, 9), (1, 9), (0, 9)]
	goalPos = {"A": (0, 15), "B": (7, 15), "C": (0, 9)}

world = np.zeros(shape=(8, 16)) # y then x
for goal in goalPos:
	y, x = goalPos[goal]
	world[y][x] = 1

if splitBar:
	for i in [3, 4, 6, 7]:
		for j in [7, 8]:
			world[i][j] = -1
else:
	for i in [3, 4, 5, 6, 7]:
		for j in [7, 8]:
			world[i][j] = -1

# Parameters

beta = 1.5
kappa = 0.9
gamma = 0.5