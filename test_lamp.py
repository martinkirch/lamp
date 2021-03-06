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

# Testcode for LAMP

__author__ = "Aika Terada"

import unittest, sys, datetime
import lamp

D = datetime.datetime.today()
RESULT_FILE = "lamp_test_" + D.strftime("%Y%m%d") + "_" + D.strftime("%H%M%S") + "_result.txt"
LOG_FILE = "lamp_test_" + D.strftime("%Y%m%d") + "_" + D.strftime("%H%M%S") + "_log.txt"

class TestLamp(unittest.TestCase):
	def setUp(self):
		self.csv_file = "sample/sample_item.csv"
		self.flag_file = "sample/sample_expression_over1.csv"
		self.value_file = "sample/sample_expression_value.csv"
		self.sig_level = 0.05
		
	def checkResults( self, csv_file, value_file, method, arity_lim, log_file, true_k, true_lam, true_comb_list ):
		fw = open( RESULT_FILE, 'a+' )
		sys.stdout = fw
		enrich_lst, k, lam, columnid2name \
					= lamp.run( csv_file, value_file, self.sig_level, method, None, arity_lim, log_file, ',' )
		sys.stdout.write("\n\n")
		sys.stdout = sys.__stdout__
		fw.close()
		sys.stderr.write("check minimum support...")
		self.assertEqual(lam, true_lam)
		sys.stderr.write("check correction factor...")
		self.assertEqual(k, true_k)
		sys.stderr.write("\n")
		
		sys.stderr.write("check the significance combinations...\n")
		for comb in enrich_lst:
			detect_set = set()
			for i in comb[0]:
				detect_set.add( columnid2name[i-1] )
			flag = False; true_comb = set(); true_p = -1; true_support = 0; true_score = -1 
			for true_comb, true_p, true_support, true_score in true_comb_list:
				if detect_set.issubset( true_comb ) and true_comb.issubset( detect_set ):
					flag = True
					break
			self.assertTrue( flag )
			self.assertAlmostEqual( comb[1], true_p )
			self.assertEqual( comb[2], true_support )
			self.assertAlmostEqual( comb[3], true_score )
		self.assertEqual( len(enrich_lst), len(true_comb_list) )

	def testFisher(self):
		sys.stderr.write( "\n\n#######################################\n")
		sys.stderr.write( "  Test LAMP using Fisher's exact test\n" )
		sys.stderr.write( "#######################################\n")
		sys.stderr.write( "--- without arity limit ---\n" )
		true_k = 5; true_lam = 5
		true_comb_list = [ tuple( [set(["TF1", "TF2", "TF3"]), 0.00699300699301, 5, 5 ]) ]
		self.checkResults( self.csv_file, self.flag_file, "fisher", -1, LOG_FILE, \
							true_k, true_lam, true_comb_list )
		
		sys.stderr.write( "\n--- arity limit = 2 ---\n" )
		true_k = 7; true_lam = 5
		true_comb_list = [ tuple( [set(["TF1", "TF2"]), 0.00699300699301, 5, 5 ]),
						   tuple( [set(["TF1", "TF3"]), 0.00699300699301, 5, 5 ]),
						   tuple( [set(["TF2", "TF3"]), 0.00699300699301, 5, 5 ]) ]
		self.checkResults( self.csv_file, self.flag_file, "fisher", 2, LOG_FILE, \
							true_k, true_lam, true_comb_list )
		
	def testUTest(self):
		sys.stderr.write( "\n\n#######################################\n")
		sys.stderr.write( "  Test LAMP using Mann-Whitney U-test\n" )
		sys.stderr.write( "#######################################\n")
		sys.stderr.write( "--- without arity limit ---\n" )
		true_k = 5; true_lam = 3
		true_comb_list = [ tuple( [set(["TF1", "TF2", "TF3"]), 0.00602414187918, 5, 2.510727 ]) ]
		self.checkResults( self.csv_file, self.value_file, "u_test", -1, LOG_FILE, \
							true_k, true_lam, true_comb_list )
		
		sys.stderr.write( "\n--- arity limit = 2 ---\n" )
		true_k = 7; true_lam = 3
		true_comb_list = [ tuple( [set(["TF1", "TF2"]), 0.00602414187918, 5, 2.510727 ]),
						   tuple( [set(["TF1", "TF3"]), 0.00602414187918, 5, 2.510727 ]),
						   tuple( [set(["TF2", "TF3"]), 0.00602414187918, 5, 2.510727 ]) ]
		self.checkResults( self.csv_file, self.value_file, "u_test", 2, LOG_FILE, \
						   true_k, true_lam, true_comb_list )

if __name__ == '__main__':
	unittest.main()
