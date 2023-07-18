import argparse
import pubchempy as pcp
def test_for_sys(cid):
    print(cid)
parser=argparse.ArgumentParser(description='Test for argparse')
parser.add_argument('--cid','-c',help='cid')
args=parser.parse_args()
if __name__=='__main__':
    try:
        test_for_sys(args.cid)
        c = pcp.Compound.from_cid(int(args.cid))
        print(c.isomeric_smiles)
    except Exception as e:
        print(e)

def smi_tokenizer(smi):
    """
    Tokenize a SMILES molecule or reaction
    """
    import re
    pattern =  "(\[[^\]]+]|Br?|Cl?|N|O|S|P|F|I|b|c|n|o|s|p|\(|\)|\.|=|#|-|\+|\\\\|\/|:|~|@|\?|>|\*|\$|\%[0-9]{2}|[0-9])"
    regex = re.compile(pattern)
    tokens = [token for token in regex.findall(smi)]
    assert smi == ''.join(tokens)
    return ' '.join(tokens)


# lines=open("C:/Users/hydro1/lowen/MolecularTransformer-master/data/TEST/tgt-test.txt").readlines()
# fp=open("C:/Users/hydro1/lowen/MolecularTransformer-master/data/TEST/upload.txt", 'w')
# for s in lines:
#    s=s.replace(' ','')
#    print(s)
#    cid=pcp.get_compounds('{}'.format(s), 'smiles')
#    CID=str(cid)
#    print(CID)
#    fp.write(CID)
#
#    fp.write(s)
# fp.close()
# print(smi.replace(' ',''))


#use cid to find smiles and iupac_name
# c = pcp.Compound.from_cid(5090)
# print(c.molecular_formula)
# print(c.molecular_weight)
# print(c.isomeric_smiles)
# print(c.iupac_name)
#use name and smiles to find cid   and name is iupic.
# results = pcp.get_compounds('Glucose', 'name')
# result1=pcp.get_compounds('Cc1nn(-c2ccc(C(F)(F)F)cc2)cc1C(C)CO', 'smiles')
# result2=pcp.get_compounds('3-(4-methylsulfonylphenyl)-4-phenyl-2H-furan-5-one', 'name')
#
# print(type(result1[0]))
# print('results',results)
# print('result1',result1)
# print('result2',result2)

def get_correct_smiles(smi):
    smi=smi.replace(' ','')
    return smi
c="C C O C C . C N ( C ) C = O . Cl c 1 c c c ( I ) c n 1 . O C 1 C N ( C ( c 2 c c c c c 2 ) c 2 c c c c c 2 ) C 1 . [Cl-] . [H-] . [NH4+] . [Na+]"
a=get_correct_smiles(c)
print(a)

