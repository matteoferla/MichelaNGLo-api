from IPython.display import display, HTML
import uuid


class Progress:
    """
    Add a progressbar.
    Using https://getbootstrap.com/docs/4.3/components/progress/ not the HTML5 one.
    Note that Jupyter uses an older version: 3.4 (https://getbootstrap.com/docs/3.4/components/), but I doubt this will be so for long hence the color via style.
    Two uses different uses.

    Timer:
    >>> Progress().countdown(seconds) = the progressbar counts to n seconds every tick ms

    Manual
    >>> p = Progress(percent=20, label='hello') both percent and label are optional arguments
    >>> p.percent = 30
    >>> p.label = 'bye'
    Do note that `.percent` and `.label` do not check what the real value of the Progress bar is and rely on a previously stored value.
    Hence why they are incorrect for `.countdown()`.
    This is unavoidable as JS can run a IPython command only when the kernel is idle and this is needed to input values.
    Consequently, the method `.update('varname')` is provided which will check.
    The argument for .update is the name variable has in the Python mainspace as a string.
    Do note the update happens after the cell has finished excecuting. So
    >>> p = Progress(percent=20, label='hello')
    >>> print(p.percent, p.label) # correct
    >>> p.countdown(5)
    >>> time.sleep(1)
    >>> print(p.percent, p.label) # incorrect
    >>> p.update('p')
    >>> print(p.percent, p.label) # incorrect within the same cell, correct in next.
    The HTML element id of the bar is `.id`.
    """

    def __init__(self, percent=0, label=''):
        self.id = uuid.uuid1().hex
        self._percent = percent
        self._label = label
        display(HTML(f'''<div class="progress">
          <div id="{self.id}"
              class="progress-bar progress-bar-striped" role="progressbar"
              style="background-color: #ffc107; width: {self._percent}%;">
              {self._label}
          </div>
        </div>
        '''))

    def countdown(self, seconds, tick=1000):
        self._append(code=f'''
            window.timegone = {seconds * self.percent / 100}; // zero normally...
            window.killTimer = setInterval(() => {{
              if(++window.timegone > {seconds}) {{
                  clearInterval(killTimer);
                  $('#{self.id}').css('width', '100%')
                                 .removeClass('progress-bar-striped')
                                 .css('background-color','#28a745')
                                 .html('Complete');
              }} else {{$('#{self.id}').css('width', (window.timegone/{seconds}*100)+'%')}}
            }}, {tick});''')
        return self

    def _set_percent(self, percent):
        ## sets the progress to that percent
        self._percent = percent
        if percent < 100:
            self._append(code=f"$('#{self.id}').css('width', '{percent}%');")
        else:
            self._append(
                code=f"$('#{self.id}').css('width', '100%').css('background-color','#28a745').removeClass('progress-bar-striped');")
        return self

    def _set_label(self, label):
        # add a label
        self._label = label
        self._append(code=f"$('#{self.id}').html('{label}');")
        return self

    def update(self, name):
        ## name is a string with the name in the main namespace that the progress instance is called by
        self._append(
            code=f'''IPython.notebook.kernel.execute("{name}._label  = '"+$('#{self.id}').html().replace('\\n',' ')+"'");''')
        self._append(
            code=f'''IPython.notebook.kernel.execute("{name}._percent  = "+$('#{self.id}').width()/$('#{self.id}').parent().width() * 100);''')

    label = property(lambda self: self._label, _set_label)
    percent = property(lambda self: self._percent, _set_percent)

    def _unbloat(self, n):
        # a wee hack to stop newlines appearing.
        return f'$("#{n}").parent().parent().hide();'

    def _append(self, code, hidden=True):
        # adds JS
        n = uuid.uuid1().hex
        if hidden:
            code += '\n' + self._unbloat(n)
        display(HTML(f'''<script type="text/javascript" id='{n}'>
        {code}
        </script>'''))

