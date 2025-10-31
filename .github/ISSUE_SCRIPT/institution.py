import sys
from pathlib import Path
# set the path to read update_ror. 
sys.path.append(str(Path(__file__).parent))

import update_ror
import json,os
from cmipld.utils import git
from  cmipld.tests import jsonld as tests
from cmipld.tests.jsonld.organisation import ror


path = './src-data/organisation/'


def similarity(name1, name2):
    '''
    This function looks at the similarity between two strings and returns a percentage similarity.
    
    NB Difflib should come bundled with the standard python pagages e.g. conda
    '''
    from difflib import SequenceMatcher
    
    matcher = SequenceMatcher(None, name1, name2)
    similarity = matcher.ratio() * 100

    return similarity




def run(issue,packet):
    # print('issue',issue)
    
    git.update_summary(f"### Issue content\n ```json\n{json.dumps(issue,indent=4)}\n```")
    
    ror = issue['ror']
    acronym = issue['acronym']
    id = acronym.lower()
    

    # update the issue title and create an issue branch
    title = f'{issue["issue-type"].capitalize()}_{acronym}'
    git.update_issue_title(title)
    git.newbranch(title)
    
    acronym_test = tests.field_test(tests.components.id.id_field)
    ror_test = tests.field_test(tests.organisation.ror.ror_field)
    # testclass = tests.multi_field_test([tests.organisation.ror.ror_field,tests.components.id.id_field])
    
    if ror != 'pending':
    
        tests.run_checks(acronym_test,{"id" : id})
        tests.run_checks(ror_test,{"ror" : ror})
        

        data = update_ror.get_institution(ror, acronym)

        ranking = similarity(issue['full-name-of-the-organisation'], data['ui-label'])
        
        git.update_summary(f"### Similarity\nThe similarity between the full name ({issue['full-name-of-the-organisation']}) of the organisation and the ui-label ({data['ui-label']}) is {ranking}%")
        
        
        if ranking < 80:
            git.update_issue(f"*Warning:* \n The similarity between the full name ({issue['full-name-of-the-organisation']}) of the organisation and the ui-label ({data['ui-label']}) is {int(ranking)}%")
            
    else:

        tests.run_checks(acronym_test,{"id" : id})
        
        data = {
                    "id": f"{id}",
                    "type": ['wcrp:organisation',f'wcrp:{issue['issue-type']}','universal'],
                    "validation-key": acronym,    
                }        

    git.update_summary(f"### Data content\n ```json\n{json.dumps(data,indent=4)}\n```")
    
    
    
    
    
    
    
    # write the data to a file

    outfile = path+id+'.json'
    print('writing to',outfile)
    json.dump(data,open(outfile,'w'),indent=4)
    print('done')


    print(os.popen(f"less {outfile}").read())
    
    # git branch commit and push function
    
    # if we are happy, and have gotten this far: 
    
# <<<<<<< update-organizations-from-ror
    # Get the author from the packet (GitHub issue submitter)
    # This is the username of the person who submitted the issue
    author = packet.get('author')
# =======
#     if 'submitter' in issue: 
#         # override the current author
#         os.environ['ISSUE_SUBMITTER'] = issue['submitter']
# >>>>>>> main
    
    # If there's a specific submitter field in the issue form, use that instead
    if 'submitter' in issue and issue['submitter']:
        author = issue['submitter']
    
    # Fallback to environment variable if neither is available
    if not author:
        author = os.environ.get('OVERRIDE_AUTHOR', 'unknown')
    
# <<<<<<< update-organizations-from-ror
    # Set the environment variable for other git operations that might need it
    if author:
        os.environ['OVERRIDE_AUTHOR'] = author
# =======
#     # # add files
#     # git.addall()

#     # git.addfile(outfile)
#     # commmit them

#     author = os.environ.get('ISSUE_SUBMITTER')
# >>>>>>> main
    
    # Commit the file with the correct author
    git.commit_one(outfile, author, comment=f'New entry {acronym} in {issue["issue-type"]} files.', branch=title)
    
    # Create pull request with the same author
    git.newpull(title, author, json.dumps(issue, indent=4), title, os.environ['ISSUE_NUMBER'])
    
    
        
    
