# Presentation

> This feat is doable only for approved users —ie. users with no JS/CSS restrictions.
> For approval please email Matteo

For a seminar explaining the site I made a presentation within [a Michelanglo page](https://michelanglo.sgc.ox.ac.uk/data/66fb9edd-8552-458e-9b0b-7c42ca13fa88).
Here is the code used.

    from michelanglo_api import MikeAPI, MikePage
    import michelanglo_api.bootstrap_elements as BS
    
    mike = MikeAPI()
    page = mike.get_page('👾👾👾👾👾👾👾')
    
    page.title = 'SGC Internal Seminar — Matteo Ferla, 09/09/20'
    page.columns_text = 6
    page.clear_revisions()
    page.public = page.public.__class__.public # enum
    #page.loadfun = '' # no JS used so far...
    page.description = '''## Presentation
    
    This is the structure of the trp-cage mini protein (PDB:1L2Y).
    This protein designed twenty years ago is only 20 aminoacids long
    and has at its core a tryptophan residue (EDIT ME!). Curiously it looks like the SGC logo.
    
    * <a href="#firstshowModal" data-toggle="modal" data-target="#firstshowModal">
    Introductiory set of slides
    </a>
    * Editing a prolink (live)
    * <a href="#prolinkModal" data-toggle="modal" data-target="#prolinkModal">
    Prolink definition
    </a>
    * Creation, advanced editing and security (live)
    * <a href="https://michelanglo.sgc.ox.ac.uk/monitor/LZTR1" target="_blank">Example of protected page with warnings</a>
    * <a href="#venusModal" data-toggle="modal" data-target="#socialModal">In publications and social media</a>
    * <a href="https://michelanglo.sgc.ox.ac.uk/gallery" target="_blank">Gallery</a>, where pages made public go (live) —including SGC entries <small>(adopt one now!)</small></a>
    * <a href="#venusModal" data-toggle="modal" data-target="#venusModal">Venus</a>
    * <a href="#creditsModal" data-toggle="modal" data-target="#creditsModal">Credits
    </a>
    * For more see documentation or _Bioinformatics_ paper
    '''
    
    mike = 'Michela<span style="font-variant: small-caps;">ngl</span>o'
    samba = 'https://www.well.ox.ac.uk/~matteo/sgc2020_seminar'
    
    # ========================= firstshowModal
    
    slideinfo = BS.make_slide('Michelaɴɢʟo: <small>sculpting protein views on web pages without coding</small>',
                              BS.make_FA_list([
                                  ('far fa-presentation', 'Oxford SGC internal virtual seminar, University of Oxford'),
                                  ('far fa-clock', '9/9/2020'),
                                  ('far fa-user', 'Matteo Ferla'),
                                  ('far fa-globe', 'https://michelanglo.sgc.ox.ac.uk/'),
                                  ('far fa-map-marked-alt',
                                   'NIHR Oxford Biomedical Research Centre Genomic Medicine Theme (Prof Jenny Taylor)'),
                                  ('far fa-map-marked-alt',
                                   'Oxford Structural Genomics Consortium Research Informatics (Dr Brian Marsden)'),
                                  ('far fa-envelope', 'matteo@well.ox.ac.uk'),
                                  ('fab fa-twitter', '@matteoferla'),
                                  ('far fa-comment-alt-lines', 'blog.matteoferla.com')
                              ]))
    
    slidenames = BS.make_slide('Names of tools mentioned',
                               BS.make_FA_list([('far fa-pencil-paintbrush',
                                                 f'<b>{mike}</b>: sculpting protein views on web pages without coding'),
                                                ('far fa-radar',
                                                 '<b>VENUS</b>: assessing the effect of amino acid variants have on structure')
                                                ]))
    
    slidemike = BS.make_header_slide(mike, 'Reasons and aims')
    
    slidemikeproblem = BS.make_slide('Biochemists make pretty but complicated figures',
                                     f'''
                                  <img src="{samba}/complicated.jpg"
                                  alt="complicated" height="400">
                                  ''' + \
                                     BS.make_FA_list([
                                         ('far fa-cube', '3D to 2D makes it hard to follow'),
                                         ('far fa-search', 'Easily becomes information dense'),
                                         ('far fa-map-marker-question',
                                          'Very hard to infer position of a residue of interest to the <i>reader</i>')
                                     ])
                                     )
    
    slidemiketechno = BS.make_slide('Bridging the gap',
                                    BS.make_FA_list([
                                        ('far fa-cassette-tape', 'Technologies exist to show 3D structures on webpages'),
                                        ('far fa-industry-alt', 'Implemented on big sites, but not on personal sites'),
                                        ('far fa-code',
                                         'Requires JS coding and understanding how to use the JS protein library'),
                                        ('far fa-user-secret',
                                         'Reviewers avoid visiting sites managed by authors for minor points'),
                                        ('far fa-paperclip', 'Adding webpage as supplementary file is non trial')
                                    ]))
    
    slidemikeisee = BS.make_slide('iSee',
                                  BS.make_FA_list([
                                      ('far fa-history', 'iSee was a previous attempt at bridging this gap'),
                                      ('far fa-users', 'Interest from journals'),
                                      ('far fa-puzzle-piece', 'Relied on Flash — obsolete technology'),
                                  ])) + f'''
                                  <br/>
                                  <div class='row p-5'>
                                  <div class='col-5'>
                                      <img src="{samba}/iSee_logo.png" alt="flash" width="300">
                                  </div>
                                  <div class='col-5'>
                                      <img src="{samba}/flash.png" alt="flash" width="300">
                                  </div>
                                  </div>
                                  '''
    
    slidemikesolution = BS.make_slide(f'Enter {mike}',
                                      f'''
                                  <img src="{samba}/Fig1_v3.jpg"
                                  alt="complicated" height="500">
                                  <br/>
                                  ''' + \
                                      BS.make_FA_list([
                                          ('far fa-cloud-upload', f'Create a view via different sources'),
                                          ('far fa-pencil-paintbrush', 'Edit an interactive description'),
                                          ('far fa-hand-holding-box', 'Share'),
                                          ('far fa-home', 'Implement locally')
                                      ])
                                      )
    
    slidemiketerm = BS.make_slide(f'Terms',
                                  BS.make_FA_list(
                                      [('far fa-user-edit', 'Creator/owner/editor: a user that creates or edits a page'),
                                       (
                                           'far fa-user-alien',
                                           'Visitor/reader: a user that visits a page created by someone'),
                                       ('far fa-user', 'User: anyone using the site')]))
    
    slidemikenext = BS.make_slide(f'Next steps',
                                  '<p>In the next few minutes the following will be showcased live:</p><br/>' + \
                                  BS.make_FA_list([
                                      ('far fa-gift',
                                       '<a href="https://michelanglo.sgc.ox.ac.uk/r/dock7" target="_blank">Example of protein in figure</a>'),
                                      ('far fa-hammer', f'Editing this page to add a prolink (at "EDIT ME")'),
                                      ('far fa-plus-octagon', 'Create a new page (1UBQ, 1-20 green, 60- red)'),
                                      ('far fa-lock-alt', 'Registration and security'),
                                      ('far fa-starship', 'Advanced editing')
                                  ])
                                  )
    
    firstshow = [slideinfo,
                 slidenames,
                 slidemike,
                 slidemikeproblem,
                 slidemiketechno,
                 slidemikeisee,
                 slidemikesolution,
                 slidemiketerm,
                 slidemikenext]
    
    carousel = BS.make_carousel(bodies=firstshow, id_attribute='firstshowCarousel')
    modal = BS.make_modal(title='Introduction', body=carousel, id_attribute='firstshowModal')
    page.description += BS.deindent(modal)
    
    # ========================= prolinkModal
    
    modal = BS.make_modal(title='Prolink', body=f'''
    <h1>Prolink Anatomy</h1>
    <p>A "prolink" (protein-controlling link) is an HTML element that gets added to the description
    that specifies how to represent the protein.</p><br/>
    <img src="{samba}/prolink_anatomy.png" alt="prolink" height="500">
    ''', id_attribute='prolinkModal')
    page.description += BS.deindent(modal)
    
    # ======================== other
    
    social = [
        BS.make_slide('Journals',
                      f'''<p>One aim is for linking in journals —hence the permenance.</p>
                        <p>So far two published articles and a two under review have not had issues with editors.</p><br/>
                        <img src="{samba}/paper.png" alt="social" height="500">
                        '''),
        BS.make_slide(f'Social media cards',
                      f'''<p>When sharing to social media links are rendered as preview cards.</p><br/>
                        <img src="{samba}/fb.png" alt="social" height="500">
                        '''),
        BS.make_slide(f'API',
                      BS.make_FA_list([('far fa-user-robot',
                                        'Python 3.7+ API: <a href="https://github.com/matteoferla/MichelaNGLo-api" target="_blank">github.com/matteoferla/MichelaNGLo-api</a>'),
                                       ('far fa-projector',
                                        'This presentation was written in a Jupyter notebook using the API'),
                                       ('far fa-jack-o-lantern',
                                        'Heavily modded page: <a href="https://michelanglo.sgc.ox.ac.uk/r/fragmenstein" target="_blank">Fragmenstein result table</a>')
                                       ])
                      )
    
    ]
    carousel = BS.make_carousel(bodies=social, id_attribute='socialCarousel')
    modal = BS.make_modal(title='Social media cards', body=carousel, id_attribute='socialModal')
    page.description += BS.deindent(modal)
    
    # ========================= venusModal
    
    venus = [
        BS.make_slide(f'State of the art',
                      BS.make_FA_list([
                          ('far fa-biohazard', 'Assessing the structural effect of a mutation is not trivial'),
                          ('far fa-chart-network', 'Multiple causes...'),
                          ('far fa-fragile',
                           'The degree of destabilization that is significant is hazy: how big must a local ∆∆G change be?'),
                          ('far fa-fire-alt',
                           'Change in post translational modifications have diverse effects (e.g. ubiquitination loss &rarr; GOF)'),
                          ('far fa-tag', 'loss of signal sequences may route the protein is the wrong location'),
                          ('far fa-cookie-bite', 'Cofactor/substrate binding affected (requires modelling)'),
                          ('far fa-sign-in-alt', 'Interface with other protein (often unknown)'),
                          ('far fa-rabbit-fast', 'Stabilization preventing dynamic change')
                      ]) + \
                      '<p class="mt-3">Current technologies:</p>' + \
                      BS.make_FA_list([
                          ('far fa-wrench', 'SDM server: ∆∆G change'),
                          ('far fa-scroll', 'Missense3D: model-dependent effects (16 criteria)'),
                          ('far fa-pen-fancy', 'Miscast: annotation-dependent effects')
                      ])
                      ),
        BS.make_slide(f'Solution',
                      BS.make_FA_list([
                          ('far fa-crosshairs', 'VENUS aims to <i>help</i> indentify what is happening with a mutation'),
                          ('far fa-hand-paper', 'Does not give a rank or score —because users go "score shopping" anyway'),
                          ('far fa-hourglass-start', 'Gives out results as they are obtained'),
                          ('far fa-id-badge', 'Start from gene name, not PDB code'),
                          ('far fa-calculator', 'Calculates ∆∆G (Pyrosetta)'),
                          ('far fa-scroll-old', 'Finds affected nearby annotations (including PTM and motifs)'),
                          ('far fa-pencil-ruler', f'Export results to a {mike}'),
                          ('far fa-exclamation-triangle', f'Not published and in beta'),
                          (
                              'far fa-road',
                              'Go to <a href="https://michelanglo.sgc.ox.ac.uk/venus" target="_blank">VENUS</a>')
                      ])
                      )]
    
    carousel = BS.make_carousel(bodies=venus, id_attribute='venusCarousel')
    modal = BS.make_modal(title='Introduction', body=carousel, id_attribute='venusModal')
    page.description += BS.deindent(modal)
    
    # ========================= fragModal
    
    modal = BS.make_modal(title='Fragmenstein',
                          body=BS.make_slide('Topics',
                                             BS.make_FA_list([('far fa-', ''),
                                                              ('far fa-', ''),
                                                              ('far fa-', ''),
                                                              ])), id_attribute='fragModal')
    page.description += BS.deindent(modal)
    
    # ========================= prolinkModal
    
    modal = BS.make_modal(title='Acknowledgements',
                          id_attribute='creditsModal',
                          body=BS.make_header_slide('Thank-yous',
                                                    subtitle=BS.make_FA_list(
                                                        [('far fa-user-chart', 'Thank you, audience, for listening'),
                                                         ('far fa-user-edit',
                                                          'And thank you, past and <b>future</b>, page editors'),
                                                         ('far fa-user-cog',
                                                          'A big thanks to Dr Brian Marsden for all the ideas and feedback'),
                                                         ('far fa-user-crown',
                                                          "And to Prof Jenny Taylor for all the feedback and patience"),
                                                         ('far fa-user-hard-hat',
                                                          "And Brian's group for the infrastructure*"),
                                                         ('far fa-user-md-chat',
                                                          "And the SGC code review group for feedback"),
                                                         ('far fa-user-graduate', '''And Jenny's group for beta testing the site and 
                                                                explaining countless times what an autozygous RPKM IGV plot is''')]) + \
                                                             '''<br/><hr/> <p>In case you were wondering the Greek god that runs the web app is Tyche (lady luck):</p>
                                                              <img src="https://www.greekmythology.com/images/mythology/tyche_amp_large_image_183.jpg"
                                                 alt="complicated" height="300">
                                                 <p><b>PS</b> Feel free to email me at matteo@well.ox.ac.uk</p>
                                                 '''))
    page.description += BS.deindent(modal)
    
