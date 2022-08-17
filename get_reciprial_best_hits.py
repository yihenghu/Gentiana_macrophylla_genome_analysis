#!/usr/bin/env python2
# -*- coding: utf-8 -*-

"""
Created on 2020/8/15
Author: Yiheng Hu
Email: yihenghu@yeah.net
"""

# in the gene id name, there should be no "-";

import sys
import operator


def get_reciprical_best_hit(input_blast_formt6_file):
    fh = open(input_blast_formt6_file, 'r')

    # read the blast reports
    blast = {}
    for line in fh:
        field = line.strip().split()
        query, target, bit = field[0], field[1], float(field[11])
        if query != target:
            if query not in blast:
                blast[query] = {target: {'line': line, 'bit': bit}}
            else:
                if not blast[query].get(target):
                    blast[query][target] = {'line': line, 'bit': bit}
    fh.close()

    # sort each query by the bit score and mark the best hit
    pair = {}
    for query in sorted(blast):
        hit_sort = sorted([(target, blast[query][target]['bit']) for target in blast[query]],
                          key=operator.itemgetter(1), reverse=True)  # # method 1
        # hit_sort = sorted([(target, blast[query][target]['bit']) for target in blast[query]], key=lambda x:x[1], reverse=True)  # method 2
        # hit_sort = [target for target,bit in hit_sort]
        best_hit = hit_sort[0][0]
        pair[query] = best_hit

    # scroll through %pair to figure out which pairs have recipracal best hits
    good_pair = {}
    for query in sorted(pair):
        best_hit = pair[query]
        if pair.get(best_hit):
            best_hit_hit = pair[best_hit]
            if query == best_hit_hit:
                sort_pair = sorted([query, best_hit])
                good_pair["%s-%s" % (sort_pair[0], sort_pair[1])] = 1

    # print out the results
    for pair in sorted(good_pair):
        query, best_hit = pair.split("-")
        print(blast[query][best_hit]['line'], end='')


def main():
    get_reciprical_best_hit(sys.argv[1])


if __name__ == '__main__':
    if len(sys.argv) == 2:
        main()
    else:
        print('USAGE: python %s input_reciprical_blast_results' % sys.argv[0])

