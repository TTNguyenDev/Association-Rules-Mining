from utils.apriori import apriori
from utils.db import fetch_db
import argparse
# import pandas
import csv

def readCSV(path): 
    with open(path, 'r') as f:
        reader = csv.reader(f)
        your_list = list(reader)
    return your_list

def print_results(outputFI, outputAR, orders, apriori, support, confidence):
    print(len(orders))
    rules = apriori['confidence']
    frequency = apriori['support']

    writeFI = open(outputFI,"w")
    print ('\t Frequency Table: items with support greater than {:.2f}% support'.format(support * 100))
    for item_group in frequency:
        previousSize = -1
        for item in item_group:
            size = len(item)
            if size != previousSize:
                previousSize = size
                print(len(item))
                writeFI.write(str(len(item)) + '\r\n')
            print ('{} '.format(item_group[item] / float(len(orders))),)
            writeFI.write(str(item_group[item] / float(len(orders))) + ' ')
            for i in item:
                print(i)
                writeFI.write(i + ' ')
            print('\n')
            writeFI.write('\r\n')
    writeFI.close()

    writeAR = open(outputAR, "w")
    print('\t Associate Rules: rules with confidence greater than or equal to {:.2f}%'.format(confidence * 100))

    for pairs in rules:
        for rule in pairs:
            print ('\t\t {}'.format(rule))
            writeAR.write(rule + "\r\n")

    writeAR.close()

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

data = readCSV(input)
print(data)

print_results(
    outputFI,
    outputAR,
    data,
    apriori(data, support, confidence),
    support,
    confidence
)

