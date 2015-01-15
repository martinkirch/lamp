#!/usr/bin/env python

"""
USAGE: ./fimi_to_lamp.py fimi_file.dat KEY_ITEM ITEMS_OUTPUT.csv EXPRESSION_OUTPUT.csv
transform a FIMI-style input intro a transactions matrix (ITEMS_OUTPUT.csv)
where KEY_ITEM is removed
transactions that contained KEY_ITEM are flagged as up-regulated in EXPRESSION_OUTPUT.csv
"""

import sys
import operator

def discoverItems(file, output, excludedItem):
	"""
	Reads file, discovers and orders the distinct items, then write them in
	a line (in the discovered order) to output
	excludedItem is ignored from the input
	"""
	
	counter=0
	ranks={}
	
	for line in open(file):
		items=line.split()
		for item in items:
			if item != excludedItem and item not in ranks:
				ranks[item]=counter
				counter+=1
	
	sortedRanks = sorted(ranks.items(), key=operator.itemgetter(1))
	
	output.write("#transaction")
	
	for item in sortedRanks:
		output.write(","+item[0])
	
	output.write("\n")
	
	return ranks

def convertToMatrix(dataset, key, itemsRanks, outmatrix, outexpression):
	outexpression.write("#transaction,contains"+key+"\n")
	
	tid = 0
	for line in open(dataset):
		items=line.split()
		containsKey = False
		
		outmatrix.write(str(tid)+",")
		matrixLine = ["0"]*len(itemsRanks)
		
		for item in items:
			if item == key:
				containsKey = True
			else:
				try:
					matrixLine[itemsRanks[item]] = "1"
				except IndexError:
					print "ahem"
					print item
					print itemsRanks[item]
					print matrixLine
					print itemsRanks
					exit(1)
		
		if containsKey:
			outexpression.write(str(tid)+",1\n")
		else:
			outexpression.write(str(tid)+",0\n")

		outmatrix.write(",".join(matrixLine))
		outmatrix.write("\n")

		tid+=1




if __name__ == "__main__":
	if len (sys.argv) != 5:
		print __doc__
		exit(1)
	else:
		dataset = sys.argv[1]
		key = sys.argv[2]
		outmatrix = open(sys.argv[3],"w")
		outexpression = open(sys.argv[4],"w")
		items = discoverItems(dataset, outmatrix, key)
		convertToMatrix(dataset, key, items, outmatrix, outexpression)
		outmatrix.close()
		outexpression.close()
