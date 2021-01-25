from typing import *
import json, re

class Prolink:
    """
    Create prolink and export it with str(prolink).
    Allows for handy manupulation such as copying and changing its values.

    To instantiate from string tag, use ``Prolink.parse``.
    """
    def __init__(self,
                 text:str,
                 target:str = "viewport",
                 focus:str="domain",
                 selection: str="*",
                 color: Optional[str]=None, #"green",
                 radius: Optional[int]=None, #=5,
                 tolerance: Optional[int]=None, #1,
                 hetero: Optional[bool]=None, #False,
                 label: Optional[bool]=None, #True,
                 view: Optional[str] = None,
                 title: Optional[str]=None,
                 load:Optional[str]=None,
                 alts: Optional[List[Dict[str, str]]] = None):
        """

        The arguments are data tags.
        For full details of these see https://michelanglo.sgc.ox.ac.uk/docs/markup

        >>> pro = Prolink(text='V242A', focus="domain", color="#967bb6", selection=":V", alts=[dict(selection="242:V",focus="residue", color="#FF00FF")])
        >>> str(pro)
        >>> pro.color = 'yellow'

        The alternative selection differs (``alts`` as opposed separate fields).
        As a result of alts remember to do `copy.deepcopy` and not just `copy.copy` if copying.

        >>> import copy
        >>> new_pro = copy.deepcopy(pro)

        NB. data-toggle="protein" defines a prolink, so isnt an option.
        NB2. intolerant to spelling "tollerance [sic.]"

        :param text: inside text, assumed to be escaped already
        :param target: viewport id in JS (generally "viewport")
        :param focus: residue | domain | residue | clash | bfactor | surface | overlay * | domain-overlay *
        :param selection: see NGL selection
        :param color: for now a string in a valid color (``#ff00ff`` or ``green``)
        :param radius:
        :param tolerance:
        :param hetero:
        :param label:
        :param view:
        :param title: caption
        :param load:
        :param alts: ``alts`` is a list of dict with keys ``selection`` | ``focus`` | ``color``. e.g. [{'selection': '242:V', 'focus': 'residue' color: "#FF00FF"}]
        :type alts: List[Dict[str, str]]
        """
        self.element = 'span'
        self.text = text
        self.target = target
        self.focus = focus
        self.selection = selection
        self.color = color
        self.title = title
        self.load = load
        self.radius = radius
        self.tolerance = tolerance
        self.hetero = hetero
        self.label = label
        self.view = view
        self.alts = alts if alts else []

    @classmethod
    def parse(cls, tag: str):
        """
        Parse a tag (str) to create a Prolink instance
        Round trip:

        >>> pro = Prolink(text='Hello', focus="domain", color="pink", selection=":A")
        >>> spro = str(pro)
        >>> neopro = Prolink.parse(spro)
        >>> print(pro, neopro)

        :param tag: tag contain both opening and closing elements. Can contain newlines
        :return: Prolink instance
        """
        # split
        rex = re.match('<(\w+) ([\w\W]*)>([\w\W]*)<\/(\w+)\s?>', tag.strip())
        assert rex is not None, 'Is the tag closed?'
        fore_element, raw_attributes, text, aft_element = rex.groups()
        assert fore_element == aft_element, f'The closing element differs: {fore_element} != {aft_element}'
        esc_attributes = re.findall('data-([\w\-]+)\=((?:(?!data-).)*)', raw_attributes)
        # escape and collapse alts
        attributes = {'alts': []}
        for k, v in esc_attributes:
            if k == 'toggle':
                continue
            try:
                value = json.loads(v)
            except: # its a string already? html is very tolerant...
                value = v
            if '-alt' not in k:
                attributes[k] = value
            else:
                ak, raw_ai = re.match('(\w+)-alt(\d+)', k).groups()
                ai = int(raw_ai) - 1
                while len(attributes['alts']) <= ai:
                    attributes['alts'].append({})
                attributes['alts'][ai][ak] = value
        # instantiate
        self = cls(text=text, **attributes)
        self.element = fore_element
        return self


    @property
    def data_attributes(self):

        attributes = {'data-toggle': "protein",
                        'data-target': self.target,
                        'data-focus': self.focus,
                        'data-selection': self.selection,
                      }
        for optional in ('load', 'title', 'color', 'tolerance', 'radius', 'hetero', 'label', 'view'):
            if getattr(self, optional) is not None:
                attributes[f'data-{optional}'] = getattr(self, optional)
        for i, alt in enumerate(self.alts):
            for k, v in alt.items():
                attributes[f'data-{k}-alt{i+1}'] = v
        return attributes

    def escaper(self, value):
        return json.dumps(value)

    def __str__(self):
        data = ' '.join([f'{k}={self.escaper(v)}' for k, v in self.data_attributes.items()])
        return f'<{self.element} class="prolink" {data}>{self.text}</{self.element}>'
