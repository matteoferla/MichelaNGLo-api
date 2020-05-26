# MichelaNGLo-api
A python module to interact with the Michelaɴɢʟo server ([<https://michelanglo.sgc.ox.ac.uk>](<https://michelanglo.sgc.ox.ac.uk>))
programmatically.

> :hammer: The migration is not complete!

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
    
## More

For more, see [Sphinx generated documentation](sphinx-docs.md).

## To Do

* Get Uniprot chain definitions
* Github
* 