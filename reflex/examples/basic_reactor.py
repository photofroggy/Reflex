
from reflex.data import Event
from reflex.control import EventManager
from reflex.interfaces import Reactor

class example(Reactor):
    
    name = 'example'
    
    def init(self):
        self.bind(self.event_handler, 'basic')
    
    def event_handler(self, event, *args):
        print("Hello, world!")
    
events = EventManager()
obj = example(events)
events.trigger(Event('basic'))
# Prints "Hello, world!"
