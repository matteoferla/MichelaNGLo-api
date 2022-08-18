import time
from datetime import datetime, timedelta
from typing import Optional
from warnings import warn

import os
import requests

from .base import BaseAPI
from .enums import Privacy, Location
from .page import MikePage

try:
    from .progressbar import Progress
except Exception as e:
    Progress = None
    warn(f'Progressbar not importable: {e}')


class MikeAPI(BaseAPI):
    Privacy = Privacy
    Location = Location

    def __init__(self,
                 username: Optional[str] = None,
                 password: Optional[str] = None,
                 session: Optional[requests.Session] = None,
                 url: str = 'https://michelanglo.sgc.ox.ac.uk/'):
        """
        Gets the API interface thingamabob.

        :param username: if None, check environment variable ``MICHELANGLO_USERNAME`` or prompt
        :param password: if None, check environment variable ``MICHELANGLO_PASSWORD`` or prompt
        :param session: supply your own session, debug use basically.
        :param url: specify if using anything other than sgc version (e.g. 'http://0.0.0.0:8088')
        """
        super().__init__(session=session, url=url)
        self.username = self._retrieve_arg(username, 'MICHELANGLO_USERNAME')
        self.password = self._retrieve_arg(password, 'MICHELANGLO_PASSWORD')
        self.visited_pages = []  # filled by self.refresh_pages()
        self.owned_pages = []  # filled by self.refresh_pages()
        self.public_pages = []  # filled by self.refresh_pages()
        self.login()
        self.refresh_pages()

    def _retrieve_arg(self, arg, envname):
        """
        fill username/password.

        :param arg:
        :param envname: 'MICHELANGLO_PASSWORD' or 'MICHELANGLO_USERNAME'
        :return:
        """
        if arg is not None:
            return arg
        elif envname in os.environ:
            return os.environ[envname]
        else:
            return input(envname).strip()

    # ==================================================================================================================

    def login(self):
        reply = self.post('login', data={'username': self.username,
                                         'password': self.password,
                                         'action': 'login'})
        if reply.status_code != 200:
            raise ConnectionRefusedError(f'Code {reply.status_code}: {reply.content}')
        return self

    def verify_user(self):
        return self.post_json('login', {'action': 'whoami'})

    # ==================================================================================================================

    def refresh_pages(self):
        data = self.post_json('get_pages')
        self.visited_pages = [MikePage(self, uuid) for uuid in data['visited']]
        self.owned_pages = [MikePage(self, uuid) for uuid in data['owned']]
        self.public_pages = [MikePage(self, uuid) for uuid in data['public']]
        if isinstance(data['all'], dict):
            self.all_pages = {category: [MikePage(self, uuid)
                                         for uuid in data['all'][category]] for category in data['all']}  # admin only
        return self

    def get_page(self, uuid: str) -> MikePage:
        uuid = self._clean_uuid(uuid)
        try:
            data = self.post_json('data/' + uuid, data={'mode': 'json'})
            return MikePage(self, uuid).parse(data)
        except Exception as err:
            raise err

    def _clean_uuid(self, url):
        if isinstance(url, str):
            return url.split('/')[-1]
        elif isinstance(url, dict):
            return url['page']

    def set_page(self, uuid, page):
        uuid = self._clean_uuid(uuid)
        data = page.dumps()
        return self.post_json('edit_user-page', data=data)

    def del_page(self, uuid):
        uuid = self._clean_uuid(uuid)
        return self.post_json('delete_user-page', data={'page': uuid})

    def rename_page(self, uuid, new_name):  ##admin only
        warn('This is depracated use shorten')
        uuid = self._clean_uuid(uuid)
        return self.post_json('rename_user-page', data={'old_page': uuid, 'new_page': new_name})

    def shorten_page(self, uuid, short_name):
        return self.post_json('set', {'item': 'shorten',
                                      'short': short_name.lower(),
                                      'long': uuid})

    # ==================================================================================================================

    def convert_pdb(self, code=None, filename=None, pdbblock=None, **prolink_settings):
        """
        use underscores for the hyphens in the data attr!

        ```python
        new_page = mike.convert_pdb(code='1UBQ', data_focus='residue', data_selection='20:A')
        new_page = mike.convert_pdb(filename='/home/my_protein.pdb')
        mike.page_link(new_page['page'])
        ```
        """
        data = {}
        prolink_settings['role'] = 'NGL'
        if code:
            prolink_settings['data-load'] = code
            data['mode'] = 'code'
            data['pdb'] = code
        elif filename:
            data['mode'] = 'file'
            data['pdb'] = open(filename).read()
        elif pdbblock:
            data['mode'] = 'file'
            data['pdb'] = pdbblock
        else:
            raise ValueError('Specifiy at least a pdb `code` or a `file`')
        data['viewcode'] = ' '.join(
            ['{a}="{p}"'.format(p=prolink_settings[s], a=s.replace('_', '-')) for s in prolink_settings])
        reply = self.post_json('convert_pdb', data)
        return MikePage(self, reply['page'])

    # ==================================================================================================================

    def convert_pse(self, demo_filename=None, filename=None, sticks='hyperball', uniform_non_carbon=False,
                    pdb_code=None):
        """
        filename is local while demo_filename is on server.
        """
        data = {'stick_format': sticks, 'uniform_non_carbon': uniform_non_carbon}
        if demo_filename:
            if demo_filename.find('.pse') == -1:
                warn(f'{demo_filename} does not end in .pse. Forcing.')
                demo_filename += '.pse'
            data['demo_filename'] = demo_filename
        elif filename:
            data['file'] = open(filename).read()
            if pdb_code:
                data['pdb'] = pdb_code
            else:
                data['pdb'] = False
        else:
            raise ValueError('Demo or file')
        reply = self.post_json('convert_pse', data)
        return MikePage(self, reply['page'])

    @staticmethod
    def print_reply(reply):
        print(f'Status code: {reply.status_code}; Headers: {reply.headers}; Content: {reply.content}')

    def find_page_by_keyword(self, keyword: str) -> MikePage:
        """
        This is a time-consuming operation as the data needs to be retrieved.

        :param keyword:
        :return:
        """
        keyword: str = str(keyword).lower()
        assert keyword != '', 'empty keyword'
        for page in self.owned_pages:
            page.retrieve()
            if keyword in page.title.lower():
                return page
        for page in self.owned_pages:
            if keyword in page.description.lower():
                return page
        else:
            raise ValueError(f'no owned page with {keyword}')

    # def rename_pdb(self, data, name: str, idx: Optional[int] = None, original: Optional[str] = None):
    #     # original is the name in the original version. idx is the index
    #     if original is not None:
    #         for p in data['pdb']:
    #             if p[0] == original:
    #                 p[0] = name
    #                 break
    #         for p in data['proteinJSON']:
    #             if p['value'] == original:
    #                 p['value'] = name
    #                 break
    #     elif idx is not None:
    #         data['proteinJSON'][idx]['value'] = name
    #         data['pdb'][idx][0] = name
    #     else:
    #         raise TypeError('specify either idx or original')

    # ======================================================================================================================

    def set_toast(self, title: str, description: str, bg: str = 'bg-danger'):
        # admin only.
        return self.post_json('set', {'item': 'msg',
                                      'title': title,
                                      'descr': description,
                                      'bg': bg})

    def reset(self, change: str = 'misc.', timeout: int = 300):
        """
        Reset the server after ``timeout`` seconds. warning about the reset with a custom message ``change``.

        :param change:
        :param timeout:
        :return:
        """
        assert 'MIKE_SECRET' in os.environ, 'Please provide the secret code as an environment variable.'
        self.set_toast(title='<i class="far fa-danger"></i> App server restart',
                       description=f'In order to implement the latest changes ({change}), ' +
                                   'the App will update and restart at ' +
                                   f'{datetime.now() + timedelta(seconds=timeout)} BST ({timeout} sec. countdown). ' +
                                   f'This will be a brief blip. You might not even notice it!',
                       bg='bg-danger')
        if Progress is not None:
            Progress().countdown(timeout)
        time.sleep(timeout)
        try:
            print(self.post_json('set', {'item': 'terminate', 'code': os.environ['MIKE_SECRET']}))
        except:
            print('Server resetting.')

    def get_user_email(self, username: str):
        assert 'MIKE_SECRET' in os.environ, 'Please provide the secret code as an environment variable.'
        reply = self.post_json('login', {'action': 'email', 'username': username, 'code': os.environ['MIKE_SECRET']})
        if 'email' not in reply:
            raise ValueError(str(reply))
        return reply['email']

    @classmethod
    def guest_login(cls):
        warn('Few features will be functional...')
        self = cls.__new__(cls)
        cls.__mro__[1].__init__(self)  # could super do this?
        self.username = None
        self.password = None
        self.visited_pages = []  # filled by self.refresh_pages()
        self.owned_pages = []  # filled by self.refresh_pages()
        self.public_pages = []  # filled by self.refresh_pages()
        # self.refresh_pages()
        return self
