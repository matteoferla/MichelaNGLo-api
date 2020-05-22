try:
    from IPython.display import display, HTML
except ImportError:
    pass # not jupyter.

class page:
    """
    This class holds page data.
    And adds some extra conversion features.
    """
    def __init__(self, uuid):
        self.uuid = uuid

    def show_page_link(self) -> str:
        link = f'<a href="{self.url}data/{self.uuid}" target="_blank">{self.uuid}</a>'+\
                     f'<img alt="error" src="{self.url}thumb/{self.uuid}" height="200">'
        display(HTML(link))
        return link