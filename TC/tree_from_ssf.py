#!/usr/local/bin/python
# -*- coding: utf-8 -*-

# Script to draw trees given bracketed strings
from nltk import *
from nltk.tree import Tree
from nltk.corpus import *
from nltk import treetransforms, bracket_parse
from copy import deepcopy
import re, sys, os
# import nltk_tgrep
from nltk.draw.util import CanvasFrame
from nltk.draw import TreeWidget

import sys, codecs, optparse

import chardet

LR_BRACES = ['(', ')']


def remove_unary(tree):
    if isinstance(tree, Tree) and len(tree) == 1:
        nodeList = [tree[0]]
    else:
        nodeList = [tree]
    # depth-first traversal of tree
    while nodeList != []:
        node = nodeList.pop()
        if isinstance(node, Tree):
            if len(node) == 1 and isinstance(node[0], Tree):
                node.set_label(node[0].label())
                node[0:] = [child for child in node[0]]
                nodeList.append(node)
            else:
                for child in node:
                    nodeList.append(child)


def remove_null(tree):
    for ind, leaf in reversed(list(enumerate(tree.leaves()))):
        if leaf.endswith("**"): #or leaf.endswith("NULL"): or leaf[-1].isdigit():
            postn = tree.leaf_treeposition(ind)
            parentpos = postn[:-1]
            while parentpos and len(tree[parentpos]) == 1:
                postn = parentpos
                parentpos = postn[:-1]
            del tree[postn]

# If a tree doesn't have S as it's root, add extra S as the head root
def add_extra_S(treestr):
    tree = Tree.fromstring(treestr)
    root = tree.label()
    if (root != '.S'):
        s = "(.S " + treestr + ")"
        return s
    else:
        return treestr


# Replaces all left-right braces to LB, RB
# Then change () to [] for tree processing
def replace_allbraces(filename,out_filename):
    try:
        with open(filename, 'r', encoding="utf-8") as infile:
            contents = infile.read()
            if any(x in contents for x in LR_BRACES):
                contents = contents.replace('(', 'LB')
                contents = contents.replace(')', 'RB')
            contents = contents.replace('[', '(')
            contents = contents.replace(']', ')')
        with open(out_filename, 'w', encoding="utf-8") as outfile:
            outfile.write(contents)
    except Exception as e:
        print(e)

#input_fname = "PS-FixTrees/ps{}.txt"
#intermediate_fname = "PS-FixTrees-Braces/ps{}.txt"
#output_fname = "FixedTree_Outputs/tree_s{}.txt"

input_dir = "data/PS"
intermediate_fname = "data/PS-Braces/{}.txt"
output_fname = "data/TC/tree_{}.txt"

#if not os.path.exists('data/TC'):
#    os.makedirs('data/TC')

for filepath, dirs, files in os.walk(input_dir):
    try:
        for file in files:
            print(file)
            in_fname = os.path.splitext(file)[0]
            in_fpath=os.path.join(filepath, file)
            mid_fname=intermediate_fname.format(in_fname)
            replace_allbraces(in_fpath, mid_fname)
    except Exception as e:
        print(e)

print("Replaced all braces")



print("Starting tree processing")
for filepath, dirs, files in os.walk('data/PS-Braces'):
    for file in files:
        fname=os.path.splitext(file)[0]
        in_fpath=os.path.join(filepath, file)
        p = open(in_fpath, 'r', encoding="utf-8")
        #sys.stdout = open(output_fname.format(i) , "w+", encoding="utf-8")
        q = open(output_fname.format(fname) , "w+", encoding="utf-8")
        for line in p:
            if line == "\n":
                continue
            else:
                newtree = add_extra_S(line)
                tree = Tree.fromstring(newtree)
                remove_null(tree)
                remove_unary(tree)
                #tree.draw()
                #print(tree)
                parse_string = ' '.join(str(tree).split()) 
                #print(parse_string)
                q.write(parse_string+'\n')
sys.stdout.close()
