# michelanglo_api package

## Submodules

## michelanglo_api.bootstrap_elements module


### michelanglo_api.bootstrap_elements.deindent(text)

* **Return type**

    `str`



### michelanglo_api.bootstrap_elements.make_FA_list(entries, id_attribute=None)

* **Return type**

    `str`



### michelanglo_api.bootstrap_elements.make_carousel(bodies, id_attribute)

* **Return type**

    `str`



### michelanglo_api.bootstrap_elements.make_header_slide(title, subtitle)

* **Return type**

    `str`



### michelanglo_api.bootstrap_elements.make_list(entries, id_attribute=None, ordered=False)

* **Return type**

    `str`



### michelanglo_api.bootstrap_elements.make_modal(title, body, id_attribute)

* **Return type**

    `str`



### michelanglo_api.bootstrap_elements.make_slide(title, body)

* **Return type**

    `str`


## michelanglo_api.core module


### class michelanglo_api.core.MikeAPI(username=None, password=None, session=None, url='https://michelanglo.sgc.ox.ac.uk/')
Bases: `object`


#### class Location()
Bases: `enum.Enum`

An enumeration.


#### left( = 0)

#### right( = 1)

#### class Privacy()
Bases: `enum.Enum`

An enumeration.


#### pinned( = 4)

#### private( = 0)

#### public( = 1)

#### published( = 2)

#### sgc( = 3)

#### \__init__(username=None, password=None, session=None, url='https://michelanglo.sgc.ox.ac.uk/')
Gets the API interface thingamabob.


