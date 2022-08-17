#!/usr/bin/env python2
# -*- coding: utf-8 -*-

"""
Created on 2020/5/10
@author: Yiheng Hu
e-mail: yihenghu@yeah.net
"""

import os
import re
import sys
import glob
import subprocess
from Bio import SeqIO
from itertools import islice


def runCMD(cmd):
    child = subprocess.Popen(cmd, shell=True)
    child.wait()


def readGroup(input_group):
    """
    read orthogroup of orthoMCL or orthoFinder
    :param input_group:
    :return {OG1:[geneA1,geneB1,geneC1],OG2:[geneA2,geneB2]}:
    """
    orthogroups = {}
    with open(input_group, "r") as OGs:
        for og in islice(OGs, 0, None):  # modified
            og = re.split(r'\s+', re.sub(',', ' ', og.rstrip()))
            ogID, ogGenes = re.sub(':', '', og[0]), og[1:]
            if len(ogGenes) >= 1:  # 注意此处筛选了OG成员小于4的
                orthogroups[ogID] = ogGenes
    return orthogroups


def readFasta(input_fasta_dir):
    """
    read all fasta in a dict
    :param input_fasta_dir:
    :return big_dict:
    """
    genes = {}
    for sp in glob.glob("%s/*.fasta" % input_fasta_dir):
        for rec in SeqIO.parse(sp, 'fasta'):
            genes[rec.id] = str(rec.seq)
    return genes


def outAllOGs(orthogroups, genes, output_dir, seq_type):
    """
    writ OGs file in outputdir
    :param orthogroups:
    :param genes:
    :param output_dir:
    :return:
    """
    if os.path.exists(output_dir) == False:
        cmd = 'mkdir ' + output_dir
        runCMD(cmd)
        print('Creating output directory:', output_dir, '...\n')
    else:
        print('Writing to existing output directory:', output_dir, '...\n')

    for og in orthogroups:
        with open("%s/%s.%s.fasta" % (output_dir, og, seq_type), 'w') as fw:
            for gene in orthogroups[og]:
                if gene != 'None': # modified by HYH 2020.04.30
                    fw.write('>' + gene + '\n' + genes.get(gene) + '\n')


def main():
    orthogroups = readGroup(sys.argv[1])
    genes = readFasta(sys.argv[2])
    outAllOGs(orthogroups, genes, sys.argv[3], sys.argv[4])


if __name__ == '__main__':
    if len(sys.argv) != 5:
        print('USAGE: python %s groups.txt input_pep_dir output_dir seq_type' % sys.argv[0])
    else:
        main()



