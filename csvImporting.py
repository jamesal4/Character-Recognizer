import csv
import numpy as np
import operator
import random
import matplotlib.pyplot as plt

def getLengthOfLongestExample(data):
    maxLength = 0
    for point in data:
        length = point.shape[0]
        if length > maxLength:
            maxLength = length
    return maxLength

def getLengthOfShortestExample(data):
    minLength = 1000
    minInd = 0
    i = 0
    for point in data:
        length = point.shape[0]
        if length < minLength:
            minInd = i
            minLength = length
        i+=1
    return (minLength, minInd)

def sameLengthForEachLetter(data,labels,letterCount,letterToOneHot):
    leastOccurringLetter = min(letterCount.items(), key=operator.itemgetter(1))[0]
    leastOccurringFrequency = letterCount[leastOccurringLetter]
    for letter in letterCount:
        if letter == leastOccurringLetter:
            continue
        while letterCount[letter] > leastOccurringFrequency:
            randInt = random.randrange(data.shape[0])
            if allLabels[randInt].all() == letterToOneHot[letter].all():
                letterCount[letter]-=1
                data = np.delete(data, (randInt), axis=0)
                labels = np.delete(labels, (randInt), axis=0)

    return data,labels

def padExamplesToLength(length,data):
    newData = []
    for point in data:
        pointLen = point.shape[0]
        zeros = np.tile(np.zeros(6),(length-pointLen,1))
        newPoint = np.concatenate((point,zeros))
        newData.append(newPoint)
    return np.array(newData)

letterToOneHot = {'A':np.array([1,0,0,0]),'B':np.array([0,1,0,0]),'C':np.array([0,0,1,0]),'D':np.array([0,0,0,1])}
#oneHotToLetter = {np.array([1,0,0,0]):'A',np.array([0,1,0,0]):'B',np.array([0,0,1,0]):'C',np.array([0,0,0,1]):'D'}
letterCount = {'A':0,'B':0,'C':0,'D':0}
letters = ["A","B","C","D"]
names = ["Kevin","Akhil"]
allData = []
allLabels = []

for j in range(len(letters)):
    letter = letters[j]
    for i in range(len(names)):
        name = names[i]
        with open(name+letter+'.csv') as csvfile:
            reader = csv.reader(csvfile)
            innerArray = []
            for row in reader:
                if row[0] == "Time":
                    continue
                npRow = np.array(row[1:7],dtype=np.float32)
                if npRow.all() == np.zeros(6).all():
                    letterCount[letter]+=1
                    allData.append(np.array(innerArray))
                    oneHot = [0]*len(letters)
                    oneHot[i] = 1
                    label = np.array(oneHot)
                    allLabels.append(label)
                    innerArray = []
                else:
                    innerArray.append(npRow)


allData = np.array(allData)
allLabels = np.array(allLabels)

print('allData.shape: '+str(allData.shape))
print("letterCount: "+str(letterCount))
length = 0
ct = 0
while length < 100:
    ct+=1
    length,index = getLengthOfShortestExample(allData)
    letterInd = np.argmax(allLabels[index])
    letterCount[letters[letterInd]]-=1
    allData = np.delete(allData, (index), axis=0)
    allLabels = np.delete(allLabels, (index), axis=0)

print("deleted: " +str(ct))
print("newShortest: "+str(getLengthOfShortestExample(allData)))
print('allData.shape: '+str(allData.shape))
print("letterCount: "+str(letterCount))

maxLen = getLengthOfLongestExample(allData)
allData = padExamplesToLength(maxLen,allData)
allData,allLabels = sameLengthForEachLetter(allData,allLabels,letterCount,letterToOneHot)
print("~~~~~~~~~~~~~~~~")
print("letterCount: "+str(letterCount))
print('allData.shape: '+str(allData.shape))
print('allData[0].shape: '+str(allData[0].shape))
print('allLabels.shape: '+str(allLabels.shape))