* **Parameters**

    
    * **username** (`Optional`[`str`]) – if None, check environment variable `MICHELANGLO_USERNAME` or prompt


    * **password** (`Optional`[`str`]) – if None, check environment variable `MICHELANGLO_PASSWORD` or prompt


    * **session** (`Optional`[`Session`]) – supply your own session, debug use basically.


    * **url** (`str`) – specify if using anything other than sgc version (e.g. ‘[http://0.0.0.0:8088](http://0.0.0.0:8088)’)



#### convert_pdb(code=None, filename=None, \*\*prolink_settings)
use underscores for the hyphens in the data attr!
>>> new_page = mike.convert_pdb(code=’1UBQ’, data_focus=’residue’, data_selection=’20:A’)
>>> new_page = mike.convert_pdb(filename=’/home/my_protein.pdb’)
>>> mike.page_link(new_page[‘page’])


#### convert_pse(demo_filename=None, filename=None, sticks='hyperball', uniform_non_carbon=False, pdb_code=None)
filename is local while demo_filename is on server.


#### del_page(uuid)

#### get_page(uuid)

* **Return type**

    `MikePage`



#### get_user_email(username)

#### login()

#### post(route, data=None, headers=None)

#### post_json(route, data=None, headers=None)

#### static print_reply(reply)

#### refresh_pages()

#### rename_page(uuid, new_name)

#### reset(change='misc.', timeout=300)
Reset the server after `timeout` seconds. warning about the reset with a custom message `change`.


* **Parameters**

    
    * **change** (`str`) – 


    * **timeout** (`int`) – 



* **Returns**

    


#### set_page(uuid, page)

#### set_toast(title, description, bg='bg-danger')

#### shorten_page(uuid, short_name)

#### verify_user()
## michelanglo_api.enums module


### class michelanglo_api.enums.Location()
Bases: `enum.Enum`

An enumeration.


#### left( = 0)

#### right( = 1)

### class michelanglo_api.enums.Privacy()
Bases: `enum.Enum`

An enumeration.


#### pinned( = 4)

#### private( = 0)

#### public( = 1)

#### published( = 2)

#### sgc( = 3)
## michelanglo_api.page module


### class michelanglo_api.page.MikePage(parent, uuid)
Bases: `michelanglo_api.table.TableMixin`

> This class holds page data.
> And adds some extra conversion features.

Attributes:        \* `authors`: (<class ‘list’>) List of who has edited the page

    
    * `backgroundcolor`: (<class ‘str’>) (read-only) colour of background of NGL viewport


    * `columns_text`: (<class ‘int’>) x/12 width of description


    * `columns_viewport`: (<class ‘int’>) x/12 width of NGL viewport


    * `confidential`: (<class ‘bool’>) show confidential banner?


    * `current_page`: (<class ‘str’>) (read-only) uuid as present in the data (not redirect)


    * `data_other`: (<class ‘str’>) NGL viewport commands (initial view in the absence of loadfun


    * `date`: (<class ‘datetime.datetime’>) (read-only) last access (see page delition policy)


    * `descr_mdowned`: (<class ‘str’>) (read-only) description in HTML


    * `description`: (<class ‘str’>) description in MD


    * `editable`: (<class ‘bool’>) (read-only) Legacy


    * `editors`: (<class ‘list’>) Who has been added as a potential editor


    * `encrypted`: (<class ‘bool’>) (read-only) Encrypt? (DB)


    * `encryption`: (<class ‘bool’>) Encrypt?


    * `encryption_key`: ((<class ‘NoneType’>, <class ‘str’>)) Encryption key. Not stored in the DB


    * `firsttime`: (<class ‘bool’>) (read-only) Show first time viewing notifications? Do not recall dif from is_unseen


    * `freelyeditable`: (<class ‘bool’>) Can anyone edit?


    * `image`: ((<class ‘NoneType’>, <class ‘bool’>, <class ‘str’>)) Image link to show or None


    * `is_unseen`: (<class ‘bool’>) ?? Same as firsttime??


    * `key`: ((<class ‘NoneType’>, <class ‘str’>)) ?? Same as encryption key??


    * `loadfun`: (<class ‘str’>) JS to add


    * `location_viewport`: (<enum ‘Location’>) Left or Right NGL viewport


    * `model`: (<class ‘bool’>) Is this a model?


    * `no_analytics`: (<class ‘bool’>) (read-only) Do not gatether stats on this page?


    * `no_buttons`: (<class ‘bool’>) (read-only) Do not show buttons on this page?


    * `no_user`: (<class ‘bool’>) (read-only) Do not show user controls on this page?


    * `page`: (<class ‘str’>) (read-only) uuid


    * `pdb`: (<class ‘dict’>) list of tuple of name and block


    * `proteinJSON`: (<class ‘list’>) list of protein


    * `public`: (<enum ‘Privacy’>) <enum ‘Privacy’>


    * `revisions`: (<class ‘list’>) list of past edits


    * `save`: (<class ‘bool’>) ????


    * `stick`: (<class ‘str’>) (ready_only) Legacy


    * `stick_format`: (<class ‘str’>) (ready_only) Legacy


    * `title`: (<class ‘str’>) Title


    * `uniform_non_carbon`: (<class ‘bool’>) (ready_only) Legacy


    * `user`: (<class ‘str’>) (ready_only) You


    * `validation`: ((<class ‘bool’>, <class ‘NoneType’>)) (ready_only) Legacy


    * `verbose`: (<class ‘bool’>) (ready_only) Legacy


    * `viewport`: (<class ‘str’>) (ready_only) NGL viewport name


    * `visitors`: (<class ‘list’>) (ready_only) who visited


#### \__init__(parent, uuid)
Parent is MikeAPI


* **Parameters**

    
    * **parent** – 


    * **uuid** (`str`) – 



#### add_publication(url=None, authors='TBA', year=None, title='TBA', journal='manuscript in preparation', issue='NA', doi=None)
This is an admin only operation due to the security issue (dodgy links in the gallery).
Publication is not data from the page, it’s an actual table


* **Parameters**

    
    * **uuid** – 


    * **url** (`Optional`[`str`]) – 


    * **authors** (`Optional`[`str`]) – 


    * **year** (`Optional`[`int`]) – 


    * **title** (`Optional`[`str`]) – 


    * **journal** (`Optional`[`str`]) – 


    * **issue** (`Optional`[`str`]) – 



* **Returns**

    


#### append_github_entry(username, repo, path)
make and add a protein entry.


* **Parameters**

    
    * **username** (`str`) – Github username


    * **repo** (`str`) – repository


    * **path** (`str`) – path within repo



* **Return type**

    `int`



* **Returns**

    


#### append_pdbblock(pdbblock, varname, chain_definitions=[])
make and add a protein entry.


* **Parameters**

    
    * **pdbblock** (`str`) – the pdbblock to add.


    * **varname** (`str`) – what should the pdbblock be known as?


    * **chain_definitions** (`List`[`dict`]) – list of dict defining who each chain is. Needed solely for Uniprot modal and chain name in builder



* **Return type**

    `int`



* **Returns**

    


#### append_pdbfile(filename, varname=None, chain_definitions=[])
make and add a protein entry.


* **Parameters**

    
    * **filename** (`str`) – the local filename to add.


    * **varname** (`Optional`[`str`]) – what should the pdbblock be known as?


    * **chain_definitions** (`List`[`dict`]) – list of dict defining who each chain is. Needed solely for Uniprot modal and chain name in builder



* **Return type**

    `int`



* **Returns**

    


#### check_columns()
Verify that columns_viewport and columns_text are 12.
See bootstrap docs for details of why a full row is 12.


#### clear_revisions()
On commit, ask the server to blank all revisions. Only privedged or admin.


* **Return type**

    `None`



* **Returns**

    None



#### commit()

#### definitions( = {'authors': 'List of who has edited the page', 'backgroundcolor': '(read-only) colour of background of NGL viewport', 'columns_text': 'x/12 width of description', 'columns_viewport': 'x/12 width of NGL viewport', 'confidential': 'show confidential banner?', 'current_page': '(read-only) uuid as present in the data (not redirect)', 'data_other': 'NGL viewport commands (initial view in the absence of loadfun', 'date': '(read-only) last access (see page delition policy)', 'descr_mdowned': '(read-only) description in HTML', 'description': 'description in MD', 'editable': '(read-only) Legacy', 'editors': 'Who has been added as a potential editor', 'encrypted': '(read-only) Encrypt? (DB)', 'encryption': 'Encrypt?', 'encryption_key': 'Encryption key. Not stored in the DB', 'firsttime': '(read-only) Show first time viewing notifications? Do not recall dif from is_unseen', 'freelyeditable': 'Can anyone edit?', 'image': 'Image link to show or None', 'is_unseen': '?? Same as firsttime??', 'key': '?? Same as encryption key??', 'loadfun': 'JS to add', 'location_viewport': 'Left or Right NGL viewport', 'model': 'Is this a model?', 'no_analytics': '(read-only) Do not gatether stats on this page?', 'no_buttons': '(read-only) Do not show buttons on this page?', 'no_user': '(read-only) Do not show user controls on this page?', 'page': '(read-only) uuid', 'pdb': 'list of tuple of name and block', 'proteinJSON': 'list of protein', 'public': <enum 'Privacy'>, 'revisions': 'list of past edits', 'save': '????', 'stick': '(ready_only) Legacy', 'stick_format': '(ready_only) Legacy', 'title': 'Title', 'uniform_non_carbon': '(ready_only) Legacy', 'user': '(ready_only) You', 'validation': '(ready_only) Legacy', 'verbose': '(ready_only) Legacy', 'viewport': '(ready_only) NGL viewport name', 'visitors': '(ready_only) who visited'})

#### delete()

#### dumps()
For proper saving see `to_pickle` or `save`.
convert the object as dictionary.
:return:


#### from_pickle(filename)

#### get_protein(index=None, name=None, value=None)
Overloaded method. accepts one of the three parameters:


* **Parameters**

    
    * **index** (`Optional`[`int`]) – list index


    * **name** (`Optional`[`str`]) – name of protein


    * **value** (`Optional`[`str`]) – value of protein, this is the JS function



* **Return type**

    `Dict`



* **Returns**

    the protein entry



#### property link()

* **Return type**

    `str`



#### load(name)
Loads what was saved with `.saved`


* **Parameters**

    **name** (`str`) – filename (path okay) with no extension.



* **Returns**

    


#### make_github_entry(username, repo, path, branch='main')
make a protein entry.


* **Parameters**

    
    * **username** (`str`) – Github username


    * **repo** (`str`) – repository


    * **path** (`str`) – path within repo


    * **branch** (`str`) – main or master etc.



* **Return type**

    `Dict`



* **Returns**

    


#### parent( = None)

#### parse(data)
Parses server sent data.


* **Returns**

    


#### preferences( = {'authors': <class 'list'>, 'backgroundcolor': <class 'str'>, 'columns_text': <class 'int'>, 'columns_viewport': <class 'int'>, 'confidential': <class 'bool'>, 'current_page': <class 'str'>, 'data_other': <class 'str'>, 'date': <class 'datetime.datetime'>, 'descr_mdowned': <class 'str'>, 'description': <class 'str'>, 'editable': <class 'bool'>, 'editors': <class 'list'>, 'encrypted': <class 'bool'>, 'encryption': <class 'bool'>, 'encryption_key': (<class 'NoneType'>, <class 'str'>), 'firsttime': <class 'bool'>, 'freelyeditable': <class 'bool'>, 'image': (<class 'NoneType'>, <class 'bool'>, <class 'str'>), 'is_unseen': <class 'bool'>, 'key': (<class 'NoneType'>, <class 'str'>), 'loadfun': <class 'str'>, 'location_viewport': <enum 'Location'>, 'model': <class 'bool'>, 'no_analytics': <class 'bool'>, 'no_buttons': <class 'bool'>, 'no_user': <class 'bool'>, 'page': <class 'str'>, 'pdb': <class 'dict'>, 'proteinJSON': <class 'list'>, 'public': <enum 'Privacy'>, 'revisions': <class 'list'>, 'save': <class 'bool'>, 'stick': <class 'str'>, 'stick_format': <class 'str'>, 'title': <class 'str'>, 'uniform_non_carbon': <class 'bool'>, 'user': <class 'str'>, 'validation': (<class 'bool'>, <class 'NoneType'>), 'verbose': <class 'bool'>, 'viewport': <class 'str'>, 'visitors': <class 'list'>})

#### refresh_image()
On commit, refresh the tumbnail.


* **Return type**

    `None`



* **Returns**

    None



#### remove_protein(index)

#### rename(new_name)

#### rename_protein_variable(index=None, name=None, value=None, newname=None)
Overloaded method. accepts one of the three parameters:


* **Parameters**

    
    * **index** (`Optional`[`int`]) – list index


    * **name** (`Optional`[`str`]) – name of protein


    * **value** (`Optional`[`str`]) – value of protein, this is the JS function


    * **newname** (`Optional`[`str`]) – if None, it will remove it as a variable and change the type to data.



* **Returns**

    


#### retrieve()

#### save(name)
Save the description, pdbs and JS for easier editing.
It’s inverse `load` loads them.
The purpose is to edit the file as opposed to a wonky notebook cell.

`save` is a legacy keyword in the page data, but is no longer used.
:type name: `str`
:param name:
:return:


#### shorten(short_name)

#### show_link()

* **Return type**

    `None`



#### to_pickle(filename)
writes to pickle


* **Parameters**

    **filename** (`str`) – filename (path okay) with extension.



* **Returns**

    


#### what_is(attr)
Query what an attribute does.


* **Parameters**

    **attr** (`str`) – 



* **Returns**

    

## michelanglo_api.progressbar module


### class michelanglo_api.progressbar.Progress(percent=0, label='')
Bases: `object`

Add a progressbar.
Using [https://getbootstrap.com/docs/4.3/components/progress/](https://getbootstrap.com/docs/4.3/components/progress/) not the HTML5 one.
Note that Jupyter uses an older version: 3.4 ([https://getbootstrap.com/docs/3.4/components/](https://getbootstrap.com/docs/3.4/components/)), but I doubt this will be so for long hence the color via style.
Two uses different uses.

Timer:
>>> Progress().countdown(seconds) = the progressbar counts to n seconds every tick ms

Manual
>>> p = Progress(percent=20, label=’hello’) both percent and label are optional arguments
>>> p.percent = 30
>>> p.label = ‘bye’
Do note that .percent and .label do not check what the real value of the Progress bar is and rely on a previously stored value.
Hence why they are incorrect for .countdown().
This is unavoidable as JS can run a IPython command only when the kernel is idle and this is needed to input values.
Consequently, the method .update(‘varname’) is provided which will check.
The argument for .update is the name variable has in the Python mainspace as a string.
Do note the update happens after the cell has finished excecuting. So
>>> p = Progress(percent=20, label=’hello’)
>>> print(p.percent, p.label) # correct
>>> p.countdown(5)
>>> time.sleep(1)
>>> print(p.percent, p.label) # incorrect
>>> p.update(‘p’)
>>> print(p.percent, p.label) # incorrect within the same cell, correct in next.
The HTML element id of the bar is .id.


#### \__init__(percent=0, label='')
Initialize self.  See help(type(self)) for accurate signature.


#### countdown(seconds, tick=1000)

#### property label()

#### property percent()

#### update(name)
## michelanglo_api.prolink module


### class michelanglo_api.prolink.Prolink(text, target='viewport', focus='domain', selection='\*', color=None, radius=None, tolerance=None, hetero=None, label=None, view=None, title=None, load=None, alts=None)
Bases: `object`

Create prolink and export it with str(prolink).
Allows for handy manupulation such as copying and changing its values.

To instantiate from string tag, use `Prolink.parse`.


#### \__init__(text, target='viewport', focus='domain', selection='\*', color=None, radius=None, tolerance=None, hetero=None, label=None, view=None, title=None, load=None, alts=None)
The arguments are data tags.
For full details of these see [https://michelanglo.sgc.ox.ac.uk/docs/markup](https://michelanglo.sgc.ox.ac.uk/docs/markup)

```python
>>> pro = Prolink(text='V242A', focus="domain", color="#967bb6", selection=":V", alts=[dict(selection="242:V",focus="residue", color="#FF00FF")])
>>> str(pro)
>>> pro.color = 'yellow'
```

The alternative selection differs (`alts` as opposed separate fields).
As a result of alts remember to do copy.deepcopy and not just copy.copy if copying.

```python
>>> import copy
>>> new_pro = copy.deepcopy(pro)
```

NB. data-toggle=”protein” defines a prolink, so isnt an option.
NB2. intolerant to spelling “tollerance [sic.]”


* **Parameters**

    
    * **text** (`str`) – inside text, assumed to be escaped already


    * **target** (`str`) – viewport id in JS (generally “viewport”)


    * **focus** (`str`) – residue | domain | residue | clash | bfactor | surface | overlay \* | domain-overlay \*


    * **selection** (`str`) – see NGL selection


    * **color** (`Optional`[`str`]) – for now a string in a valid color (`#ff00ff` or `green`)


    * **radius** (`Optional`[`int`]) – 


    * **tolerance** (`Optional`[`int`]) – 


    * **hetero** (`Optional`[`bool`]) – 


    * **label** (`Optional`[`bool`]) – 


    * **view** (`Optional`[`str`]) – 


    * **title** (`Optional`[`str`]) – caption


    * **load** (`Optional`[`str`]) – 


    * **alts** (*List**[**Dict**[**str**, **str**]**]*) – `alts` is a list of dict with keys `selection` | `focus` | `color`. e.g. [{‘selection’: ‘242:V’, ‘focus’: ‘residue’ color: “#FF00FF”}]



#### property data_attributes()

#### escaper(value)

#### classmethod parse(tag)
Parse a tag (str) to create a Prolink instance
Round trip:

```python
>>> pro = Prolink(text='Hello', focus="domain", color="pink", selection=":A")
>>> spro = str(pro)
>>> neopro = Prolink.parse(spro)
>>> print(pro, neopro)
```


* **Parameters**

    **tag** (`str`) – tag contain both opening and closing elements. Can contain newlines



* **Returns**

    Prolink instance


## michelanglo_api.table module


### class michelanglo_api.table.TableMixin()
Bases: `object`


#### make_fragment_table(sdfile, username, repo_name, foldername, protein_sele, sort_col, sort_dir='asc', template_row=- 1, fragment_row=- 1, jsonfile='data.json', branch='main')
Makes a interactive table out of xchem submission.


* **Parameters**

    
    * **sdfile** (`str`) – 


    * **username** (`str`) – GitHub username


    * **repo_name** (`str`) – GitHub repo name


    * **foldername** (`str`) – folder name within repo


    * **protein_sele** (`str`) – selection on protein to show as sticks


    * **sort_col** (`int`) – column to sort by


    * **sort_dir** (`str`) – asc | desc


    * **template_row** (`int`) – -1 for foldername/template.pdb else row in data.json to load.


    * **fragment_row** (`int`) – -1 for none. else read that column. comma separated. Names must match mol in foldername.


    * **jsonfile** (`str`) – data. use `sdf_to_json`.


    * **branch** (`str`) – main or master etc.



* **Returns**

    


#### sdf_to_json(sdfile, keys, key_defaults, filename, spaced=True)
Get the keys out of the sdf and make a list of lists. filling blanks with the defaults.
A convoluted method, that evolved into doing what numpy does…


* **Parameters**

    
    * **sdfile** (`str`) – SDF file


    * **keys** (`Sequence`[`str`]) – props to show in the table


    * **key_defaults** (`Sequence`[`float`]) – what are the value to show if absent (e.g. ∆∆G of 999.)


    * **filename** (`str`) – with path data.json


    * **spaced** (`bool`) – convert underscores to spaces in header?



* **Return type**

    `List`[`list`]



* **Returns**

    


#### sdf_to_meta(sdfile)

#### sdf_to_mols(sdfile, targetfolder, skip_first=True)
Converts a sdf file to mols for github


* **Parameters**

    
    * **sdfile** (`str`) – SDF file


    * **targetfolder** (`str`) – folder where to save the mol files (a github repo)


    * **skip_first** – skip first if its definitions XChem style.



* **Return type**

    `List`[`str`]



* **Returns**

    list of filenames


## Module contents
