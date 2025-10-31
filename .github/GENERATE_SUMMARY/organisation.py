import cmipld
from cmipld.utils.ldparse import *
from cmipld.utils.checksum import version

me = __file__.split('/')[-1].replace('.py','')

def run(localhost,whoami,repopath,reponame):

    url = f'{localhost}/{whoami}/{me}/graph.jsonld'
    ctx = f'{localhost}/{whoami}/{me}/_context_'
    
    frame = {
        "@context": ctx,
        "@type": "wcrp:organisation"
    }
    
    
    data = cmipld.jsonld.frame(url,frame)["@graph"]
    
    summary = name_entry(data,'ui-label')
    
    location = f'{repopath}/{reponame}_{me}.json'
    summary = version(summary, me, location.split("/")[-1])
    cmipld.utils.io.wjsn(summary,location)