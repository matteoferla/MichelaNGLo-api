window.table_promises = [];
window.sdf_promises = [];
// table to card
if (document.getElementById("data") === null) {
    const table_el = document.createElement("table");
    table_el.id = "data";
    table_el.classList.add('display');
    table_el.setAttribute('width', "100%");
    //
    document.getElementById("uniprot_btns").prepend(table_el);
    ops.addToast('loading_toast', 'Data is being loaded', 'Please be patient', 'bg-info');
}

// js x2
function loadScript(url) {
    return new Promise(function (resolve, reject) {
        let script = document.createElement("script");
        script.onload = resolve;
        script.onerror = reject;
        script.src = url;
        document.getElementsByTagName("head")[0].appendChild(script);
    });
}

// call x2
window.table_promises.push(loadScript("https://cdn.datatables.net/1.13.4/js/jquery.dataTables.min.js"));
window.table_promises.push(loadScript("https://cdn.datatables.net/1.13.4/js/dataTables.bootstrap4.min.js"));

// css
const datatablecss = document.createElement("link");
datatablecss.href = "https://cdn.datatables.net/1.13.4/css/dataTables.bootstrap4.min.css"
datatablecss.rel = "stylesheet"
document.getElementsByTagName("head")[0].appendChild(datatablecss);

sdf_promises.push(NGL.getStage().loadFile(user_definitions.hit_sdf_url)
    .then(comp => user_definitions.hit_idx = NGL.getStage().compList.length - 1)
);
user_definitions.model_idxdex = {};
Object.entries(user_definitions.model_sdf_urldex).forEach(
    ([name, model_sdf_url]) => sdf_promises.push(NGL.getStage().loadFile(model_sdf_url)
        .then(comp => user_definitions.model_idxdex[name] = NGL.getStage().compList.length - 1)
    )
);
const dataLoader = (data) => {
    console.log(data);
    // show hits. This will be resolved by ``template_promise`` or called directly
    const showMols = () => {
        // hits
        let hit_sdf = NGL.getStage().compList[user_definitions.hit_idx];
        let hit_names = user_definitions.hit_col_idx !== -1 ? data[user_definitions.hit_col_idx] : [];
        if (Array.isArray(hit_names)) {
            // pass
        }
        else if (typeof hit_names !== 'string') {
            ops.addToast('error_toast', 'TypeError ' + hit_name, 'TypeError', 'bg-danger');
            return null;
        }
        else if (hit_names.includes('[')) {
            hit_names = JSON.parse(hit_names);
        } else {
            hit_names = hit_names.split(',');
        }
        let sele_ids = [...hit_names].map(hit_name => user_definitions.hitnames.indexOf(hit_name));
        if (sele_ids.some(v => v === -1)) {
            ops.addToast('error_toast', 'Missing data ' + hit_name, 'Error. No hit named', 'bg-danger');
            return null;
        }
        hit_sdf.setSelection(sele_ids.map(v => '/' + v).join(' or '));
        hit_sdf.addRepresentation("licorice", {
            colorValue: user_definitions.hit_color,
            multipeBond: true
        })
        hit_sdf.autoView();
        let mol_name = data[user_definitions.name_col_idx].trim();
        Object.entries(user_definitions.model_idxdex).forEach(
            ([groupname, model_idx]) => {
                let m_id = user_definitions.model_namedex[groupname].indexOf(mol_name);
                if (m_id === -1) {
                    ops.addToast('error_toast', 'Missing data ', `Error. Cannot find hit named ${mol_name} in ${groupname}`, 'bg-danger');
                    return null;
                }
                console.log(`loading mol model ${mol_name} (${m_id}) from ${groupname}`);
                let model_sdf = NGL.getStage().compList[model_idx];
                model_sdf.setSelection("/" + m_id)
                model_sdf.addRepresentation("hyperball", {
                    sele: 'not _H',
                    colorValue: user_definitions.model_colordex[groupname],
                    opacity: 0.3
                });
                model_sdf.autoView("/" + m_id);
            }
        )
    }

    // template
    if (user_definitions.target_col_idx === -1) {
        console.log('no template specified');
        showMols();
    } else {
        // the following replaces specialOps.load as it does a swap.
        const template_name = data[user_definitions.target_col_idx];
        const wanted_index = window.myData.proteins.map(v => v.name).indexOf(template_name);
        // resolve
        if (wanted_index === -1) {
            ops.addToast('error_toast', 'Missing data ', 'Error. Cannot find template named' + template_name, 'bg-danger');
            return null;
        } else if (wanted_index !== window.myData.currentIndex) {
            console.log(`Load new template ${wanted_index}, current: ${window.myData.currentIndex}`);
            const stage = NGL.getStage();
            // hide starting or remove newer one
            if (window.myData.currentIndex === 0) {
                stage.compList[0].removeAllRepresentations();
            } else {
                let current_name = window.myData.proteins[window.myData.currentIndex].name || window.myData.proteins[window.myData.currentIndex].value;
                console.log(current_name)
                if (!!current_name) {
                    stage.removeComponentsbyName(current_name);
                } else {
                    // this is subpar as it assumes it is the last
                    // nb pop would not work.
                    stage.removeComponent(stage.compList[stage.compList.length - 1]);
                }
            }
            // add new
            console.log(window.myData.proteins[wanted_index].value);
            ops.addToast('loadingT_toast', 'Template is being loaded', 'Please be patient', 'bg-info');
            window.myData.currentIndex = wanted_index;
            stage.loadFile(window.myData.proteins[wanted_index].value)
                .then((new_protein) => {
                    new_protein.setName(template_name);
                    if (window.myData.proteins[wanted_index].loadFx !== undefined) {
                        console.log('Protein loaded - defined func')
                        window[window.myData.proteins[wanted_index].loadFx](new_protein);
                    } else {
                        console.log('Protein loaded - vanilla')
                        new_protein.addRepresentation('cartoon', {color: user_definitions.template_color});
                        new_protein.addRepresentation('line');
                        new_protein.autoView();
                    }
                    showMols();

                }).catch(ops.addErrorToast);
        } else {
            // simply show the mols. Template is fine.
            showMols();
        }
    }
};

