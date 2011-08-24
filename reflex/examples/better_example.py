
from reflex.data import Event
from reflex.control import EventManager
from reflex.interfaces import Reactor

class example(Reactor):
    
    name = 'example'
    
    def init(self):
        self.bind(self.handler, 'basic', source='main')
        self.bind(self.use_args, 'args')
    
    def handler(self, event, *args):
        print("Hello, world!")
    
    def use_args(self, event, *args):
        print("Event triggered by {0} since because {1}.".format(event.source, args[0]))
    
events = EventManager()
obj = example(events)

# The following event trigger is not handled by anything.
events.trigger(Event('basic'))
# The next event trigger is handled by the handler method.
events.trigger(Event('basic', [('source', 'main')]))
# This one is yes.
events.trigger(Event('args', [('source', 'main')]), 'pickles')
