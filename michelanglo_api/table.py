from typing import *
# if TYPE_CHECKING:   # from typing
#     import pandas as pd

from rdkit import Chem
import os, json
from typing import List, Sequence
from warnings import warn

class TableMixin:

    def pandas_to_mols(self,
                      df: 'pd.DataFrame',
                      targetfolder: str,
                      name_column_name: str = 'name',
                      mol_column_name: str = 'mol',
                      skip_first=False) -> List[str]:
        """
        Extracts the mols


        :param df: pandas datatable. Most likely the dataframe is ``rdkit.Chem.PandasTools`` flavoured,
            but this is not a requirement
        :param targetfolder: folder where to save the mol files (in a github repo)
        :param name_column_name: column name containing the molecule name
        :param mol_column_name: column name containing the molecules
        :param skip_first: default False, skip first if its definitions XChem style.
        :return:
        """
        filenames = []
        for i, row in df.iterrows():
            if skip_first and i == 0:
                continue
            mol = row[mol_column_name]
            name = row[name_column_name]
            if mol is None:
                filenames.append(None)
                continue
            elif not name:
                filename = f'compound_{i}'
            else:
                def valid(character): any([character.isalpha(),
                                           character.isdigit(),
                                           character in (' ', '-', '_', '.')
                                           ])
                filename = ''.join(filter(valid, name)).strip()
            filename += '.mol'
            Chem.MolToMolFile(mol, filename)
            filenames.append(filename)
        return filenames

    def sdf_to_mols(self, sdfile: str, targetfolder: str, skip_first=False) -> List[str]:
        """
        Converts a sdf file to mols for github
        The format is the same as that required by XChem fragalysis

        :param sdfile: SDF file
        :param targetfolder: folder where to save the mol files (a github repo)
        :param skip_first: default True, skip first if its definitions XChem style.
        :return: list of filenames
        """
        if os.path.exists(targetfolder):
            warn(f'{targetfolder} already exists')
        else:
            os.mkdir(targetfolder)
        suppl = Chem.SDMolSupplier(sdfile)
        next(suppl)
        filenames = []
        for i, mol in enumerate(suppl):
            if i == 0 and skip_first:
                continue
            filename = os.path.join(targetfolder, mol.GetProp('_Name') + '.mol')
            Chem.MolToMolFile(mol, filename)
            filenames.append(filename)
        return filenames

    def sdf_to_meta(self, sdfile: str) -> dict:
        suppl = Chem.SDMolSupplier(sdfile)
        return next(suppl).GetPropsAsDict()

    def sdf_to_json(self,
                    sdfile: str,
                    keys: Sequence[str],
                    key_defaults: Sequence[float],
                    filename: str,
                    spaced:bool=True
                    ) -> List[list]:
        """
        Get the keys out of the sdf and make a list of lists. filling blanks with the defaults.
        A convoluted method, that evolved into doing what numpy does...

        :param sdfile: SDF file
        :param keys: props to show in the table
        :param key_defaults: what are the value to show if absent (e.g. ∆∆G of 999.)
        :param filename: with path data.json
        :param spaced: convert underscores to spaces in header?
        :return:
        """
        suppl = Chem.SDMolSupplier(sdfile)
        # Parse data
        data = []
        for i, mol in enumerate(suppl):
            if i == 0:
                continue
            d = {'name': mol.GetProp('_Name')}
            for k, kd in zip(keys, key_defaults):
                if mol.HasProp(k):
                    v = mol.GetProp(k).strip()
                    if k == 'ref_mols':
                        d[k] = v.replace(',', ', ')
                        continue
                    elif isinstance(kd, float):
                        try:
                            v = round(float(v) * 10) / 10
                        except:
                            v = kd
                    elif isinstance(kd, str):
                        pass
                    d[k] = v
                else:
                    d[k] = kd
            data.append(d)
        # Make header
        if not spaced:
            header = [['name']+list(keys)]
        else:
            header = [[k.replace('_',' ') for k in ['name']+list(keys)]]
        # Combine
        flatten = header + [list(d.values()) for d in data]
        json.dump(flatten, open(filename, 'w'))
        return flatten

    def make_fragment_table(self,
                   metadata:Dict[str, str],
                   username:str,
                   repo_name:str,
                   foldername:str,
                   protein_sele:str,
                   sort_col:int,
                   sort_dir:str='asc',
                   template_row:int=-1,
                   fragment_row:int=-1,
                   jsonfile:str='data.json',
                   branch:str='main'):
        """
        Makes a interactive table out of xchem submission.
        NB. this formerly accepted an SDF (XChem style formatted) not it is agnostic
        and accepts the dictionary metadata.

        :param metadata: a dictionary of value -> definitions. It is for the ``description`` text and
            not for the table per se. If really must be ommitted simply pass an empty dictionary.
            also see ``sdf_to_meta(sdfile)``
        :param username: GitHub username
        :param repo_name: GitHub repo name
        :param foldername: folder name within repo
        :param protein_sele: selection on protein to show as sticks
        :param sort_col: column to sort by
        :param sort_dir: asc | desc
        :param template_row: -1 for foldername/template.pdb else row in data.json to load.
        :param fragment_row: -1 for none. else read that column. comma separated. Names must match mol in foldername.
        :param jsonfile: data. use ``sdf_to_json``.
        :param branch: main or master etc.
        :return:
        """
        giturl = f'https://raw.githubusercontent.com/{username}/{repo_name}/{branch}/{foldername}'
        # Description
        self.description += '## Fields\n\n' + ''.join([f'* **{k}**: {v}\n' for k, v in metadata.items()]) + '\n'
        self.description += '## Data\n'
        self.description += '<table id="data" class="display" width="100%"></table>\n'
        self.description += '<link href="https://cdn.datatables.net/1.10.20/css/dataTables.bootstrap4.min.css" rel="stylesheet"/>\n'
        # JS
        self.loadfun += '''["https://cdn.datatables.net/1.10.20/js/jquery.dataTables.min.js",
                            "https://cdn.datatables.net/1.10.20/js/dataTables.bootstrap4.min.js"].map((v,i) => {
                                setTimeout(() => {
                                    let s = document.createElement("script");
                                    s.type = "text/javascript";
                                    s.src = v;
                                    $("body").append(s);
                                },100 * i + 1);
                            });'''
        load_table = f'const giturl = "{giturl}"; const jsonfile = "{jsonfile}";' + \
                     f'const sort_col = {sort_col}; const sort_dir= "{sort_dir}";' + \
                     f'const protein_sele = "{protein_sele}"; const template_row={template_row};' +\
                     f'const fragment_row={fragment_row};' +\
                     '''fetch(`${giturl}/${jsonfile}`)
                        .then((response) => {
                            return response.json();
                        })
                        .then((dataSet) => {
                            let headers = dataSet.shift().map(v => ({'title': v}));
                            window.dataSet = dataSet;
                            window.dt = $('#data').DataTable({
                                    data: dataSet,
                                    columns:  headers,
                                    scrollX: true,
                                    order: [[ sort_col, sort_dir ]]
                                });
                            window.makeTableClickable(giturl, protein_sele, template_row, fragment_row);
                        });\n'''
        self.loadfun +=  '''window.makeTableClickable = (giturl, protein_sele, template_row, fragment_row) => {
                        $('#data tbody').css('cursor', 'pointer');
                        $('#data tbody').on('click', 'tr', function () {
                        $('#data .bg-info').removeClass('bg-info');
                        $(this).addClass('bg-info');
                        let data = dt.row(this).data();
                        let name = data[0].trim();
                        let hits = (fragment_row === -1) ? [] : data[fragment_row].replace(' ', '').replace(/_0/g, '').split(',');
                        if (!myData.proteins.some(v => v.name === name)) {
                            let ref_url = giturl+'/';
                            ref_url += (template_row === -1) ? 'template.pdb' : data[template_row].replace('.pdb','')+'.pdb';
                            myData.proteins.push({
                                type: 'url',
                                value: ref_url,
                                'name': name,
                                'loadFx': (protein) => {
                                    let colors = ['silver', 'black', 'white', 'gray', 'gainsboro'];
                                    protein.removeAllRepresentations();
                                    protein.addRepresentation("cartoon", {opacity: 0.1, colorValue: 'coral'});
                                    protein.addRepresentation("hyperball", {sele: protein_sele, colorValue: 'coral', opacity: 0.3});
                                    protein.autoView(protein_sele, 2000);
                                    // ligand
                                    NGL.getStage('viewport').loadFile(
                                        `${giturl}/${data[0].replace('.mol','')}.mol`)
                                        .then(molecule => {
                                            molecule.removeAllRepresentations();
                                            molecule.addRepresentation("hyperball", {sele: 'not _H', colorValue: 'teal', opacity: 0.3});
                                            molecule.autoView(2000);
                                        });
                    
                                    hits.map(h => NGL.getStage('viewport').loadFile(
                                        `${giturl}/${h.trim()}.mol`)
                                        .then(molecule => {
                                            molecule.removeAllRepresentations();
                                            molecule.addRepresentation("licorice", {
                                                sele: 'not _H',
                                                colorValue: colors.pop(),
                                                multipleBond: "symmetric"
                                            });
                                        })
                                    );
                                }
                            });
                        }
                        NGL.specialOps.load(name, false);
                    });};'''
        self.loadfun += '$(document).ready(() => { setTimeout(() => {' +load_table +'},200)});'