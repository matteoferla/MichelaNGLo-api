### Table

A table of followup compounds which can be shown overlayed with their inspiration fragment hits.
These pages can be made with the API by a **privileged** users (tldr; email matteo for access).


This was not meant to be an official feature, but has become one.
It has a few issues: the files are kept outside and it's rather complicated.
One has to do the following:

* make a sdf files of the hits and a keep a list of the compound names
* make a sdf file of the followups
* make a json file with the metadata, which needs a few keys to be present
* make a js function
* add a call to the js function to the page

```python
from michelanglo_api import MikeAPI
from rdkit import Chem
from typing import List
import pandas as pd
import json

# declare variables
hits: List[Chem.Mol] = [...] # list of hits
hit_filename: str = ... # SDF filename to save the hits to
followups: pd.DataFrame = ... # dataframe of followups
followup_filename: str = ... # SDF filename to save the followups to
metadata_filename: str = ... # JSON filename to save the metadata to
headers = ['name', 'hit_names', 'group', '∆∆G', ...]  # headers to show in the table
base_url = 'https://...'  # base url path
uuid = '...' # uuid of the page target


# Save the hits to a file to upload to a XSS enabled server
hit_names = []
with Chem.SDWriter(hit_filename) as sdw:
    for hit in hits:
        sdw.write(hit)
        
# get the hit names
hit_names = [hit.GetProp('_Name') for hit in hits]

# make model_sdf_urldex and metadata_url

metadata = followups[headers].copy(deep=True)
# make sure the keys do not contain nans
for k in ('∆∆G', 'LE', 'RMSD'):
    metadata[k] = metadata[k].fillna(999).astype(float).round(1)
for k in ('N_interactions', 'N_HA', 'N_rotatable'):
    metadata[k] = metadata[k].fillna(-1).astype(int)

# write the followup_filename
# make sure mols in the SDF have names even if NGL does not keep them...
with Chem.SDWriter(followup_filename) as sdw:
    mol: Chem.Mol
    for name, mol in zip(metadata['name'], metadata.mol):
        mol.SetProp('_Name', name)
        sdw.write(mol)

with open(metadata_filename, 'w') as fh:
    json.dump(dict(
                   headers=headers,
                   data=metadata.values.tolist(),
                   modelnamedex={'prediction': metadata['name'].to_list()},
                   hitnames=hit_names,
            ), fh)
    
# make a page

mike = MikeAPI()
page = mike.get_page(uuid)

page.loadfun = page.get_fragment_js(hit_sdf_url=base_url+hit_filename,
                               model_sdf_urldex={'prediction': base_url+followup_filename},
                               metadata_url=base_url+metadata_filename,
                               model_colordex={'prediction': 'salmon'},
                               hit_color='grey',
                               template_color='gainsboro',
                               name_col_idx = headers.index('name'),
                               hit_col_idx = headers.index('hit_names'),
                               target_col_idx = -1, # headers.index('target')
                               sort_col = headers.index('LE'),
                               sort_dir = 'asc',
                               fun_name ='loadTable')

# create a way to load the protein
# laziest: 
#page.loadfun += 'setTimeout(loadTable, 1000)'
# better:
page.loadfun += """
window.loadprotein = (prot) => {prot.removeAllRepresentations(); 
                                prot.addRepresentation('cartoon');
                                prot.addRepresentation('line', {sele: '454 or ...', colorValue: 'cyan'}); 
                                prot.autoView(); 
                                prot.setName('template');
                                loadTable(); 
                                }
"""
page.proteins[0]['loadFx'] = 'loadprotein'
page.title = '...'
page.description = f'## Predicted followups\n...\n'
page.columns_text = 6
page.commit()
```

The JS template is from `page.fragment_table_template` dynamic attribute.
If each row uses a different template PDB, then `target_col_idx` needs to be specified.
The values need to match a declared protein in the page, 
i.e. `page.proteins.append( dict(name='foo', type='url', value='https://foo.pdb') )`.

## Past
This code has gone through several iterations.
The previous version required multiple separate files —thousands. Not great.

For the Covid Moonshot, I made a few interactive tables with different poses,
_eg._ [Fragmenstein hits](https://michelanglo.sgc.ox.ac.uk/data/13523b58-d0b1-4d05-9158-a8fd2be8465c).


They require GitHub for storing the `mol` files.
Starting with

* `scores` a pandas table containing name, rdkit.Chem.Mol and some scores
* `gitfolder` a str of the file path of the github repo
* `folder` a str of the folder name within that repo

```jupyterpython
targetfolder=f'{gitfolder}/{folder}'
# make a smaller table and json store it
scores['filename'] = page.pandas_to_mols(scores, targetfolder)
headers = ['filename', 'regarded', '∆∆G', 'comRMSD']
mini = scores.loc[~scores.filename.isna()][headers]  # filename None has some issue.
mini.to_json(f'{targetfolder}/data.json')
# make a table
page.make_fragment_table(metadata=dict(zip(headers, ['name', 'used hits', '∆∆G', 'RMSD'],
               username='matteoferla',
               repo_name='Data_for_own_Michelanglo_pages',
               foldername=folder,
               protein_sele='145:A', # show this on protein. NGL selection
               sort_col=2, #sort by column index 2.
               sort_dir='asc', #asc or desc
               template_row=-1, # is the template a file called `template.pdb` (-1) or a filename in the row n?
               fragment_row=1, # the inspiration fragments (-1 for none). The names must match with or without a .mol.
               jsonfile='data.json')
page.commit()
```
Don't forget to git add, commit and push