import csv
import time
from math import floor

def main(writer):
    t0 = time.time()
    writer.write("Reader: Reader Starts\n")
    print("Reader: Reader Starts")
    retVal = {}
    with open('data.csv', 'r', newline = '', encoding = 'UTF-8') as f:
        csvfile = csv.reader(f)
        for row in csvfile:
            if row[-1] not in retVal:
                retVal[row[-1]] = 1
            else:
                retVal[row[-1]] += 1
    with open('result.csv', 'w', newline = '', encoding = 'UTF-8') as g:
        csvwriter = csv.writer(g)
        total = 0
        for i in retVal:
            total += int(retVal[i])
        for j in retVal:
            csvwriter.writerow([j, retVal[j], retVal[j] / total])
    t1 = time.time()
    writer.write("Reader: DONE!!\nTime Used: %s seconds\n" % (floor(t1 - t0)))
    print("Reader: DONE!!\nTime Used: %s seconds" % (floor(t1 - t0)))
    return retVal
