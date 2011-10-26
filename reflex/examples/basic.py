
from reflex.data import Event
from reflex.control import EventManager

events = EventManager()

def handler(event, *args):
    print("Hello, world!")

events.bind(handler, 'example')

events.trigger(Event('example'))
# prints "Hello, world!"
