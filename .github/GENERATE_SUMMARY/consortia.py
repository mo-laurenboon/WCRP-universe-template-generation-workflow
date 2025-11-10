import cmipld
from cmipld.utils.ldparse import *
from cmipld.utils.checksum import version

me = __file__.split('/')[-1].replace('.py','')

def run(whoami, path, name, url, io):
    
    url = f'{whoami}:organisation/graph.jsonld'
    
    data = cmipld.get(url,depth=1)['@graph']
    
    summary = name_extract(data,['validation-key','ui-label','url','members'])
    
    
    for i in summary:
        summary[i] = set(summary[i]['members'].keys())
    
    location = f'{path}/{name}_{me}.json'
    return location, me, summary