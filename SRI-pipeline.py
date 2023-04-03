#!/usr/bin/env/python
#coding=utf-8

#import argparse
#import os
import sys

def read_annotation_file(annotation):
    geneNumDic = {}
    if annotation[-4:] == "gff3" or annotation[-3:] == "gff":
        formation = 'gff3'
    elif annotation[-3:] == "bed":
        formation = 'bed'
    else:
        print("WARNNING: thr format of annotation file should be 'gff3' or 'bed'! Please check it and rerun.")
        sys.exit()
#    if annotation[-3:] == "bed":
    with open(annotation, 'r') as IN:
        for line in IN:
            if line.startswith('#'):
                pass
            else:
                tmpLst = line.rstrip().split('\t')
                chrName = tmpLst[0]
                if formation == 'gff3' and tmpLst[2] == 'gene':
                    geneNumPerChr = geneNumDic.setdefault(chrName, 0)
                    geneNumPerChr += 1
                    geneNumDic[chrName] = geneNumPerChr
                elif formation == 'bed':
                    geneNumPerChr = geneNumDic.setdefault(chrName, 0)
                    geneNumPerChr += 1
                    geneNumDic[chrName] = geneNumPerChr
                else:pass
    Total_geneNum = 0
    for Chr in geneNumDic:
        numOfGene = geneNumDic[Chr]
        ## 一条contig上至少要有3个基因才计入总数
        if numOfGene >= 3:
            Total_geneNum += numOfGene
    return Total_geneNum

def read_anchor(anchor_file):
    with open(anchor_file,'r') as IN:
        refAnchorGeneSet = set([])
        qryAnchorGeneSet = set([])
        for line in IN:
            if line.startswith('#'):
                pass
            else:
                refAnchorGeneSet.add(line.split('\t')[0])
                qryAnchorGeneSet.add(line.split('\t')[0])
    numOfRefGene, numOfQryGene= len(list(refAnchorGeneSet)), len(list(qryAnchorGeneSet))
    numOfAnchorGene = numOfRefGene + numOfQryGene
    return numOfAnchorGene

def main(sample_list, output):
    # A.B.lifted.anchord    A.gff3  B,gff3
    syndexDic = {}
    sample_pool = []
    with open(sample_list,'r') as IN:
        for line in IN:
            tmpLst = line.rstrip().split("\t")
            [ABanchor, A_annotation, B_annotation] = tmpLst
            sample_name_set = set(ABanchor.rstrip().split('/')[-1].split('.')[:2])
            #sample_pool.append(set(sample_name_lst))
            if sample_name_set not in sample_pool and len(sample_name_set)>1:
                sample_pool.append(sample_name_set)
                num_of_anchor_gene = read_anchor(ABanchor)
                num_of_A_gene = read_annotation_file(A_annotation)
                num_of_B_gene = read_annotation_file(B_annotation)
                syndex = float(num_of_anchor_gene)/float(num_of_A_gene + num_of_B_gene)
                sample_name = ",".join(list(sample_name_set))
                syndexDic[sample_name] = "{:.4f}".format(syndex)
    with open("{}.result.txt".format(output), 'w') as OUT:
        OUT.write("#sample_pair\tsyndex\n")
        for sample_pair in syndexDic:
            OUT.write("{}\t{}\n".format(sample_pair, syndexDic[sample_pair]))

if __name__ == "__main__":
    [sample_lst, output] = sys.argv[1:]
    main(sample_lst, output)
