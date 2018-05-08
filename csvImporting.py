import csv
import numpy as np

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
            zData.append(innerArray)
            innerArray = []
        else:
            innerArray.append(npRow)
zLabels = np.array(["Z"]*n)

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
nLabels = np.array(["N"]*n)
