#!/usr/bin/env python  
# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name:       add_abb_in_fasta.py
   Description:     This script is for ...
   Author:          Yiheng Hu
   Date:            2022/4/8
   Email:           yihenghu@yeah.net
-------------------------------------------------
   Change Activity: 2022/4/8
-------------------------------------------------
"""
__author__ = 'Yiheng Hu'

import argparse
import sys
import re
from Bio import SeqIO
from Bio.SeqRecord import SeqRecord


"""
根据物种的缩写与物种基因组注释中的特征开头字符，对fasta文件中不同物种的基因添加物种缩写
使用此脚本前，请先检查不同物种的基因特征字符是否唯一（），比如在水稻中LOC_*和ChrUn.*都表示为水稻的基因
"""

parse = argparse.ArgumentParser()
parse.add_argument('-i', '--input', type=str, help='The input fasta file')
parse.add_argument('-c', '--char2abb', type=str, help='The fasta name abbreviation')
parse.add_argument('-o', '--output', type=str, help='The output fasta file')
args = parse.parse_args()

fr = open(args.char2abb, 'r')
char2abb = {}
for line in fr:
    cols = line.strip().split('\t')
    char2abb[cols[1]] = cols[0]
fr.close()
# print(char2abb, len(char2abb))

sequence = []
for rec in SeqIO.parse(args.input, 'fasta'):
    name = rec.id
    seqs = rec.seq
    for char in char2abb:
        if name.startswith(char):
            new_name = '%s|%s' % (char2abb.get(char), name)
            break

    sequence.append(SeqRecord(id=new_name, seq=seqs, description=''))

SeqIO.write(sequence, args.output, 'fasta')
