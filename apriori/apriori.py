from itertools import chain, combinations
from collections import defaultdict
import sys
import csv

def returnItemsWithMinSupport(itemSet, transactionList, minSup, freqSet):
        _itemSet = set()
        localSet = defaultdict(int)

        for item in itemSet:
                for transaction in transactionList:
                        if item.issubset(transaction):
                                freqSet[item] += 1
                                localSet[item] += 1

        for item, count in localSet.items():
                support = float(count)/len(transactionList)

                if support >= minSup:
                        _itemSet.add(item)

        return _itemSet

def getItemSetTransactionList(data_iterator):
    transactionList = list()
    itemSet = set()
    for record in data_iterator:
        transaction = frozenset(record)
        transactionList.append(transaction)
        for item in transaction:
            itemSet.add(frozenset([item]))             
    return itemSet, transactionList


def runApriori(data_iter, minSupport, minConf):
    itemSet, transactionList = getItemSetTransactionList(data_iter)

    freqSet = defaultdict(int)
    largeSet = dict()

    assocRules = dict()
    oneCSet = returnItemsWithMinSupport(itemSet,
                                        transactionList,
                                        minSupport,
                                        freqSet)

    currentLSet = oneCSet
    k = 2
    while(currentLSet != set([])):
        largeSet[k-1] = currentLSet
        currentLSet = set([i.union(j) for i in currentLSet for j in currentLSet if len(i.union(j)) == k])
        currentCSet = returnItemsWithMinSupport(currentLSet,
                                                transactionList,
                                                minSupport,
                                                freqSet)
        currentLSet = currentCSet
        k = k + 1

    def getSup(item):
            return float(freqSet[item])/len(transactionList)

    toRetItems = []
    for key, value in largeSet.items():
        toRetItems.extend([(tuple(item), getSup(item))
                           for item in value])

    toRetRules = []
    for key, value in largeSet.items()[1:]:
        for item in value:
            subsets = chain(*[combinations(item, i + 1) for i, a in enumerate(item)])
            _subsets = map(frozenset, [x for x in subsets])
            for element in _subsets:
                remain = item.difference(element)
                if len(remain) > 0:
                    confidence = getSup(item)/getSup(element)
                    if confidence >= minConf:
                        toRetRules.append(((tuple(element), tuple(remain)),
                                           confidence))
    return toRetItems, toRetRules
