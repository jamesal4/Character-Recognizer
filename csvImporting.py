import csv
import numpy as np

data = []
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
            trainData.append(innerArray)
            innerArray = []
        else:
            innerArray.append(npRow)
labels = np.array(["N"]*n)
