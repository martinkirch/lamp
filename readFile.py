#!/usr/bin/env python

"""
Copyright (c) 2013, LAMP development team
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:
    * Redistributions of source code must retain the above copyright
      notice, this list of conditions and the following disclaimer.
    * Redistributions in binary form must reproduce the above copyright
      notice, this list of conditions and the following disclaimer in the
      documentation and/or other materials provided with the distribution.
    * Neither the name of the LAMP development team nor the
      names of its contributors may be used to endorse or promote products
      derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL LAMP DEVELOPMENT TEAM BE LIABLE FOR ANY
DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""

# Define methods to read transaction and flag files
# @author Terada 26, June, 2011
# @editor aika 1, Nov. 2011
#    Developing the readValueFile for handling the value.
# @editor aika 10, Nov. 2011
#    Change readTransactionFile. If file has space the front and the end, remove them.
# @editor aika, 11, Mar. 2014
#    Change readFiles for keeping transaction ID.
# @editor Martin Kirchgessner, 15, Jan. 2015
#    readFiles now reads a FIMI-like dataset, with a key item that's used as 1-flag in Fisher's test.
#    column to names map is now provided as a side-input

import sys, transaction, csv


def readFiles(transaction_file, value_file, key):
	"""
	Reads FIMI-like transaction_file
	value_file is a space/tab-separated text file giving (col name, ID)
	key is an integer item ID that will be ommited in transactions and used as a value flag (1/0)
	"""
	transaction_list = []
	#gene2id = {} # dictionary that gene name -> transaction ID
	columnid2name = [] # list about mapping column id to column name
	itemsMap = {}
	itemCounter = 0
	for line in open(value_file):
		(artist,num)=line.split()
		if int(num) != key:
			itemsMap[num] = itemCounter
			columnid2name.append(artist)
			itemCounter += 1
	
	sys.stderr.write("Last ID from %s: %d\n" % (value_file, itemCounter-1))
	
	tid = 0
	for line in open(transaction_file):
		items=line.split()
		t = transaction.Transaction(tid)
		t.setID(tid)
		tid += 1
		t.setValue(0)
		for item in items:
			i = int(item)
			if i == key:
				t.setValue(1)
			else:
				i=itemsMap[item]
				t.addItem(i)
		transaction_list.append(t)
	
	sys.stderr.write("Loaded %d transactions from %s\n" % (len(transaction_list), transaction_file))
	
	sys.stderr.write(columnid2name.__str__())
	#transaction_list, gene2id, columnid2name = readTransactionFile(transaction_file, delm)
	#transaction_list = readValueFile(value_file, transaction_list, gene2id, delm)
	transaction_list.sort() # sort transaction_list according to transaction_value
	# Generate IDs to transactions
	#for i in xrange( 0, len(transaction_list) ):
	#	t = transaction_list[i]
	#	t.id = i
	# check transaction names two
	#checkTransName(transaction_list, transaction_file) # check transaction names two
	return transaction_list, columnid2name