//JSON file
let metadata_promise = fetch(user_definitions.metadata_url);
table_promises.push(metadata_promise);

Promise.all(table_promises)
    .then(response => metadata_promise)
    .then(response => response.json())
    .then(info => {
        if (info.model_namedex) {
            user_definitions.model_namedex = info.model_namedex;
        } else if (info.modelnamedex) {
            user_definitions.model_namedex = info.modelnamedex;
        } else if (info.modelnames) {
            user_definitions.model_namedex = Object.fromEntries(
                Object.keys(user_definitions.model_colordex).map(groupname => [groupname, info.modelnames])
            );
        } else if (info.model_names) {
            user_definitions.model_namedex = Object.fromEntries(
                Object.keys(user_definitions.model_colordex).map(groupname => [groupname, info.model_names])
            );
        } else {
            throw 'modelnamedex or modelnames missing from json';
        }
        user_definitions.hitnames = info.hitnames;
        if (info.templates) {
            window.myData.proteins.push(...info.templates);
        }
        user_definitions.dt = $('#data').DataTable({
            data: info.data,
            columns: info.headers.map(v => ({
                'title': v
            })),
            scrollX: true,
            order: [
                [user_definitions.sort_col, user_definitions.sort_dir]
            ]
        });
        $('#data tbody').css('cursor', 'pointer');
        $('#data tbody').on('click', 'tr', function () {
            // reset status
            $('#data .bg-info').removeClass('bg-info');
            $(this).addClass('bg-info');
            dataLoader(user_definitions.dt.row(this).data());
        });
    });

// send alerts
Promise.all(table_promises).then(() => ops.addToast('json_loaded_toast', 'JSON Data loaded', 'JSON files loaded successful. Table will now work 1/2', 'bg-success'))
    .catch(ops.addErrorToast);
Promise.all(sdf_promises).then(() => ops.addToast('sdf_loaded_toast', 'SDF Data loaded', 'sdf files loaded successful. Table will now work 2/2', 'bg-success'))
    .catch(ops.addErrorToast);