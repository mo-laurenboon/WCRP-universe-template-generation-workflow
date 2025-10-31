

import cmipld
import json
from cmipld.tests.jsonld import organisation
from pydantic import  ValidationError


repopath = './src-data/organisation/'


def get_institution(ror, acronym):

    mytype = 'institution'

    ror_template = 'https://api.ror.org/organizations/{}'

    url = ror_template.format(ror)

    ror_data = cmipld.utils.read_url(url)

    assert ror_data, f"ROR data not found for {ror},{acronym} in {url}. Exiting Now."
    
    # ensure the acronym has no _
    cmip_acronym = acronym.replace('_','-')
    
    
    ror_data =  {
        "id": f"{cmip_acronym.lower()}",
        "type": ['wcrp:organisation',f'wcrp:{mytype}','universal'],
        "validation-key": cmip_acronym,
        "ror": ror_data['id'].split('/')[-1],
        "ui-label": ror_data['name'],
        "url": ror_data.get('links', []) ,
        "established": ror_data.get('established'),
        "kind": ror_data.get('types', [])[0] if ror_data.get('types') else None,
        "labels": [i['label'] for i in ror_data.get('labels', [])],
        "aliases": ror_data.get('aliases', []),
        "acronyms": ror_data.get('acronyms', []),
        "location": {
            "id": f"universal:location/{ror_data['id'].split('/')[-1]}",
            "type": "wcrp:location",
            "lat":  ror_data['addresses'][0].get('lat') if ror_data.get('addresses') else None,
            "lon":  ror_data['addresses'][0].get('lng') if ror_data.get('addresses') else None,
            "city": ror_data['addresses'][0].get('city') if ror_data.get('addresses') else None,
            "country": list(ror_data['country'].values())  if ror_data.get('country') else None
        
        }         
        #  can reverse match consortiums or members from here.    
    }
    
    return ror_data

    


if __name__ == '__main__':
    from p_tqdm import p_map
    import glob
    
    files = glob.glob(repopath+'*.json')
    # print(files)
    
    def update(file):
        
        data = json.load(open(file))
        
        match data:
            case {"type":ldtypes} if 'wcrp:institution' in ldtypes:
                try:
                    data = get_institution(data['ror'],data['validation-key'])
                    organisation.institution(**data)
                except ValidationError as err:
                    return 'institution',data['ror'],data['validation-key'],err.errors()[0]
                    
                
            case {"type":ldtypes} if 'wcrp:consortium' in ldtypes:
                errors = []
                return errors
                
        with open(file,'w') as f:
            json.dump(data,f,indent=4) 
        
    # run on all files
    errors = p_map(update,files)
    errors = [i for i in errors if i]
        
    if errors: 
        from rich.console import Console
        from rich.table import Table
        from rich.text import Text
        console = Console()
            
        console.print(Text("Validation Errors", style="bold red underline"))

        # Create a table
        table = Table(show_header=True, header_style="bold white")
        
        table.add_column("Type", style="bold green")  # Green
        table.add_column("Item", style="bold blue")  # Blue
        table.add_column("Warnings", style="red")  # Red for errors (bullet points)


        for kind,ror,validation_key,err in errors:
            # print('eee',err)
            table.add_row(
                kind,
                f"{ror}: {validation_key}",
                f"[{err['loc'][0]}]:\n {err['msg']}"
            )


        console.print(table)
            
