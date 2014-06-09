import csv, sys, copy
from array import *
from random import shuffle, sample


class Node:
        def __init__(self,attrIndex, fIndex, parent, y): #constructor of class
                self.attrIndex = attrIndex
                self.fIndex = fIndex
                self.left = None  #left leef
                self.right = None #right leef
                self.parent = parent
                self.y = y

        def addLeft(self, node):
                self.left = node

        def addRight(self, node):
                self.right = node

        


featureL = []
pfeatureL = []
y_list = []
ty_list = []
def calScore(exampleRC, lChildRC, rChildRC):
        MeanRC = float(sum(exampleRC))/float(len(exampleRC))
        sumRC = 0
        for item in exampleRC:
                sumRC = sumRC + (float(item) - MeanRC)*(float(item) - MeanRC)
        VarRC = float(sumRC)/float(len(exampleRC))

        lMeanRC = float(sum(lChildRC))/float(len(lChildRC))
        rMeanRC = float(sum(rChildRC))/float(len(rChildRC))
        lSumRC = 0
        rSumRC = 0
        for item in lChildRC:
                lSumRC = lSumRC + (float(item) - lMeanRC)*(float(item) - lMeanRC)
        lVarRC = float(lSumRC)/float(len(lChildRC))
        for item in rChildRC:
                rSumRC = rSumRC + (float(item) - rMeanRC)*(float(item) - rMeanRC)
        rVarRC = float(rSumRC)/float(len(rChildRC))

        score = VarRC - (float(len(lChildRC))/float(len(exampleRC)))*lVarRC -(float(len(rChildRC))/float(len(exampleRC)))*rVarRC
        return score

                
def DecisionTree(allFeatures):
        for row in yelp:
                rowIndex = 0
                while (rowIndex < len(row)):
                        if (rowIndex !=2 and row[rowIndex] not in features[rowIndex]):
                                features[rowIndex].append(row[rowIndex])
                        rowIndex  = rowIndex + 1
        #print ('all features are: \n', features)
        allFeatures = copy.deepcopy(features)
        rootNode = None
        rootNode = growTree(yelp, yelp, features, None, None, rootNode)
        #print rootNode.fIndex
        #printTree(rootNode)
        print y_list, len(y_list)
        #print featureL, len(featureL)
        #print pfeatureL, len(pfeatureL)
        return allFeatures
       

def growTree(node, examples, features, pNode, isLeft, rootNode):
        threshold = 0.1
        maxScore = 0
        maxFeature = ''
        lChildExamples = []
        rChildExamples = []
        attrIndex = 0
        maxAttrIndex = 0
        maxFeatureIndex = 0
        for attr in features:
                for feature in attr[1:]:
                        if feature != None:
                                #=print attrIndex, fIndex
                                lChild = []
                                rChild = []
                                exampleRC = []
                                lChildRC = []
                                rChildRC = []
                                for row in examples:
                                        exampleRC.append(int(row[2]))
                                        if(row[attrIndex] == feature):
                                                lChild.append(row)
                                                lChildRC.append(int(row[2]))
                                        else:
                                                rChild.append(row)
                                                rChildRC.append(int(row[2]))
                                if(len(lChildRC)==0 or len(rChildRC) == 0):
                                        continue
                                currentScore = calScore(exampleRC, lChildRC, rChildRC)
                                #print features[attrIndex][0], feature, currentScore
                                #if str(currentScore) == str(maxScore):
                                 #       print "!!!!!!EQUILITY"
                                if currentScore > maxScore and str(currentScore) != str(maxScore):#currentScore-maxScore>0.00000001:
                                        #print 'new',  currentScore, maxScore
                                        maxFeature = feature
                                        maxAttrIndex = attrIndex
                                        maxFeatureIndex = attr.index(feature)
                                        maxScore = currentScore
                                        lChildExamples = lChild
                                        rChildExamples = rChild
                attrIndex = attrIndex + 1
        if(maxScore < threshold):
                #print pNode
                nodeRC = []
                for row in examples:
                        nodeRC.append(int(row[2]))
                meanRC = float(sum(nodeRC))/float(len(nodeRC))
                currentNode = Node(None, None, pNode, meanRC)
                if(isLeft):
                        pNode.addLeft(currentNode)
                else:
                        pNode.addRight(currentNode)
                return

        #print '         max!!!!!!!!!!!!!!!!!!!!!!!!', features[maxAttrIndex][0], maxFeature, maxFeatureIndex, maxScore
        #print features[maxAttrIndex][maxFeatureIndex]
        features[maxAttrIndex][maxFeatureIndex] = None

        if(rootNode == None):
                rootNode = Node(maxAttrIndex, maxFeatureIndex, None, None)
                growTree(examples, lChildExamples, features, rootNode, True, rootNode)
                growTree(examples, rChildExamples, features, rootNode, False, rootNode)
        else:
                currentNode = Node(maxAttrIndex, maxFeatureIndex, pNode, None)
                if(isLeft):
                        pNode.addLeft(currentNode)
                else:
                        pNode.addRight(currentNode)
                growTree(examples, lChildExamples, features, currentNode, True, rootNode)
                growTree(examples, rChildExamples, features, currentNode, False, rootNode)

        return rootNode


