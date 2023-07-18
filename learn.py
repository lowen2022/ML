smi="C 1 C C O C 1 . N # C c 1 c c s c 1 N . O = [N+] ( [O-] ) c 1 c c ( F ) c ( F ) c c 1 F . [H-] . [Na+]"
print(smi.replace(" ",""))

import re
import pubchempy as pcp
import logging
import cirpy

print(cirpy.resolve('79-11-8 ', 'smiles'))

logging.getLogger('pubchempy').setLevel(logging.DEBUG)

# def get_substructure_cas(smiles):
#     cas_rns = []
#     results = pcp.get_synonyms(smiles, 'smiles', searchtype='substructure')
#     for result in results:
#         for syn in result.get('Synonym', []):
#             match = re.match('(\d{2,7}-\d\d-\d)', syn)
#             if match:
#                 cas_rns.append(match.group(1))
#     return cas_rns
# cids = pcp.get_cids('O=C([O-])[O-]', 'smiles', searchtype='substructure')
# # cas_rns = get_substructure_cas('O=C([O-])[O-]')
# # print(len(cas_rns))
# # print(cas_rns[:10])
# print(cids)
