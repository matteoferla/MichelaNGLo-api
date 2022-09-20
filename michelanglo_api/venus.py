from typing import *
from enum import Enum
from .base import BaseAPI


class VenusError(ValueError):
    pass


class Steps(Enum):
    none = 0
    mutation = 1,
    protein = 2,
    structural = 3,
    ddG = 4,
    ddG_gnomad = 5


class VenusAPI(BaseAPI):
    """
    see ``analyse``, ``match_gene``, ``match_species`` and ``from_transcript``.

    """
    steps = Steps

    defaults = {'swiss_oligomer_identity_cutoff': 40,
                'swiss_monomer_identity_cutoff': 70,
                'swiss_oligomer_qmean_cutoff': -2,
                'swiss_monomer_qmean_cutoff': -2,
                'cycles': 1,
                'radius': 12,
                'scorefxn_name': 'ref2015',
                'allow_pdb': True,
                'allow_swiss': True,
                'allow_alphafold': True,
                'job_id': None, ## Do not touch this unless you know what you are doing.
                # these are not allowed as 'customfile' route as API does not allow this.
                # extras.pdb, filename, params, format
                }

    def analyse(self,
                gene: str,
                mutation: str,
                species: Union[int, str] = 9606,
                step: Optional[Union[str, Steps]] = None,
                **extras) -> dict:
        """
        >>> venus = VenusAPI()  # url argument for custom
        >>> venus.analyse(gene='LZTR1', mutation='S244C')  # omitted species is human

        The gene is uniprot id or gene name —If unsure of gene name use ``venus.match_gene``.
        while species is taxid or species name. If unsure of species name use ``venus.match_species``.

        The dictionary contains the following keys:

        * status ('success')
        * warnings, a List[str] of minor issues
        * time_taken: time in secs
        * has_structure: bool
        * protein: details about the protein
        * mutation: structure independent details about mutation
        * structural: structure dependent details about mutation
        * ddG: ddG calculation of mutant (including models)
        * gnomAD_ddG: quick ddG calculation of gnomAD

        :param gene: uniprot id or gene name. If unsure of gene name use ``venus.match_gene``
        :param mutation:
        :param species: taxid or species name. If unsure of species name use ``venus.match_species``.
        :param step:
        :param extras: extra arguments for run. see ``.defaults`` for defaults.
        :return: dictionary with data
        """
        # overloaded is 3.8 so avoided.
        # parse inputs
        inputs = self._parse_analysis_inputs(mutation, gene, species, step)
        # analyse
        return self._analyse(**inputs, **extras)

    def _analyse(self, mutation, uniprot, taxid, step_name, **extras):
        essential = dict(uniprot=uniprot,
                         species=taxid,
                         mutation=mutation,
                         mode='json',
                         step=step_name)
        reply = self.post_json('venus_analyse', data={**essential, **extras} )
        # parse reply
        if reply['status'] == 'error':
            raise VenusError(reply['msg'])
        return reply

    def _parse_analysis_inputs(self, mutation, gene, species, step) -> dict:
        if isinstance(species, str):
            taxid = self.get_taxid(species)
        elif isinstance(species, int):
            taxid = species
        else:
            raise TypeError('Species is neither str or int')
        if gene[1].isdigit():
            uniprot = gene
        else:
            uniprot = self.get_uniprot(gene)
        # for now this is convoluted
        if isinstance(step, Steps) and step.value != 0:
            step_name = step.name
        elif isinstance(step, str) and step.lower() != 'none':
            # make sure it is fine. KeyError
            step_name = Steps[step].name
        else:
            step_name = None
        return dict(mutation=mutation,
                    uniprot=uniprot,
                    taxid=taxid,
                    step_name=step_name)

    # ---------------- Random ------------------------------------------------------------------------------------------

    def random(self):
        return self.post_json('venus_random')

    def analyse_random(self):
        random = self.random()
        return self._analyse(uniprot=random['uniprot'],
                             taxid=random['taxid'],
                             mutation=random['mutation'],
                             step_name=None)

    # ---------------- Matching ----------------------------------------------------------------------------------------

    def _match_choice(self, name, reply):
        if 'taxid' in reply or 'uniprot' in reply:
            return [name]
        elif 'options' not in reply:
            raise NotImplementedError(f'This is impossible: {reply}')
        elif reply['options'] == 'many':
            raise ValueError('Too many options.')
        else:
            return reply['options']

    def match_species(self, species_name: str):
        """
        Given a partial species name return the correct names
        """
        reply = self.post_json('choose_pdb',
                               data=dict(item='match species',
                                         name=species_name)
                               )
        return self._match_choice(species_name, reply)

    def match_gene(self, gene_name: str, taxid: int = 9606):
        """
        Given a partial gene name return the correct names
        """
        reply = self.post_json('choose_pdb',
                               data=dict(item='match gene',
                                         species=taxid,
                                         gene=gene_name)
                               )
        return self._match_choice(gene_name, reply)

    # ---------------- Conversion --------------------------------------------------------------------------------------

    def _assert_single(self, reply, required: str):
        if 'options' in reply:
            raise ValueError(f'Ambiguous. Specify one of {reply["options"]}')
        elif required not in reply:
            raise NotImplementedError(f'This is impossible: {reply}')

    def get_taxid(self, species_name: str) -> int:
        """Given a species name, e.g. cat, return the taxid"""
        reply = self.post_json('choose_pdb',
                               data=dict(item='match species', name=species_name)
                               )
        self._assert_single(reply, 'taxid')
        return int(reply['taxid'])

    def get_uniprot(self, gene_name: str, species: int = 9606) -> str:
        """Given a gene name, return the Uniprot ID"""
        reply = self.post_json('choose_pdb',
                               data=dict(item='match gene',
                                         species=species,
                                         gene=gene_name)
                               )
        self._assert_single(reply, 'uniprot')
        return reply['uniprot']

    def from_transcript(self, enst:str, mutation:str) -> dict:
        reply = self.post_json('venus_transcript',
                               data=dict(enst=enst,
                                         mutation=mutation)
                               )
        if 'status' in reply and reply['status'] == 'error':
            raise VenusError(reply['error'])
        return reply

