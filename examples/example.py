''' Just an example of how to use reactors and stuff.
    Probably not a good idea.
    It works! But I need to make it better!
    
    This example produces the following output on the command line:
    
    << Reflexing! Provoking other reactors!
    >> example one touched me! Stop that!
    >> Oh shit... into darkness we go...
    << Reflexing! Provoking other reactors!
    >> example one touched me! Stop that!
    << Oh stop complaining, you fool.
'''

import sys
from reflex.data import Event
from reflex.control import EventManager
from reflex.interfaces import Reactor

class main:
    def __init__(self):
        self.events = EventManager()
        self.load()
        self.events.trigger(Event('reload'))
    
    def load(self):
        self.reactors = []
        self.reactors.append(example(self.events))
        self.reactors.append(example2(self.events))
        self.events.bind('main app', self.reload, 'reload')
        self.events.trigger(Event('ready'))
    
    def reload(self, event=None, *args):
        self.events.trigger(Event('reloading'))
        self.events.clear_bindings()
        self.reactors = []
        self.load()
        self.events.trigger(Event('reloaded'))
    
class example(Reactor):
    
    name = 'example one'
    
    def init(self):
        self.bind(self.e_ready, 'ready')
        self.bind(self.e_reloaded, 'reloaded')
        
    def e_ready(self, event):
        sys.stdout.write('<< Reflexing! Provoking other reactors!\n')
        self.trigger(Event('provoke', [('source', self.name)]))
    
    def e_reloaded(self, event):
        sys.stdout.write('<< Oh stop complaining, you fool.\n')
    
class example2(Reactor):
    
    name = 'example two'
    
    def init(self):
        self.bind(self.e_provoke, 'provoke')
        self.bind(self.e_reloading, 'reloading')
    
    def e_provoke(self, event):
        sys.stdout.write('>> {0} touched me! Stop that!\n'.format(event.source))
    
    def e_reloading(self, event):
        sys.stdout.write('>> Oh shit... into darkness we go...\n')
        
    
if __name__ == '__main__':
    main()

# EOF
