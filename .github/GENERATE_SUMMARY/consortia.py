import cmipld
from cmipld.utils.ldparse import *
from cmipld.utils.checksum import version

me = __file__.split('/')[-1].replace('.py','')

def run(localhost,whoami,repopath,reponame):

    url = f'{localhost}/{whoami}/organisation/graph.jsonld'
    ctx = f'{localhost}/{whoami}/organisation/_context_'
    
    frame = {
        "@context": ctx,
        "@type": "wcrp:consortium"
    }
    
    data = cmipld.jsonld.frame(url,frame)["@graph"]
    
    summary = name_extract(data,['validation-key','ui-label','url','members'])
    
    
    for i in summary:
        summary[i] = set(summary[i]['members'].keys())
    
    location = f'{repopath}/{reponame}_{me}.json'
    summary = version(summary, me, location.split("/")[-1])
    cmipld.utils.io.wjsn(summary,location)