import sys
# from pathlib import Path
# set the path to read local files 
# sys.path.append(str(Path(--file--).parent))

import json,os
from cmipld.utils import git
from  cmipld.tests import jsonld as tests
from cmipld.utils.json import sorted_json
from collections import OrderedDict

from cmipld import reverse_mapping

rmap = reverse_mapping()
prefix = rmap[git.url2io(git.url())]




def run(issue,packet):
    # print('issue',issue)
    
    # also breaks the issue updates for the same reason 
    git.update_summary(f"### Issue content\n ```json\n{json.dumps(issue,indent=4)}\n```")
    path = f'./src-data/{issue['issue-type']}/'
    
    acronym = issue['activity-id']
    id = acronym.lower()
    
    outfile = path+id+'.json'
    
    # check if the file already exists
    mainfiles = git.getfilenames('main')
    if outfile in mainfiles:
        git.close_issue(f'File {outfile} already exists, please check and correct. ')
        sys.exit('File already exists on main')
    
    title = f'New {issue["issue-type"].capitalize()}  {acronym}'
    branch = title.replace(' ','_').lower()
    
    git.update_issue_title(title)
    git.newbranch(branch)
    os.popen(f"git checkout {branch}")
    
    git.update_summary(f"### Branch created: {branch}, {os.popen('git branch').read()}")
    
    gb = git.getbranch()
    assert gb == branch, f'the branch is not the same (not created) "{gb}" != "{branch}"'
    
    
    data = {
            "id": f"{id}",
            "type": [f'wcrp:{issue['issue-type']}',prefix],
            
            "validation-key": acronym,    
            "ui-label": issue['activity-title'],
            "description": issue['description'],
            "url": issue['activity-webpage-/-citation']
        }   

        
    data = sorted_json(data)

    git.update_summary(f"### Data content\n ```json\n{json.dumps(data,indent=4)}\n```")
    
    # tests.run_checks(tests.activity.activity_model,data)
    
    git.update_summary(f"### Content has no errors. \n```")


    print('writing to',outfile)
    json.dump(data,open(outfile,'w'),indent=4)
    print('done')


    
    # if we are happy, and have gotten this far: 
    
    if 'submitter' in issue:  # override the current author
        author = issue['submitter']
        author = {'name':author,'login':f"{author}@users.noreply.github.com"}
    else:
        author = git.issue_author(os.environ['ISSUE_NUMBER'])

    print('Author',author)
    
    
    # git.commit-override-author(acronym,issue["issue-type"])
    git.commit_one(outfile,author,comment=f'New entry {acronym} in {issue["issue-type"]} files.' ,branch=branch)
    print('CREATING PULL\n',branch, author,title,os.environ['ISSUE_NUMBER'])
    
    git.newpull(branch,author,json.dumps(data,indent=4),title,os.environ['ISSUE_NUMBER'])
    
    
        
    
