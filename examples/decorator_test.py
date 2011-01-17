
from reflex.data import Event
from reflex.control import EventManager
from reflex.interfaces import reactor

# Create an event manager
events = EventManager()

# Create an event handler
@events.handler('basic')
def example(event, *args):
    print("Hello, world!")

# Trigger the event.
events.trigger(Event('basic'))

# Odd test! Gets funky beyong this point.
class exampler(reactor):
    
    name = 'Funky decorator hack'
    
    def init(self):
        
        @self.handler('funky')
        def handler(event, *args):
            print(self.name)
        
    
exampler(events)
events.trigger(Event('funky'))
