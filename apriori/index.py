from itertools import chain, combinations
from collections import (defaultdict, Counter)
from optparse import OptionParser
from apriori import runApriori
import argparse
import csv
import sys

def printResults(items, rules, outputFI, outputAR):
    previousSize = -1
    writeFI = open(outputFI,"w")
    items = sorted(items, key=lambda (item, support): len(item))

    count = list()
    for item, support in items:
        count.append(item)
    count = Counter(map(len, count))

    for item, support in items:
        if previousSize != len(item):
            print(count[len(item)])
            writeFI.write(str(count[len(item)]) + "\n")
        previousSize = len(item)
        print "%.2f %s" % (support, str(item)[1:-1])
        writeFI.write("%.2f %s \n" % (support, str(item)[1:-1]))
    writeFI.close()
    
    print "\n------------------------ RULES ------------------------"

    writeAR = open(outputAR, "w")
    previousSize = -1
    rules = sorted(rules, key=lambda((pre, post), confidence): len(pre))

    count = list()
    for rule, confidence in rules:
        pre, post = rule 
        count.append(pre)
    count = Counter(map(len, count))

    for rule, confidence in rules:
        pre, post = rule
        if previousSize != len(pre):
            print(count[len(pre)])
            writeAR.write(str(count[len(pre)]) + "\n")
        previousSize = len(pre)
       
        print "%.2f %s ==> %s" % (confidence, str(pre)[1:-1], str(post)[1:-1])
        writeAR.write("%.2f %s ==> %s \n" % (confidence, str(pre)[1:-1], str(post)[1:-1]))

def readCSV(path): 
    with open(path, 'r') as f:
        reader = csv.reader(f)
        your_list = list(reader)
        attributesName = your_list[0]
        del your_list[0]
        dataAfter = list()

        for itemSet in your_list:
            temp = list()
            for index, item in enumerate(itemSet):
                if item == 'y':
                    temp.append(attributesName[index])
            dataAfter.append(temp)
    print(dataAfter)
    return dataAfter

# main function
parser=argparse.ArgumentParser()
parser.add_argument('--input', help='Name of csv file')
parser.add_argument('--outputFI', help='FI')
parser.add_argument('--outputAR', help='AR')
parser.add_argument('--support', help='Support threshold')
parser.add_argument('--confidence', help='Confidence threshold')

args=parser.parse_args()
input = args.input
outputFI = args.outputFI
outputAR = args.outputAR
support = float(args.support) if args.support is not None else .5
confidence = float(args.confidence) if args.confidence is not None else .5

#preprogress data
data = readCSV(input)
items, rules = runApriori(data, support, confidence)

printResults(items, rules, outputFI, outputAR)
