import argparse

import torch
import rdkit
import os
import sys
import cirpy
import pubchempy as pcp


# use cid to find smiles and iupac_name
c = pcp.Compound.from_cid(5090)
print(c.molecular_formula)
print(c.molecular_weight)
print(c.isomeric_smiles)
print(c.iupac_name)
# use name and smiles to find cid   and name is iupic.
results = pcp.get_compounds('Glucose', 'name')
print("results_smiles",results[0].isomeric_smiles)
result1=pcp.get_compounds('Cc1nn(-c2ccc(C(F)(F)F)cc2)cc1C(C)CO', 'smiles')
result2=pcp.get_compounds('3-(4-methylsulfonylphenyl)-4-phenyl-2H-furan-5-one', 'name')

print(type(result1[0]))
print('results',results)
print('result1',result1)
print('result2',result2)
# C17H14O4S
# 314.4
# CS(=O)(=O)C1=CC=C(C=C1)C2=C(C(=O)OC2)C3=CC=CC=C3
# 3-(4-methylsulfonylphenyl)-4-phenyl-2H-furan-5-one
# <class 'pubchempy.Compound'>
# results [Compound(5793)]
# result1 [Compound(58733816)]
# result2 [Compound(5090)]
#
smi="C C N ( C C ) C C . C C O C C . C S ( = O ) ( = O ) Cl . O C C C Br"
print(smi.replace(" ",""))
