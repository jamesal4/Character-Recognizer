import csv
import numpy as np

#TODO: Automate this from an array of letters
letters = ["A","N","Z"]
allData = []
allLabels = []

# for i in range(len(letters)):
#     n = 0
#     letter = letters[i]
#     with open('James'+letter+'.csv') as csvfile:
#         reader = csv.reader(csvfile)
#         innerArray = []
#         for row in reader:
#             if row[0] == "Time":
#                 continue
#             npRow = np.array(row[:-1],dtype=np.float32)[1:]
#             if npRow.all() == np.zeros(6).all():
#                 n += 1
#                 allData.append(innerArray)
#                 innerArray = []
#             else:
#                 innerArray.append(npRow)
#     oneHot = [0]*len(letters)
#     oneHot[i] = 1
#     labels = np.array([oneHot]*n)
#     allLabels.extend(labels)

zData = []
n = 0
with open('JamesZ.csv') as csvfile:
    reader = csv.reader(csvfile)
    innerArray = []
    for row in reader:
        if row[0] == "Time":
            continue
        npRow = np.array(row[:-1],dtype=np.float32)[1:]
        if npRow.all() == np.zeros(6).all():
            n += 1
            allData.append(np.array(innerArray))
            zData.append(innerArray)
            innerArray = []
        else:
            innerArray.append(npRow)
zLabels = np.array([[1,0,0,0]]*n)
allLabels.extend(zLabels)

nData = []
n = 0
with open('JamesN.csv') as csvfile:
    reader = csv.reader(csvfile)
    innerArray = []
    for row in reader:
        if row[0] == "Time":
            continue
        npRow = np.array(row[:-1],dtype=np.float32)[1:]
        if npRow.all() == np.zeros(6).all():
            n += 1
            allData.append(np.array(innerArray))
            nData.append(innerArray)
            innerArray = []
        else:
            innerArray.append(npRow)
nLabels = np.array([[0,1,0,0]]*n)
allLabels.extend(nLabels)

aData = []
n = 0
with open('JamesA.csv') as csvfile:
    reader = csv.reader(csvfile)
    innerArray = []
    for row in reader:
        if row[0] == "Time":
            continue
        npRow = np.array(row[:-1],dtype=np.float32)[1:]
        if npRow.all() == np.zeros(6).all():
            n += 1
            allData.append(np.array(innerArray))
            aData.append(innerArray)
            innerArray = []
        else:
            innerArray.append(npRow)
aLabels = np.array([[0,0,1,0]]*n)
allLabels.extend(nLabels)

vData = []
n = 0
with open('KevinV.csv') as csvfile:
    reader = csv.reader(csvfile)
    innerArray = []
    for row in reader:
        if row[0] == "Time":
            continue
        npRow = np.array(row[:-1],dtype=np.float32)[1:]
        if npRow.all() == np.zeros(6).all():
            allData.append(np.array(innerArray))
            vData.append(innerArray)
            innerArray = []
        else:
            innerArray.append(npRow)
n = 50
allData = allData[0:200] #remove last data point since 51 instead of 50
nLabels = np.array([[0,0,0,1]]*n)
allLabels.extend(nLabels)



allData = np.array(allData)
allLabels = np.array(allLabels)

def getLengthOfLongestExample(data):
    maxLength = 0
    for point in data:
        length = point.shape[0]
        if length > maxLength:
            maxLength = length
    return maxLength

def padExamplesToLength(length,data):
    newData = []
    for point in data:
        pointLen = point.shape[0]
        zeros = np.tile(np.zeros(6),(length-pointLen,1))
        newPoint = np.concatenate((point,zeros))
        newData.append(newPoint)
    return np.array(newData)



maxLen = getLengthOfLongestExample(allData)
allData = padExamplesToLength(maxLen,allData)

print('allData.shape: '+str(allData.shape))
print('allData[0].shape: '+str(allData[0].shape))
print('allLabels.shape: '+str(allLabels.shape))
