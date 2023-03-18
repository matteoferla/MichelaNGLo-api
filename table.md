### Table

A table of followup compounds which can be shown overlayed with their inspiration fragment hits.
These pages can be made with the API by a **priviledged** users (tldr; email matteo for access).


This was not meant to be an official feature, but has become one.
It has one issue: the files are kepts outside.



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