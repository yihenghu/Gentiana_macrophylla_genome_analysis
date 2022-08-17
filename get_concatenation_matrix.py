#!/usr/bin/env python  
# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name:       get_concatenation_matrix.py
   Description:     This script is for ...
   Author:          Yiheng Hu
   Date:            2021/7/21
   Email:           yihenghu@yeah.net
-------------------------------------------------
   Change Activity: 2021/7/21
-------------------------------------------------
"""
__author__ = 'Yiheng Hu'

import sys
import re
from Bio import SeqIO

"""
根据单个基因的mas结果，将单个基因串联为supermatrix
"""

msa_file = sys.argv[1]

msa = open(msa_file, 'r')
og2name = {re.search(r"(OG\d+)", line).group(1): line.strip() for line in msa}
msa.close()
print(og2name)

og2gene2seq = {}
for og in og2name:
    og2gene2seq[og] = \
        {re.search(r"(.*)?\|", rec.id).group(1): str(rec.seq) for rec in
         SeqIO.parse(og2name.get(og), "fasta")}

# 获得物种名称，因为不是绝对单拷贝的数据，考虑到有的OGs会缺少个别物种，因此把所有OGs中的物种名都拿出来，然后去重，就能保证每个物种都不会漏
species_name_set = []
for seq_record in og2gene2seq.values():
    species_name_set += seq_record.keys()
species_name_set = sorted(set(species_name_set))
print(species_name_set)

def super_matrix(og2gene2seq, sp):
    sequence = ""
    for og, seq_record in sorted(og2gene2seq.items(), key=lambda x:x[0]):
        length = len(list(seq_record.values())[0])
        if sp in seq_record.keys():
            sequence += seq_record[sp]
        else:
            sequence += length * "-"
    return sequence


# 输出fasta格式的单拷贝orthogroup的supermatrix
with open("supermatrix_%sOG.fasta" % len(og2name), "w") as fw:
    for sp in species_name_set:
        sequence = super_matrix(og2gene2seq, sp)
        fw.write(">" + sp + "\n" + sequence + "\n")

# 输出phylip格式的单拷贝orthogroup的supermatrix
with open("supermatrix_%sOG.phy" % len(og2name), "w") as fw:
    # header
    length = 0
    for og, seq_record in sorted(og2gene2seq.items(), key=lambda x:x[0]):
        seq_len = len(list(seq_record.values())[0])
        length += seq_len
    fw.write(str(len(species_name_set)) + "\t" + str(length) + "\n")
    # sequence
    for sp in species_name_set:
        sequence = super_matrix(og2gene2seq, sp)
        fw.write(sp + "\t" + sequence + "\n")

count = 1
with open('supermatrix_%sOG.partition.nex' % len(og2name), 'w') as f:
    f.write("#nexus\n\nbegin sets;\n")
    for og, genes in sorted(og2gene2seq.items(), key=lambda x:x[0]):
        f.write('\tcharset ' + '%s' % og + ' = ' + str(count) + '-' + str(count + len(list(genes.values())[0]) - 1) + ';\n')
        count += len(list(genes.values())[0])
    f.write("\nend;\n")

count = 1
with open('supermatrix_%sOG.partition.codon.nex' % len(og2name), 'w') as f:
    f.write("#nexus\n\nbegin sets;\n")
    for og, genes in sorted(og2gene2seq.items(), key=lambda x:x[0]):
        for n in [1, 2, 3]:
            f.write('\tcharset ' + '%s_pos%s' % (og, n) + ' = ' + str(count + n - 1) + '-' +
                    str(count + len(list(genes.values())[0]) - 1) + '\\3;\n')
        count += len(list(genes.values())[0])
    f.write("\nend;\n")

