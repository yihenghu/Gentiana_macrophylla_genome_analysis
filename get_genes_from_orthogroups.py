#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   get_genes_from_orthogroups.py
@Time    :   2022/07/28 10:23:36
@Author  :   HYH
@Version :   1.0
@Contact :   yihenghu@yeah.net
@License :   (C)Copyright 2022-2023, HYH
@Descrip :   None
'''

# here put the import lib
"""
根据OG的id，输出指定物种的基因拷贝数
query_id参数可以是一个单独的id，也可以是一个包含很多id的文件，每行一个id
"""
import sys
import re
import os

group_file = sys.argv[1]
query_id = sys.argv[2]
species = {'Gmac'}  # {'Acon', 'Afim', 'Aman', 'Atha'}

if os.path.exists(query_id):
    with open(query_id, 'r') as fr:
        query_id = fr.read().splitlines()
else:
    query_id = [query_id]

orthogroups = {}
with open(group_file, "r") as fr:
    for line in fr:
        if not line.startswith("\t"):
            cols = re.split(r'\s+', re.sub(',', ' ', line.rstrip()))
            id_, members = re.sub(r':', '', cols[0]), cols[1:]
            orthogroups[id_] = members

gene_all = []
for id_ in query_id:
    gene_list = []
    members = orthogroups.get(id_)
    if members is None:
        print('%s not found!!!' % id_)
        continue
    for gene in members:
        abb, name = gene.split('|')
        if abb in species:
            gene_list.append(gene)
    # print('%s\t%s' % (id_, ' '.join(sorted(gene_list))))
    gene_all.extend(gene_list)

for gene in gene_all:
    print(gene)