try:
    from IPython.display import display, HTML
except ImportError:
    pass  # not jupyter.

import json
from warnings import warn
from enum import Enum
from typing import Any
from datetime import datetime
import copy


class Privacy(Enum):
    private = 0
    public = 1
    published = 2
    sgc = 3
    pinned = 4


class Location(Enum):
    left = 0
    right = 1


class MikePage:
    """
    This class holds page data.
    And adds some extra conversion features.
    """
    parent = None

    preferences = {'authors': list,
                   'backgroundcolor': str,
                   'columns_text': int,
                   'columns_viewport': int,
                   'confidential': bool,
                   'current_page': str,
                   'data_other': str,
                   'date': datetime,
                   'descr_mdowned': str,
                   'description': str,
                   'editable': bool,
                   'editors': list,
                   'encrypted': bool,
                   'encryption': bool,
                   'encryption_key': (None.__class__, str),
                   'firsttime': bool,
                   'freelyeditable': bool,
                   'image': (None.__class__, bool, str), #: todo fix! this legacy business
                   'is_unseen': bool,
                   'key': (None.__class__, str),
                   'loadfun': str,
                   'location_viewport': Location,
                   'model': bool,
                   'no_analytics': bool,
                   'no_buttons': bool,
                   'no_user': bool,
                   'page': str,
                   'pdb': dict, # not list of tuples!
                   'proteinJSON': list,
                   'public': Privacy,
                   'revisions': list,
                   'save': bool,
                   'stick': str,
                   'stick_format': str,
                   'title': str,
                   'uniform_non_carbon': bool,
                   'user': str,
                   'validation': (bool, None.__class__),
                   'verbose': bool,
                   'viewport': str,
                   'visitors': list}

    definitions = {'authors': 'List of who has edited the page',
                   'backgroundcolor': '(read-only) colour of background of NGL viewport',
                   'columns_text': 'x/12 width of description',
                   'columns_viewport': 'x/12 width of NGL viewport',
                   'confidential': 'show confidential banner?',
                   'current_page': '(read-only) uuid as present in the data (not redirect)',
                   'data_other': 'NGL viewport commands (initial view in the absence of loadfun',
                   'date': '(read-only) last access (see page delition policy)',
                   'descr_mdowned': '(read-only) description in HTML',
                   'description': 'description in MD',
                   'editable': '(read-only) Legacy',
                   'editors': 'Who has been added as a potential editor',
                   'encrypted': '(read-only) Encrypt? (DB)',
                   'encryption': 'Encrypt?',
                   'encryption_key': 'Encryption key. Not stored in the DB',
                   'firsttime': '(read-only) Show first time viewing notifications? Do not recall dif from is_unseen',
                   'freelyeditable': 'Can anyone edit?',
                   'image': 'Image link to show or None',
                   'is_unseen': '?? Same as firsttime??',
                   'key': '?? Same as encryption key??',
                   'loadfun': 'JS to add',
                   'location_viewport': 'Left or Right NGL viewport',
                   'model': 'Is this a model?',
                   'no_analytics': '(read-only) Do not gatether stats on this page?',
                   'no_buttons': '(read-only) Do not show buttons on this page?',
                   'no_user': '(read-only) Do not show user controls on this page?',
                   'page': '(read-only) uuid',
                   'pdb': 'list of tuple of name and block',
                   'proteinJSON': 'list of protein',
                   'public': Privacy,
                   'revisions': 'list of past edits',
                   'save': '????',
                   'stick': '(ready_only) Legacy',
                   'stick_format': '(ready_only) Legacy',
                   'title': 'Title',
                   'uniform_non_carbon': '(ready_only) Legacy',
                   'user': '(ready_only) You',
                   'validation': '(ready_only) Legacy',
                   'verbose': '(ready_only) Legacy',
                   'viewport': '(ready_only) NGL viewport name',
                   'visitors': '(ready_only) who visited'}

    def __init__(self, parent, uuid: str):
        """
        Parent is MikeAPI

        :param parent:
        :param uuid:
        """
        self.parent = parent
        self.page = uuid
        self.date = datetime.min
        self.protein = []
        self.pdb = {}
        # set these to off for safety
        self._columns_viewport = 6
        self._columns_text = 6
        self.encryption = False
        self.encryption_key = str()
        self.public = Privacy.private
        self.freelyeditable = False
        self.new_editors = []
        self.model = False
        self.confidential = False

    def __getattr__(self, attr) -> Any:
        if attr not in self.__dict__:
            return False
        else:
            return getattr(self, attr)

    def __setattr__(self, attr, value) -> None:
        if attr in self.preferences and not isinstance(value, self.preferences[attr]):
                raise TypeError(f'{attr} is expected to be {self.preferences[attr]}, {value} is {type(value).__name__}')
        else:
            self.__dict__[attr] = value

    # ==== Columns =====================================================================================================

    def check_columns(self):
        if self._columns_viewport + self._columns_text != 12:
            raise ValueError('text and viewport are not 12.')

    @property
    def columns_viewport(self):
        self.check_columns()
        return self._columns_viewport

    @property
    def columns_text(self):
        self.check_columns()
        return self._columns_text

    @columns_viewport.setter
    def columns_viewport(self, value):
        if not isinstance(value, int):
            raise TypeError('Expecting int')
        elif value > 12 or value < 0:
            raise ValueError('Max is 12.')
        else:
            self._columns_text = 12 - value
            self._columns_viewport = value

    @columns_text.setter
    def columns_text(self, value):
        self.columns_viewport = 12 - value

    # ==== Columns =====================================================================================================

    def parse(self, data):
        """
        Parses server sent data.

        :return:
        """
        # proteinJSON -> protein
        # unfortunately I need to change how the data is sent. but I never get round to it.
        if isinstance(data['proteinJSON'], str):  # will be.
            self.protein = json.loads(data['proteinJSON'])
        else:
            self.protein = data['proteinJSON']
        del data['proteinJSON']
        if isinstance(data['pdb'], str):  # will be.
            try:
                data['pdb'] = json.loads(data['pdb'])
            except json.JSONDecodeError:
                warn('Pre-beta entry!')
                data['pdb'] = [[data['proteinJSON'][0]['value'], data['pdb']]]
        # pdb
        self.pdb = dict(data['pdb'])
        del data['pdb']
        # date
        self.date = datetime.fromisoformat(data['date'])
        del data['date']
        self.columns_viewport = data['columns_viewport']
        del data['columns_viewport']
        self.location_viewport = Location[data['location_viewport']]
        del data['location_viewport']
        self.public = Privacy[data['public']]
        del data['public']
        # rest
        for k, v in data.items():
            setattr(self, k, v)
        return self

    def dump(self):
        data = self.__dict__.copy()
        data['page'] = self.page
        data['proteinJSON'] = json.dumps(self.protein)
        del data['protein']
        data['pdb'] = json.dumps([[k, v] for k, v in self.pdb.items()])
        del data['date']
        # enums
        data['location_viewport'] = self.location_viewport.name
        data['public'] = self.public.name
        return data

    @property
    def link(self) -> str:
        link = f'<a href="{self.parent.url}data/{self.page}" target="_blank">{self.page}</a>' + \
               f'<img alt="error" src="{self.parent.url}thumb/{self.page}" height="200">'
        return link

    def show_link(self) -> None:
        display(HTML(self.link))

    def what_is(self, attr):
        """
        Query what an attribute does.

        :param attr:
        :return:
        """
        if attr in self.definitions:
            print(attr, self.definitions[attr])
        else:
            print(attr, 'No idea')

    def clear_revisions(self) -> None:
        """
        On commit, ask the server to blank all revisions. Only privedged or admin.

        :return: None
        """
        self.no_revisions = True

    def refresh_image(self) -> None:
        """
        On commit, refresh the tumbnail.

        :return: None
        """
        self.refresh_image = True

    # ======== Parent ==================================================================================================

    def retrieve(self):
        for k, v in self.parent.get_page(uuid=self.page).__dict__.items():
            self.__dict__[k] = v
        return self

    def commit(self):
        return self.parent.set_page(self.page, self)

    def delete(self):
        return self.parent.del_page(self.page)

    def rename(self, new_name):  ##admin only
        return self.parent.rename_page(self.page, new_name)

    def shorten(self, short_name):
        return self.parent.shorten_page(self.page, short_name)

    def __repr__(self):
        return f'<MikePage:{self.page} at {id(self)}>'

    def __str__(self):
        text = f'Page {self.page}\n'
        if self.title:
            text += f'# {self.title}\n'
        if self.description and len(self.description) > 200:
            text += f'{self.description[:200]} [... +{len(self.description) - 200} chars]\n'
        elif self.description:
            text += f'{self.description}\n'
        return text

MikePage.__doc__ += '\n Attributes:'
for key in MikePage.definitions:
    if key not in MikePage.preferences:
        MikePage.__doc__ += f'        * ``{key}``: {MikePage.definitions[key]}\n'
    else:
        MikePage.__doc__ += f'        * ``{key}``: ({MikePage.preferences[key]}) {MikePage.definitions[key]}\n'