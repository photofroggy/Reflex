========
Reflex
========

reflex is an event system for python applications.

The package, written for Python 3.1, provides a way for applications to manage events and event listeners, with little effort.

While the system is somewhat more complex than existing event systems, I feel it is more flexible, and more powerful.

Here is the most basic example::

    from reflex.data import Event
    from reflex.control import EventManager
    
    events = EventManager()
    
    def handler(event, *args):
        print("Hello, world!")
    
    events.bind('main application', handler, 'example')
    
    events.trigger(Event('example'))
    # prints "Hello, world!"

The example provided above seems far too complicated for what it does, but the system is intended to be used differently.

Here is a better example::

    from reflex.data import Event
    from reflex.control import EventManager
    from reflex.interfaces import reactor
    
    class example(reactor):
        
        name = 'example'
        
        def __inst__(self):
            self.bind(self.handler, 'basic')
        
        def handler(self, event, *args):
            print("Hello, world!")
        
    events = EventManager()
    obj = example(events)
    events.trigger(Event('basic'))
    # Prints "Hello, world!"

Still a bit simple in that it doesn't really show the system's capabilities or benefits. Below is an example that hints at the capabilites::

    from reflex.data import Event
    from reflex.control import EventManager
    from reflex.interfaces import reactor
    
    class example(reactor):
        
        name = 'example'
        
        def __inst__(self):
            self.bind(self.handler, 'basic', ['main'])
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

It may seem complicated and not make any sense but documentation shall be available in time.
