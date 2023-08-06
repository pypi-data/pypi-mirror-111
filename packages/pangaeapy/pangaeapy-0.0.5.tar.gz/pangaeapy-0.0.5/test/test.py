import sys

from pangaeapy import PanDataSet, PanQuery
import re
import requests

def is_gbif_dataset(doi: str):
    gbifapiurl = 'https://api.gbif.org/v1/dataset/doi/'
    ret = False
    if type(doi) == str:
        if doi.startswith('10.') or doi.startswith('doi:10.'):
            if doi.startswith('doi:'):
                doi= doi.replace('doi:','')
            r = requests.get(gbifapiurl+doi)
            if r.status_code == 200:
                gbifjson = r.json()
                if gbifjson.get('results'):
                    if len(gbifjson.get('results'))>0:
                        print('SUCCESS: '+doi)
                        ret = True
                    else:
                        ret = False
                        print('FAIL: '+doi)
                else:
                    print('FAIL: '+doi)
            else:
                print(r.status_code)
        else:
            print('invalid doi')
    else:
        print('DOI has to be a string')
    return ret



totalcount = 10000000000
position = offset = 0
limit = 100
nontaggedparams=[]

ingbif=[]

while position+offset < totalcount:
    pq = PanQuery(query='project:OA-ICC', offset =offset, limit=limit)
    res = pq.result
    totalcount = int(pq.totalcount)
    print('Totalcount'+str(totalcount))
    print(offset, limit)
    for result in res:
        print(result.get('position'),result.get('URI'))
        if is_gbif_dataset(result.get('URI')):
            ingbif.append(result.get('URI'))
        position = result.get('position')
        if result.get('type')=='parent':
            print('Parent')
        else:
            ds = PanDataSet(result.get('URI'), include_data=False)
            dsterms =[]
            for paramkey, paramvalue in ds.params.items():
                # print(paramvalue.terms)
                if paramvalue.terms == []:
                    if paramvalue.name not in nontaggedparams:
                        nontaggedparams.append(paramvalue.name)
                for term in paramvalue.terms:
                    if term.get('ontology') in [1, 2]:
                        if term.get('name') not in dsterms:
                            if len(term.get('name').split()) >1:
                                dsterms.append(term.get('name'))
            if len(dsterms) > 0:
                print(dsterms)
    offset = offset + limit

print(nontaggedparams)
print(ingbif)
print(len(ingbif))

'''
ds = PanDataSet('10.1594/PANGAEA.758344',include_data=False)
#ds.info()
for paramkey, paramvalue in ds.params.items():
    #print(paramvalue.terms)
    if paramvalue.terms == []:
        print('###########')
        print(paramvalue.name)
    for term in paramvalue.terms:
        #print(term)
        if term.get('ontology') in [1,2]:
            print(term)
'''