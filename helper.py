def normalize(probs):
	s = sum(probs)
	return [i/float(s) for i in probs]

def normalizeVals(probDict):
	s = sum(probDict.values())
	return {i: probDict[i]/float(s) for i in probDict}