def printTree(node):
	print "printTree"
	if node == None:
		return
	print "node.attrIndex = ", node.attrIndex
	printTree(node.left)
	printTree(node.right)


                             
def prediction(testExample, allFeatures, node):
        while(node != None):
                if(node.y != None):
                        #print testExample[2]
                        return float(int(testExample[2])- int(node.y))*float(int(testExample[2])- int(node.y))
                trainF = allFeatures[int(node.attrIndex)][int(node.fIndex)]
                if(trainF == row[node.attrIndex]):
                        node = node.left
                else:
                        node = node.right
                

##################### Args ######################
if len(sys.argv) == 3:
        #print('arg1', sys.argv[1])
        #print('arg2', sys.argv[2])
	trainSet = open(sys.argv[1], 'rU')
	testSet = open(sys.argv[2], 'rU')
else:
	print('Invalid Execution Format')
	sys.exit()

## Read data and train data in table ##
reader = csv.reader(trainSet)
index = -1
yelp = []
attributesL = []
reviewCountL = []
longitudeL = []
latitudeL = []
for row in reader:
	if (index == -1):
		attributesL = row
		index = index + 1
		continue
	yelp.append(row)
	reviewCountL.append(int(row[2]))
	longitudeL.append(float(row[19]))
	latitudeL.append(float(row[32]))
	index += 1
trainSet.close()


### Sort continuous values ###
longitudeL.sort()
latitudeL.sort()

LG25Q = longitudeL[len(longitudeL)/4]
LG75Q = longitudeL[len(longitudeL)*3/4]
LT25Q = latitudeL[len(latitudeL)/4]
LT75Q = latitudeL[len(latitudeL)*3/4]

### Parse Features ###
index = 0
for row in yelp:
	## Convert continuous attributes to discrete ##
	if float(row[19]) <= LG25Q:
		row[19] = 'low'
	elif float(row[19]) > LG25Q and float(row[19]) <= LG75Q:
		row[19] = 'med'
	else:
		row[19] = 'high'
	if float(row[32]) <= LT25Q:
		row[32] = 'low'
	elif float(row[32]) > LT25Q and float(row[32]) <= LT75Q:
		row[32] = 'med'
	else:
		row[32] = 'high'
#print attributesL

features = []
allFeatures = []
count = 0
while (count < len(attributesL)):
        if(count != 2):
                attribute = []
                attribute.append(attributesL[count])
                features.append(attribute)
        else:
                attribute = []
                features.append(attribute)
        count = count + 1


#print ('feature attributes are: \n', features)
#allFeatures = DecisionTree(allFeatures)

## Read data and test data in table ##
reader = csv.reader(testSet)
index = -1
testT = []
longitudeL = []
latitudeL = []
for row in reader:
	if (index == -1):
		index = index + 1
		continue
	testT.append(row)
	longitudeL.append(float(row[19]))
	latitudeL.append(float(row[32]))
	index = index + 1
testSet.close()

### Sort continuous values ###
longitudeL.sort()
latitudeL.sort()

LG25Q = longitudeL[len(longitudeL)/4]
LG75Q = longitudeL[len(longitudeL)*3/4]
LT25Q = latitudeL[len(latitudeL)/4]
LT75Q = latitudeL[len(latitudeL)*3/4]

### Parse Features ###
index = 0
for row in testT:
	## Convert continuous attributes to discrete ##
	if float(row[19]) <= LG25Q:
		row[19] = 'low'
	elif float(row[19]) > LG25Q and float(row[19]) <= LG75Q:
		row[19] = 'med'
	else:
		row[19] = 'high'
	if float(row[32]) <= LT25Q:
		row[32] = 'low'
	elif float(row[32]) > LT25Q and float(row[32]) <= LT75Q:
		row[32] = 'med'
	else:
		row[32] = 'high'



for row in yelp:
        rowIndex = 0
        while (rowIndex < len(row)):
                if (rowIndex !=2 and row[rowIndex] not in features[rowIndex]):
                        features[rowIndex].append(row[rowIndex])
                rowIndex  = rowIndex + 1
allFeatures = copy.deepcopy(features)

rootNode = None
rootNode = growTree(yelp, testT, features, None, None, rootNode)

sumY = 0
for row in testT:
        sumY = sumY + prediction(row, allFeatures, rootNode)

print float(sumY)/float(len(testT))




