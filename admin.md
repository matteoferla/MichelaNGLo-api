# Admin only commands

Here are some commands that are admin only.
This is intended for anyone who takes over the duties of maintaining Michelanglo
and not general users.

Admins have an additional property in their MikeAPI instance, `mike.all_pages`, which is a dictionary of lists of pages.
Unretrieved like the rest.

```python
from michelanglo_api import MikeAPI
import os
mike = MikeAPI(os.environ['MIKE_USER'], os.environ['MIKE_PASS'])
print(mike.all_pages.keys()) #['unencrypted_files', 'encrypted_files', 'unencrypted_entries', 'encrypted_entries', 'deleted_entries']
```

## Reset

Reset runs off a secret code, 
which for security reasons the API does not accept as an argument but
reads the environment variable `MIKE_SECRET`
to avoid any snippets making their way into GitHub. Serverside the code is the same one 
in `request.registry.settings['michelanglo.secretcode']` as read in the ini file or environment variable `MICHELANGLO_SECRETCODE`.

```python
## Set here in Python for demo purposes only
os.environ['MIKE_SECRET'] = '👾👾👾👾👾👾👾👾👾'
mike.reset(change='Fix for x, y and z', timeout=5 * 60)
```

The result is possible in the site, via the [admin page](https://michelanglo.sgc.ox.ac.uk/admin).
By setting a message, waiting a bit and resetting.

## Shorten

Given a page, a short name can be generated:

```python
uuid = '👾👾👾-👾👾👾-👾👾👾'
short_name = '👾👾👾'

mike.post_json('set',{'item':'shorten', 
                      'short': short_name,
                      'long': uuid})
```

## Publish

The easiest way is to find the article in Pubmed and press the blue cite button on the right and copy that.

```python
## copy citation off PubMED
# Do check all is fine!
copied_citation = '''👾👾👾👾👾👾'''

citation = dict(zip(['authors', 'title', 'journal', 'date-issue', 'doi', 'epub', 'pmid'], copied_citation.split('. ')))
citation['year'] = int(citation['date-issue'][:4])
if ';' in citation['date-issue']:
    citation['date'], citation['issue'] = citation['date-issue'].split(';')
else:
    citation['date'], citation['issue'] = citation['date-issue'].split(':')
print(citation)
```

Make absolutely sure the uuid is correct and the citation data is correct. To correct a mistake,
you have to log into the server and into postgres and manually correct it.

```python
page = mike.get_page(uuid)
print(page.title)
```

Then do

```python
page.add_publication(authors=citation['authors'].split(',')[0] + ' et al.',
                     year=citation['year'],
                     title= citation['title'],
                     journal= citation['journal'],
                     issue= citation['issue'],
                     doi= citation['doi'])
```

There are other things that need to be taken care of, namely:

```python
print(page.title)
page.public = mike.Privacy.published
page.protect()
page.freelyeditable = False
page.clear_revisions()
page.commit()
```

Remember to shift+refresh the [gallery page](https://michelanglo.sgc.ox.ac.uk/gallery) when checking the results!!