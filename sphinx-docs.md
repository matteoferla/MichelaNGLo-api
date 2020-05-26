# api package

## Submodules

## api.core module


### class api.core.MikeAPI(username=None, password=None, session=None, url='https://michelanglo.sgc.ox.ac.uk/')
Bases: `object`


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



#### login()

#### make_github_entry(username, repo, path)
make a proteinJSON entry.


* **Return type**

    `Dict`



#### post(route, data=None, headers=None)

#### post_json(route, data=None, headers=None)

#### static print_reply(reply)

#### refresh_pages()

#### rename_page(uuid, new_name)

#### rename_pdb(data, name, idx=None, original=None)

#### set_page(uuid, page)

#### shorten_page(uuid, short_name)

#### verify_user()
## api.page module


### class api.page.Location()
Bases: `enum.Enum`

An enumeration.


#### left( = 0)

#### right( = 1)

### class api.page.MikePage(parent, uuid)
Bases: `object`

> > This class holds page data.
> > And adds some extra conversion features.

> Attributes:\* `authors`: (<class ‘list’>) List of who has edited the page


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



#### check_columns()

#### clear_revisions()
On commit, ask the server to blank all revisions. Only privedged or admin.


* **Return type**

    `None`



* **Returns**

    None



#### property columns_text()

#### property columns_viewport()

#### commit()

#### definitions( = {'authors': 'List of who has edited the page', 'backgroundcolor': '(read-only) colour of background of NGL viewport', 'columns_text': 'x/12 width of description', 'columns_viewport': 'x/12 width of NGL viewport', 'confidential': 'show confidential banner?', 'current_page': '(read-only) uuid as present in the data (not redirect)', 'data_other': 'NGL viewport commands (initial view in the absence of loadfun', 'date': '(read-only) last access (see page delition policy)', 'descr_mdowned': '(read-only) description in HTML', 'description': 'description in MD', 'editable': '(read-only) Legacy', 'editors': 'Who has been added as a potential editor', 'encrypted': '(read-only) Encrypt? (DB)', 'encryption': 'Encrypt?', 'encryption_key': 'Encryption key. Not stored in the DB', 'firsttime': '(read-only) Show first time viewing notifications? Do not recall dif from is_unseen', 'freelyeditable': 'Can anyone edit?', 'image': 'Image link to show or None', 'is_unseen': '?? Same as firsttime??', 'key': '?? Same as encryption key??', 'loadfun': 'JS to add', 'location_viewport': 'Left or Right NGL viewport', 'model': 'Is this a model?', 'no_analytics': '(read-only) Do not gatether stats on this page?', 'no_buttons': '(read-only) Do not show buttons on this page?', 'no_user': '(read-only) Do not show user controls on this page?', 'page': '(read-only) uuid', 'pdb': 'list of tuple of name and block', 'proteinJSON': 'list of protein', 'public': <enum 'Privacy'>, 'revisions': 'list of past edits', 'save': '????', 'stick': '(ready_only) Legacy', 'stick_format': '(ready_only) Legacy', 'title': 'Title', 'uniform_non_carbon': '(ready_only) Legacy', 'user': '(ready_only) You', 'validation': '(ready_only) Legacy', 'verbose': '(ready_only) Legacy', 'viewport': '(ready_only) NGL viewport name', 'visitors': '(ready_only) who visited'})

#### delete()

#### dump()

#### property link()

* **Return type**

    `str`



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



#### rename(new_name)

#### retrieve()

#### shorten(short_name)

#### show_link()

* **Return type**

    `None`



#### what_is(attr)
Query what an attribute does.


* **Parameters**

    **attr** – 



* **Returns**

    


### class api.page.Privacy()
Bases: `enum.Enum`

An enumeration.


#### pinned( = 4)

#### private( = 0)

#### public( = 1)

#### published( = 2)

#### sgc( = 3)
## Module contents
