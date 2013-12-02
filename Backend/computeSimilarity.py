import os
import math

IDS = []


def cosSim(_numX, _numY):
	indX = []
	numX = []
	temp1, temp2, temp3 = 0.0, 0.0, 0.0

	for _x in _numX:
		dat = _x.split()
		indX.append(dat[0])
		numX.append(float(dat[1]))
	for _y in _numY:
		dat = _y.split()
		if dat[0] in indX:
			temp1 = temp1 + (float(dat[1]) * numX[indX.index(dat[0])])
			temp2 = temp2 + (float(dat[1]) * float(dat[1]))
			temp3 = temp3 + (numX[indX.index(dat[0])] * numX[indX.index(dat[0])])
	if temp1 == 0.0:
		return 0.0
	else:
		return temp1 / math.sqrt(temp2 * temp3)



def processGameScores():
	for x in IDS:
		scoresX = []
		scores = []
		with open("scores/{}.txt".format(x),'r') as file:
			scoresX = file.readline().split(', ')
			scoresX.pop()
		for y in IDS:
			scoresY = []
			if y != x:
				with open("scores/{}.txt".format(y),'r') as file:
					scoresY = file.readline().split(', ')
					scoresY.pop()
				scores.append((y,cosSim(scoresX, scoresY)))
			else:
				scores.append((y,0))
		scores = sorted(scores,key=lambda x:x[1], reverse=True)

		with open("ranks/{}.txt".format(x),'a') as file:
			for i in range(50):
				file.write(str(scores[i][0])+' '+str(scores[i][1])+'\n')

				

def main():
	global IDS
	files = os.listdir("scores/")
	for file in files:
		IDS.append(int(file.split('.txt')[0]))
	IDS.sort()

	processGameScores()


if __name__ == '__main__':
	main()