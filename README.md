# MichelaNGLo-api
A python module to interact with the Michelaɴɢʟo server programmatically.

> :hammer: The migration is not complete!

## Notes
The details of the requests accepted by Michelaɴɢʟo are described in [its documentation](https://michelanglo.sgc.ox.ac.uk/docs/api).\
You may interact with the server however you please. This code is just to make life easier.

There are three tiers of users. Basic, priviledged, admin. Basic users cannot add JS to the site as this is a security threat
(cookie theft)... And it prevents users from making
[pages that behave maliciously or similar](https://michelanglo.sgc.ox.ac.uk/data/fa3844a8-d7f5-4e84-9540-240f134ba6d1).

## Documentation

 simple API interface for Py3.6+ for
[<https://michelanglo.sgc.ox.ac.uk>](<https://michelanglo.sgc.ox.ac.uk>).

    mike = MikeAPI('username','password')
    page_data = mike.get_page('abcdedf-uuid-string-of-page')
    page\_data\['title'\] = 'Hello World'
    mike.set\_page('abcdedf-uuid-string-of-page',page\_data)

New pages can be added using either a pdb code or a filename with
additional arguments as used by prolinks, but with underscores instead
of spaces. 

\>\>\> new\_page = mike.convert\_pdb(code='1UBQ',
data\_focus='residue', data\_selection='20:A') \>\>\> new\_page =
mike.convert\_pdb(filename='/home/my\_protein.pdb')

To display in a Jupyter notebook a link use
<span class="title-ref">mike.page\_link(uuid)</span>, however will not
work in terminal I think.

Altering 'loadfun' (the JS) and 'pdb' is restricted to admin and
approved users.

  - Note, changing the variable name in 'proteinJSON' for the PDB code
    requires it to be changed in 'pdb'.  
    \>\>\> page\_data\['proteinJSON'\]\[2\]\['value'\] =
    'altered\_variable\_name' \>\>\> page\_data\['pdb'\]\[2\]\[0\] =
    'altered\_variable\_name'

\#\#\# Instance attributes: \* <span class="title-ref">.url</span> is
'<https://michelanglo.sgc.ox.ac.uk/>' unless altered (\_e.g.\_ local
version of Michelanglo) \* <span class="title-ref">.username</span> is
the username \* <span class="title-ref">.password</span> is the raw
password \* <span class="title-ref">.visited\_pages</span>,
<span class="title-ref">.owned\_pages</span> and
<span class="title-ref">.public\_pages</span> are lists filled by
<span class="title-ref">.refresh\_pages()</span> \*
<span class="title-ref">.request</span> is a requests session object.

\#\#\# Instance methods: \* <span class="title-ref">.post(route,
data=None, headers=None)</span> does the requests for other methods...
\* <span class="title-ref">.post\_json(route, data=None,
headers=None)</span> as above but decodes the json reply... \*
<span class="title-ref">.login()</span>. called automatically during
initialisation. \* <span class="title-ref">.verify\_user()</span>. check
whether you are still logged in. \*
<span class="title-ref">.refresh\_pages()</span>. gets the lists
<span class="title-ref">.visited\_pages</span>,
<span class="title-ref">.owned\_pages</span> and
<span class="title-ref">.public\_pages</span> (and
<span class="title-ref">.all</span> if admin) \*
<span class="title-ref">.get\_page(uuid)</span> returns the data (:dict)
for a given page. \* <span class="title-ref">.set\_page(uuid,
data)</span> sets the data (:dict) for a given page \*
<span class="title-ref">.delete\_page(uuid)</span> delete \*
<span class="title-ref">.rename\_page(uuid, name)</span> rename (admin
only\!)

\#\#\# keys of page json Some are obsolete. 'viewport', 'image',
'uniform\_non\_carbon', 'verbose', 'validation', 'stick\_format',
'save', 'backgroundcolor', 'location\_viewport', 'columns\_viewport',
'columns\_text', 'pdb', 'loadfun', 'proteinJSON', 'author', 'editors',
'description', 'title', 'visitors', 'authors', 'public', 'confidential',
'stick', 'data\_other', 'date', 'page', 'key', 'encryption',
'freelyeditable', 'user', 'editable', 'no\_user', 'no\_buttons',
'no\_analytics', 'current\_page'
