from email import header


#!/usr/bin/env python
# -*- encoding: utf-8 -*-

'''
@File    :   get_expansions_in_CAFE.py
@Time    :   2022/08/14 10:12:11
@Author  :   HYH
@Version :   1.0
@Contact :   yihenghu@yeah.net
@License :   (C)Copyright 2022-2023, HYH
@Descrip :   None
'''

# here put the import lib
import sys
import re

fams = open(sys.argv[1], 'r')
species = sys.argv[2]
output = sys.argv[3]

for n, line in enumerate(fams):
    if n <= 1:
        continue
    else:
        if line.startswith(species):  # Gmac
            cols = line.strip().split('\t')
            families = cols[1].split(',')
            expansions = []
            for fam in families:
                symbol = re.search(r'\[([+-])', fam).group(1)
                if symbol == '+':
                    id_ = int(re.search(r'(\d+)\[', fam).group(1))
                    id_ = 'OG%07d' % (id_ - 1)
                    expansions.append(id_)
            break
fams.close()

fw = open(output, 'w')
for id_ in expansions:
    fw.write(id_ + '\n')
fw.close()