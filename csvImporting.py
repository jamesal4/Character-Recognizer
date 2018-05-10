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
            allData.append(innerArray)
            zData.append(innerArray)
            innerArray = []
        else:
            innerArray.append(npRow)
zLabels = np.array([[0,1,0]]*n)
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
            allData.append(innerArray)
            nData.append(innerArray)
            innerArray = []
        else:
            innerArray.append(npRow)
nLabels = np.array([[1,0,0]]*n)
allLabels.extend(nLabels)

# aData = []
# n = 0
# with open('JamesA.csv') as csvfile:
#     reader = csv.reader(csvfile)
#     innerArray = []
#     for row in reader:
#         if row[0] == "Time":
#             continue
#         npRow = np.array(row[:-1],dtype=np.float32)[1:]
#         if npRow.all() == np.zeros(6).all():
#             n += 1
#             allData.append(innerArray)
#             aData.append(innerArray)
#             innerArray = []
#         else:
#             innerArray.append(npRow)
# aLabels = np.array([[0,0,1]]*n)
# allLabels.extend(nLabels)

vData = []
n = 0
with open('JamesV.csv') as csvfile:
    reader = csv.reader(csvfile)
    innerArray = []
    for row in reader:
        if row[0] == "Time":
            continue
        npRow = np.array(row[:-1],dtype=np.float32)[1:]
        if npRow.all() == np.zeros(6).all():
            n += 1
            allData.append(innerArray)
            vData.append(innerArray)
            innerArray = []
        else:
            innerArray.append(npRow)
nLabels = np.array([[1,0,0]]*n)
allLabels.extend(nLabels)

allData = np.array(allData)
allLabels = np.array(allLabels)
