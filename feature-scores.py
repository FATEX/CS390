import csv
import sys
import copy
import math
from array import *


def printTopFeatures(list, type):
        outputFile = open('./top_10_features.txt', 'w+')
	print '*****************TOP10 features*****************'
	maxF = [[], [], []]
	columnIndex = 0
	while columnIndex < len(list):
		cMaxScore = 0
		cMaxIndex = 0
		Index = 0
		while Index < len(list[columnIndex]):
			if list[columnIndex][Index] > cMaxScore:
				cMaxScore = list[columnIndex][Index]
				columnMaxIndex = Index
			elif list[columnIndex][Index] == cMaxScore:
				maxF[0].append(columnIndex)
				maxF[1].append(cMaxIndex)
				maxF[2].append(cMaxScore)
				cMaxScore = list[columnIndex][Index]
				cMaxIndex = Index
			Index += 1
		maxF[0].append(columnIndex)
		maxF[1].append(cMaxIndex)
		maxF[2].append(cMaxScore)
		columnIndex += 1
	top10 = copy.copy(maxF[2])
	top10.sort()
	top10 = top10[len(top10)-10:len(top10)]
	maxIndex = 0
	while maxIndex < len(maxF[2]):
		if maxF[2][maxIndex] in top10:
			attribute1 = attribute[maxF[0][maxIndex]]
			feature = X[maxF[0][maxIndex]][0][maxF[1][maxIndex]]
			if type is 'C':
				functionType = 'Chi-Square'
			else:
				functionType = 'Information-Gain'
			sys.stdout.write(functionType + ', max feature=<' + attribute1 + ',' + feature + '>, max score=' + str(maxF[2][maxIndex]) + '\n')
			outputFile.write(functionType + ', max feature=<' + attribute1 + ',' + feature + '>, max score=' + str(maxF[2][maxIndex]) + '\n')
		maxIndex += 1
		
def printMax(list, type):
        print '*****************TOP1 feature*****************'
	maxF = [[], [], []]
	columnIndex = 0
	while columnIndex < len(list):
		cMaxScore = 0
		cMaxIndex = 0
		Index = 0
		while Index < len(list[columnIndex]):
			if list[columnIndex][Index] > cMaxScore:
				cMaxScore = list[columnIndex][Index]
				cMaxIndex = Index
			elif list[columnIndex][Index] == cMaxScore:
				maxF[0].append(columnIndex)
				maxF[1].append(cMaxIndex)
				maxF[2].append(cMaxScore)
				cMaxScore = list[columnIndex][Index]
				cMaxIndex = Index
			Index = Index + 1
		maxF[0].append(columnIndex)
		maxF[1].append(cMaxIndex)
		maxF[2].append(cMaxScore)
		columnIndex = columnIndex + 1
	maxScore = max(maxF[2])
	maxIndex = 0
	while maxIndex < len(maxF[2]):
		if maxF[2][maxIndex] == maxScore:
			attribute1 = attribute[maxF[0][maxIndex]]
			feature = X[maxF[0][maxIndex]][0][maxF[1][maxIndex]]
			if type is 'C':
				functionType = 'Chi-Square'
			else:
				functionType = 'Information-Gain'
			sys.stdout.write(functionType + ', max feature=<' + attribute1 + ',' + feature + '>, max score=' + str(maxScore) + '\n')
		maxIndex += 1



fileName = open(sys.argv[1], 'rU')
classIndex = int(sys.argv[2])
scoreFunction = sys.argv[3]

reviewCount = array('i')
longitude = array('d')
latitude = array('d')
yelp = []
X = []
F = []
attribute = []

reader = csv.reader(fileName)
i = -1

for row in reader:
    if (i == -1):
        attribute = row
        i += 1
        continue
    yelp.append(row)
    reviewCount.append(int(row[2]))
    longitude.append(float(row[19]))
    latitude.append(float(row[32]))
    i += 1

SortedreviewCount = sorted(reviewCount)
Sortedlongitude = sorted(longitude)
Sortedlatitude = sorted(latitude)

reviewCountFirstQ = (SortedreviewCount[641]+SortedreviewCount[642])/2
reviewCountThirdQ = (SortedreviewCount[1923]+SortedreviewCount[1924])/2

longitudeFirstQ = (Sortedlongitude[641]+Sortedlongitude[642])/2
longitudeThirdQ = (Sortedlongitude[1923]+Sortedlongitude[1924])/2

latitudeFirstQ = (Sortedlatitude[641]+Sortedlatitude[642])/2
latitudeThirdQ = (Sortedlatitude[1923]+Sortedlatitude[1924])/2
fileName.close()

