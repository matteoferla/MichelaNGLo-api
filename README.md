# MichelaNGLo-api
A python module to interact with the Michelaɴɢʟo server ([<https://michelanglo.sgc.ox.ac.uk>](<https://michelanglo.sgc.ox.ac.uk>))
programmatically.

> :hammer: The migration is partial. But this repo is not expected to get more TLC for a few months.

## Notes
The details of the requests accepted by Michelaɴɢʟo are described in [its documentation](https://michelanglo.sgc.ox.ac.uk/docs/api).\
You may interact with the server however you please. This code is just to make life easier.

There are three tiers of users. Basic, priviledged, admin. Basic users cannot add JS to the site as this is a security threat
(cookie theft)... And it prevents users from making
[pages that behave maliciously or similar](https://michelanglo.sgc.ox.ac.uk/data/fa3844a8-d7f5-4e84-9540-240f134ba6d1).

## Documentation

### Authenticate
To start, authenticate.

    mike = MikeAPI('username','password')
    
The argument `url` sets other address outside of the SGC one, such as `http://0.0.0.0:8088`.
The password and username can be ommitted, in which case they are either read from the environment variables
 `MICHELANGLO_PASSWORD` and `MICHELANGLO_USERNAME` or the user is prompted.
 
To check all worked `mike.verify_user()`. This will show your `rank` (see [user priviledges in the site](https://michelanglo.sgc.ox.ac.uk/docs/users)).

#### Instance attributes:
* `.url` is 'https://michelanglo.sgc.ox.ac.uk/' unless altered (_e.g._ local version of Michelanglo)
* `.username` is the username
* `.password` is the raw password, so do not share pickles!
* `.visited_pages`, `.owned_pages` and `.public_pages` are lists filled by `.refresh_pages()`
* `.request` is the requests session object.

#### Instance methods:
* `.post(route, data=None, headers=None)` does the requests for other methods...
* `.post_json(route, data=None, headers=None)` as above but decodes the json reply...
* `.login()`. called automatically during initialisation.
* `.verify_user()`. check whether you are still logged in.
* `.refresh_pages()`. gets the lists `.visited_pages`, `.owned_pages` and `.public_pages` (and `.all` if admin)
* `.get_page(uuid)` returns the `MikePage` instance for a given page. See below.
* `.set_page(uuid, data)` sets the `MikePage` instance for a given page.  See below.
* `.delete_page(uuid)` delete.  See below.


### Page editing

To see what pages you own, you can use:

* `mike.owned_pages` Pages you created/edited
* `mike.visited_pages` Pages you visited
* `mike.public_pages` All pages in gallery
* `mike.all_pages` (admin only)

These are lists of `MikePage` instances that are *not* retrieved. Retrieval would reset the expiration date and would be heavy.

    page = mike.owned_pages[0].retrieve()
    
A specific page can be explicitly retrieved.
    
    page = mike.get_page('abcdedf-uuid-string-of-page')
    
Pages can be edited:

    page.title = 'Hello World'
    page.commit()
    
But not all attribute changes are allowed. To understand what does an attribute do (apart from using `help`) you can query it with:

    page.what_is('location_viewport')
    
Note that two properties are Enums, `.public` handled by `Privacy` and `.location_viewport` handled by `Location`.
This is to avoid arbitrary values:

    p.public = Privacy['public']
    p.public = p.public.__class__['public'] # if you forgot/don't want to import `Privacy`.

In addition two methods alter the page with new keys (`commit` still required). `page.clear_revisions()`
and `page.refresh_image()`.

To display in a Jupyter notebook a link and a thumbnail use `page.show_link()`, however will not work in terminal.

Some methods are duplicated between `MikeAPI` and `MikePage`.
  
* `page.retrieve()` = `mike.set_page(uuid)`
* `page.commit()` = `mike.set_page(uuid, page)`
* `page.delete()` = `mike.del_page(uuid)`
* `page.shorten(short)` = `mike.shorten_page(uuid, short)`

There is no difference.

Altering 'loadfun' (the JS) and 'pdb' is restricted to admin and approved users.

As changing the variable name in 'proteins' for the PDB code requires it to be changed in 'pdb'.

    page.proteins[2]['value'] = 'altered_variable_name'
    page.pdb['altered_variable_name']
    
The method `.rename_protein_variable()` does this for you.
    
Proteins stored in GitHub can be added via `page.append_github_entry(self, username, repo, path)` where the name
will be a sluggified filename.
    
## Page creation
New pages can be added using either a pdb code or a filename with additional arguments as used by prolinks,
but with underscores instead of spaces.

    new_page = mike.convert_pdb(code='1UBQ', data_focus='residue', data_selection='20:A')
    new_page = mike.convert_pdb(filename='/home/my_protein.pdb')
    
## Admin commands

Some commands are for admins only. Please do not try them out or you will get automatically blocked.

## Table

For the Covid Moonshot, I made a few interactive tables with different poses,
_eg._ [Fragmenstein hits](https://michelanglo.sgc.ox.ac.uk/data/13523b58-d0b1-4d05-9158-a8fd2be8465c).

This is not meant to be an official feature, but these can be made with the API by a priviledged users.
They require GitHub for storing the `mol` files.

    gitfolder='/Users/you/path_to_your_github_repo_on_your_machine'
    sdfile='/Users/you/path_to_sdfile.sdf'
    folder = 'folder_name_within_repo'
    targetfolder=f'{gitfolder}/{folder}'
    page.description = 'Hello world. '
    page.loadfun = ''
    page.columns_viewport = 6
    page.columns_text = 6
    
    page.sdf_to_mols(sdfile=sdfile,
                 targetfolder=targetfolder,
                 skip_first=True) # first row is metadata in a SDF for XChem
    page.sdf_to_json(sdfile=sdfile,
                 keys=('∆∆G', 'comRMSD', 'N_constrained_atoms', 'runtime', 'disregarded', 'smiles'),
                 key_defaults=(999., 999., 0, 999., 'NA', 'NA'), #what to set stuff that is null
                 filename=f'{targetfolder}/data.json')
    page.make_fragment_table(sdfile=sdfile,
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
    # git add, commit and push

## "Merging"

The object `MikePage` does not have a merge uuids like the website has. The reason for this is because this would be rather
redundant and convoluted. To add structures to a page use the following methods:

* append_github_entry
* append_pdbfile
* append_pdbblock
* remove_protein

Or operate upon the manually. PDBBlocks are stored in `.pdbs` (`Dict[str: str]`),
while `.proteins` (`List[dict]`) stores the protein information.


## More

For more, see [Sphinx generated documentation](sphinx-docs.md).

## To Do

* Get Uniprot chain definitions
* read/write MD from/to cell
* 

## Plotly

With JS priviledges it is possible to add a Plotly plot, by exporting via `fig.write_html("file.html", include_plotlyjs='cdn')`
and getting the content of `<body>` and adding to the description (with corrected indentation).
Unfortunately, whereas the path-element of class `.point` contains the data values to determine what residue it is,
I am not sure how to detect a specific click as this detects a click for the whole series...

    document.getElementById('xxxx').on('plotly_hover', data =>
        data.points.forEach(d => NGL.getStage().compList[0].addRepresentation("hyperball", { sele: ''+d.data.x[0]}))
    )