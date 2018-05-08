import csv
import numpy as np

allData = []
allLabels = []

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
            allData.apend(innerArray)
            zData.append(innerArray)
            innerArray = []
        else:
            innerArray.append(npRow)
zLabels = np.array([0,1]*n)
allLabels.append([0,1]*n)

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
            nData.append(innerArray)
            innerArray = []
        else:
            innerArray.append(npRow)
nLabels = np.array([1,0]*n)
allLabels.append([1,0]*n)
