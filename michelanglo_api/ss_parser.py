from collections import namedtuple


class SSParser:
    """
    Create a SS block from PDB data.
    Written to be agnostic of PDB parser, but for now only has PyMOL.
    .. code-block:: python
        import pymol2
        with pymol2.PyMOL() as pymol:
            pymol.cmd.load('model.pdb', 'prot')
            ss = SSParser().parse_pymol(pymol.cmd)
            print(ss)
        # or
        SSParser.correct_file('model.pdb', True)
    Do note that the lines seem offset because SHEET has a name parameter.
    HELIX    1  HA GLY A   86  GLY A   94  1                                   9
    SHEET    5   A 5 GLY A  52  PHE A  56 -1  N  PHE A  56   O  TRP A  71
    SHEET    1   B 5 THR B 107  ARG B 110  0
    """
    # faux pymol atom
    Atom = namedtuple('Atom', ['ss', 'resi', 'resn', 'chain'])

    def __init__(self):
        # none of the attributes are actually public.
        self.ss = []
        self.start = self.Atom('L', 0, 'XXX', 'X')
        self.previous = self.Atom('L', 0, 'XXX', 'X')
        self.ss_count = {'H': 1, 'S': 1, 'L': 0}

    def parse_pymol(self, cmd, selector: str = 'name ca') -> str:
        atoms = list(cmd.get_model(selector).atom)
        return self.parse(atoms)

    def parse(self, atoms: list) -> str:
        """
        atoms is a list of objects with 'ss', 'resi', 'resn'.
        one per residue (CA).
        This does not collapse the list into a list of ranges, as resn is also require etc.
        :param atoms:
        :return:
        """
        for current in atoms:
            if self.previous.ss != current.ss or self.previous.chain != current.chain:  # different
                self._store_ss()  # the previous ss has come to an end.
                # deal with current
                if current.ss in ('S', 'H'):  # start of a new
                    self.start = current
            # move on
            self.previous = current
        self._store_ss()
        return str(self)

    def _store_ss(self):
        """
        The SS sequence has come to an end: store it.
        :return:
        """
        if self.previous.ss == '':
            return # not AA?
        if int(self.previous.resi) == int(self.start.resi) + 1:
            return # too short
        cc = self.ss_count[self.previous.ss]
        if self.previous.ss == 'H':  # previous was the other type
            self.ss.append(
                f'HELIX  {cc: >3} {cc: >3} ' +
                f'{self.start.resn} {self.start.chain} {self.start.resi: >4}  ' +
                f'{self.previous.resn} {self.previous.chain} {self.previous.resi: >4}  1' +
                '                                  ' +
                f'{int(self.previous.resi) - int(self.start.resi): >2}'
            )
            self.ss_count[self.previous.ss] += 1
        elif self.previous.ss == 'S':  # previous was the other type
            self.ss.append(
                f'SHEET  {cc: >3} {cc: >2}S 1 ' +
                f'{self.start.resn} {self.start.chain}{self.start.resi: >4}  ' +
                f'{self.previous.resn} {self.previous.chain}{self.previous.resi: >4}  0')
            self.ss_count[self.previous.ss] += 1
        else:
            # loop? Nothing.
            pass

    def __str__(self):
        return '\n'.join(self.ss) +'\n'

    @classmethod
    def correct_file(cls, filename: str, write:bool=True):
        import pymol2
        with pymol2.PyMOL() as pymol:
            pymol.cmd.load(filename, 'prot')
            ss = cls().parse_pymol(pymol.cmd)
        with open(filename, 'r') as fh:
            block = fh.read()

        if write:
            with open(filename, 'w') as fh:
                fh.write(ss + block)
        return ss + block

    @classmethod
    def correct_block(cls, block: str):
        import pymol2
        with pymol2.PyMOL() as pymol:
            pymol.cmd.read_pdbstr(block, 'prot')
            ss = cls().parse_pymol(pymol.cmd)
        return ss + block
