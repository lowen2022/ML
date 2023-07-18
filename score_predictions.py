#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division, unicode_literals
import argparse
from rdkit import Chem
import pandas as pd
import onmt.opts
import numpy as np
from numpy import nan as NaN
def canonicalize_smiles(smiles):#get smiles
    mol = Chem.MolFromSmiles(smiles)
    if mol is not None:
        return Chem.MolToSmiles(mol, isomericSmiles=True)
    else:
        return ''

def get_rank(row, base, max_rank):
    for i in range(1, max_rank+1):
        if row['target'] == row['{}{}'.format(base, i)]:
            return i
    return 0

def main(opt):
    with open(opt.targets, 'r') as f:
        targets = [''.join(line.strip().split(' ')) for line in f.readlines()]
        #print("targets",targets) # target=['N#CCC(=O)O']
    #confuse. what means beam_size?
    count_line=len(open(opt.targets, 'rU').readlines())
    print("count_line",count_line)
    opt.beam_size=1
    # if(count_line<opt.beam_size):
    #     opt.beam_size = count_line
    print("opt.beam_size",opt.beam_size)
    #change opt.beam_size if the line of test is less than beam_size
    predictions = [[] for i in range(opt.beam_size)]#[[],[],[],[],[]] while size=5
    print("predictions",predictions)
    test_df = pd.DataFrame(targets)#why do we need so much row rather than targets/beam_size?
    test_df.columns = ['target']
    print("test_df",test_df)# 40000 rows x 1 columns
    total = len(test_df)
    print("total",total)

    with open(opt.predictions, 'r') as f:
        for i, line in enumerate(f.readlines()):

            predictions[i % opt.beam_size].append(''.join(line.strip().split(' ')))#length dose match
            #because of i=0 and beam_size=5  test have only one line. other will be empty
            #[['N#CCC(=O)O'],[],[],[],[]]
            #print("predictions[{}]".format(i % opt.beam_size),predictions[i % opt.beam_size])
    print("len",len(predictions))# 5
    print("len of test_df",len(test_df))#40000
    for i, preds in enumerate(predictions):
        print("i", i)
        print("preds len", len(preds))#8000
        print("preds",preds)
        test_df['prediction_{}'.format(i + 1)] = preds#valueError values does not match index
        #test_df['prediction_{}'.format(i + 1)]=pd.Series(preds)
        test_df['canonical_prediction_{}'.format(i + 1)] = test_df['prediction_{}'.format(i + 1)].apply(
            lambda x: canonicalize_smiles(x))

    test_df['rank'] = test_df.apply(lambda row: get_rank(row, 'canonical_prediction_', opt.beam_size), axis=1)

    correct = 0

    for i in range(1, opt.beam_size+1):
        correct += (test_df['rank'] == i).sum()
        invalid_smiles = (test_df['canonical_prediction_{}'.format(i)] == '').sum()
        if opt.invalid_smiles:
            print('Top-{}: {:.1f}% || Invalid SMILES {:.2f}%'.format(i, correct/total*100,
                                                                     invalid_smiles/total*100))
        else:
            print('Top-{}: {:.1f}%'.format(i, correct / total * 100))



if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='score_predictions.py',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    onmt.opts.add_md_help_argument(parser)

    parser.add_argument('-beam_size', type=int, default=5,
                       help='Beam size')
    parser.add_argument('-invalid_smiles', action="store_true",
                       help='Show % of invalid SMILES')
    parser.add_argument('-predictions', type=str, default="",
                       help="Path to file containing the predictions")
    parser.add_argument('-targets', type=str, default="",
                       help="Path to file containing targets")

    opt = parser.parse_args()
    main(opt)
