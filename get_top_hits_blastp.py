#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2020/11/23
Author: Yiheng Hu
Email: yihenghu@yeah.net
"""


import sys


def read_blast(input_blast_format6_result, top_number):
    fr = open(input_blast_format6_result, 'r')
    print('Please make sure the results of blast is original or sorted!')
    print('sort blast result: "sort -k1,1nr -k12,12nr input.blast"')
    blast = {}
    count = 0
    for line in fr:
        query, target = line.strip().split('\t')[:2]
        if query != target:
            if query not in blast:
                blast[query] = line
                count = 1
            else:
                if count < int(top_number):
                    blast[query] += line
                    count += 1
    fr.close()
    return blast


def output_result(blast, output_result_file):
    fw = open(output_result_file, 'w')
    for query in sorted(blast):
        fw.write(blast.get(query))
    fw.close()


def main():
    blast = read_blast(sys.argv[1], sys.argv[2])
    output_result(blast, sys.argv[3])


if __name__ == '__main__':
    if len(sys.argv) != 4:
        print 'USAGE: %s input_blast_format6 top_number output_blast_format6' % sys.argv[0]
    else:
        main()
