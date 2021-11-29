#-*- coding: UTF-8 -*- 
import os
import sys
import glob
from ssf_api import *
from os import listdir
from os.path import isfile, join
from Word_order import *
from Clause_joining import *


#input_fname = "SSF-FixTrees/ssf{}.txt"
#output_fname = "PS-FixTrees/ps{}.txt"

#input_fname = "data/SSF/ssf{}.txt"
output_fname = "data/PS/ps_{}.txt"
directory= 'data/SSF'

#if not os.path.exists('data/PS'):
 #   os.makedirs('data/PS')

for filepath, dirs, files in os.walk(directory):
    #print("Processing file ssfn{}".format(i))
    for file in files:
        input_fpath=os.path.join(filepath, file)
        input_fname= os.path.splitext(file)[0]
        p = open(output_fname.format(input_fname),'w+')
        ssf = SSF(input_fpath)
        # p = open('output.txt','w+')
        # ssf = SSF('trial.txt')
        for tree in ssf.getTrees():
            # print(tree)
            draw=Join_clauses(tree)
            PS_tree=draw.ps_tree()
            #print(PS_tree+'\n\n')
            p.write(PS_tree+'\n\n')
        p.close()