first = 1
for row in yelp:
	if int(row[2])<= reviewCountFirstQ:
            row[2] = 'low'
        elif int(row[2]) > reviewCountFirstQ and int(row[2]) < reviewCountThirdQ:
            row[2] = 'med'
        elif int(row[2]) >= reviewCountThirdQ:
            row[2] = 'high'
            
        if float(row[19])<= longitudeFirstQ:
            row[19] = 'low'
        elif float(row[19]) > longitudeFirstQ and float(row[19]) < longitudeThirdQ:
            row[19] = 'med'
        elif float(row[19]) >= longitudeThirdQ:
            row[19] = 'high'

        if float(row[32])<= latitudeFirstQ:
            row[32] = 'low'
        elif float(row[32]) > latitudeFirstQ and float(row[32]) < latitudeThirdQ:
            row[32] = 'med'
        elif float(row[32]) >= latitudeThirdQ:
            row[32] = 'high'

        
	columnIndex = 0
	for item in row:
		if first == 1:
			X.append([[item], [1]])
			F.append([[[], []]])
		elif item not in X[columnIndex][0]:
			X[columnIndex][0].append(item)
			X[columnIndex][1].append(1)
			F[columnIndex].append([[], []])
		else:
			X[columnIndex][1][X[columnIndex][0].index(item)] += 1
		columnIndex += 1
	first = 0

for row in yelp:
	columnIndex = 0
	for item in row:
		if columnIndex is not classIndex:
			classIndexCount = 0
			while len(F[columnIndex][X[columnIndex][0].index(item)][0]) < len(X[classIndex][0]):
				F[columnIndex][X[columnIndex][0].index(item)][0].append(X[classIndex][1][classIndexCount])
				F[columnIndex][X[columnIndex][0].index(item)][1].append(0)
				classIndexCount += 1
			F[columnIndex][X[columnIndex][0].index(item)][0][X[classIndex][0].index(row[classIndex])] -= 1
			F[columnIndex][X[columnIndex][0].index(item)][1][X[classIndex][0].index(row[classIndex])] += 1
		columnIndex += 1

if scoreFunction is 'C':
    Chi = []
    ChiSum = 0
    M = copy.deepcopy(F)
    Tsum = len(yelp)
    columnIndex = 0
    while columnIndex < len(F):
        Chi.append([])
        if columnIndex is not classIndex:
            i = 0
            while i < len(F[columnIndex]):
                j = 0
                while j < len(X[classIndex][0]):
                    Vsum = F[columnIndex][i][0][j] + F[columnIndex][i][1][j]
                    Hsum = sum(F[columnIndex][i][0])
                    #print 'Hsum for [0] = ', Hsum
                    M[columnIndex][i][0][j] = Hsum * Vsum / float(Tsum)
                    ChiSum = ChiSum + (F[columnIndex][i][0][j]-M[columnIndex][i][0][j])*(F[columnIndex][i][0][j]-M[columnIndex][i][0][j])/M[columnIndex][i][0][j]
                    Hsum = sum(F[columnIndex][i][1])
                    #print 'Hsum for [1] = ', Hsum
                    M[columnIndex][i][1][j] = Hsum * Vsum / float(Tsum)
                    ChiSum = ChiSum + (F[columnIndex][i][1][j]-M[columnIndex][i][1][j])*(F[columnIndex][i][1][j]-M[columnIndex][i][1][j])/M[columnIndex][i][1][j]
                    j += 1
                Chi[columnIndex].append(ChiSum)
                ChiSum = 0
                i += 1
        else:
            Chi[columnIndex].append(-100)
        columnIndex += 1

    index = 0
    result = []
    while index < len(Chi):
        result.append(max(Chi[index]))
        index = index + 1
    maxChi = max(result)



    index = 0
    temp = []
    st = 0
    sort = []
    while index < len(Chi):
        while st< len(Chi[index]):
            temp.append(Chi[index][st])
            st = st+1
        st = 0
        index = index + 1
    sort = sorted(temp, reverse=True)

    printTopFeatures(Chi, 'C')
    printMax(Chi, 'C')

# Information Gain
if scoreFunction is 'I':
	EntropyC = 0
	sumC = float(len(yelp))
	IndexC = 0
	while IndexC < len(X[classIndex]):
		EntropyC += -(X[classIndex][1][IndexC]/sumC * math.log(X[classIndex][1][IndexC]/sumC, 2))
		IndexC += 1
	
	En = []
	columnIndex = 0
	while columnIndex < len(F):
		En.append([])
		if columnIndex is not classIndex:
			Index = 0
			while Index < len(F[columnIndex]):
				en = 0
				IndexC = 0
				while IndexC < len(X[classIndex][0]):
					if F[columnIndex][Index][1][IndexC]/float(sum(F[columnIndex][Index][1])) != 0:
						en += -(F[columnIndex][Index][1][IndexC]/float(sum(F[columnIndex][Index][1])) * math.log((F[columnIndex][Index][1][IndexC]/float(sum(F[columnIndex][Index][1]))), 2))
					IndexC += 1
				En[columnIndex].append(en)
				Index += 1
		else:
			En[columnIndex].append(-1)
		columnIndex += 1
	printTopFeatures(En, 'I')
	printMax(En, 'I')
