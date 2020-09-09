from typing import Optional, List, Dict, Tuple

import re

def deindent(text: str) -> str:
    return re.sub('\s+', ' ', text)


def make_modal(title: str, body: str, id_attribute: str) -> str:
    modalblock = f'''<div class="modal fade" 
                          id="{id_attribute}" 
                          data-backdrop="static" data-keyboard="false" 
                          tabindex="-1" 
                          aria-labelledby="staticBackdropLabel" aria-hidden="true">
      <div class="modal-dialog modal-dialog-centered modal-xl">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title" id="staticBackdropLabel">{title}</h5>
            <button type="button" class="close" data-dismiss="modal" aria-label="Close">
              <span aria-hidden="true">&times;</span>
            </button>
          </div>
          <div class="modal-body">
            {body}
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>
          </div>
        </div>
      </div>
    </div>
    '''
    return modalblock


def make_carousel(bodies: list, id_attribute: str)  -> str:
    assert len(bodies) >= 2, 'You need two for a carousel'

    def inner(text, active=False):
        return f'''<div class="carousel-item {'active' if active else ''}" data-interval="false">
          <div class="w-100 h-100">
              {text}
          </div>
        </div>'''

    li_els = [f'<li class="bg-dark active" data-target="#{id_attribute}" data-slide-to="0"></li>'] + \
             [f'<li class="bg-dark" data-target="#{id_attribute}" data-slide-to="{i}"></li>' for i in
              range(1, len(bodies))]
    li_elblock = '\n'.join(li_els)
    div_els = [inner(bodies[0], active=True)] + [inner(bodies[i], active=False) for i in range(1, len(bodies))]
    div_elblock = '\n'.join(div_els)
    carouselblock = f'''
    <div id="{id_attribute}" class="carousel slide" data-interval="false" data-ride="carousel">
      <ol class="carousel-indicators">
        {li_elblock}
      </ol>
      <div class="carousel-inner" style="min-height: 800px;">
        {div_elblock}
      </div>
      <a class="carousel-control-prev text-dark" href="#{id_attribute}" role="button" data-slide="prev">
        <i class="fas fa-caret-left  fa-2x text-dark"></i>
        <span class="sr-only">Previous</span>
      </a>
      <a class="carousel-control-next  text-dark" href="#{id_attribute}" role="button" data-slide="next">
        <i class="fas fa-caret-right  fa-2x text-dark"></i>
        <span class="sr-only">Next</span>
      </a>
    </div>
    '''
    return carouselblock


def make_list(entries: list, id_attribute: Optional[str] = None, ordered=False) -> str:
    lis = ' '.join([f'<li class="list-group-item">{entry}</li>' for entry in entries])
    if ordered:
        el = 'ol'
    else:
        el = 'ul'
    if id_attribute:
        ol = f'''<{el} class="list-group" id="{id_attribute}">{lis}</{el}>'''
    else:
        ol = f'''<{el} class="list-group">{lis}</{el}>'''
    return ol


def make_FA_list(entries: List[Tuple[str, str]], id_attribute: Optional[str] = None) -> str:
    lis = ' '.join([f'<li><span class="fa-li"><i class="{fa}"></i></span>{entry}</li>' for fa, entry in entries])
    if id_attribute:
        ul = f'''<ul class="fa-ul" id="{id_attribute}">{lis}</ul>'''
    else:
        ul = f'''<ul class="fa-ul">{lis}</ul>'''
    return ul


def make_slide(title: str, body: str) -> str:
    return f'''<div class="p-5">
<h1>{title}</h1>

<br/>

    <div style="font-size: 1.5em;">
        {body}
    </div>

</div>
'''


def make_header_slide(title: str, subtitle: str) -> str:
    if subtitle:
        wrapped_sub = f'<hr class="my-4"/><p class="lead">{subtitle}</p>'
    else:
        wrapped_sub = ''
    return f'<div class="jumbotron p-5"><h1 class="display-4">{title}</h1>{wrapped_sub}</div>'
