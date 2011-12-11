''' Reflex setup.
'''

from distutils.core import setup

setup(name='Reflex-events',
    version='1.14',
    description='Event system for Python',
    author='photofroggy',
    author_email='froggywillneverdie@msn.com',
    url='http://photofroggy.github.com/Reflex/index.html',
    packages=[
        'reflex',
        'reflex.test',
        'reflex.test.reactors',
        'reflex.test.rules',
        'reflex.examples'
    ],
    platforms=['Any'],
    classifiers=[
        'Natural Language :: English',
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'License :: OSI Approved :: ISC License (ISCL)',
        'Topic :: Software Development :: Libraries :: Application Frameworks'
    ],
    long_description="""
**Reflex** is an event system for applications made using **Python**.

The package provides a way for applications to manage events and event listeners, with little effort.

While the system is somewhat more complex than existing event systems, I feel it is more flexible, and more powerful.

Below is an example that hints at the capabilites of Reflex::

    from reflex.data import Event
    from reflex.control import EventManager
    from reflex.interfaces import Reactor
    
    class example(Reactor):
        
        name = 'example'
        
        def __inst__(self):
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

Documentation and a package reference can be found at
http://photofroggy.github.com/Reflex/index.html

The purpose of this package is to make creating an event driven plugin system
for your application an effortless task. A full plugin system can created in
just a few lines, as shown here::
    
    from reflex.data import Event
    from reflex.control import EventManager
    from reflex.control import ReactorBattery
    import plugins
    
    # Create an event manager.
    events = EventManager()
    
    # Create a battery.
    battery = ReactorBattery()
    # Load our plugins.
    battery.load_objects(events, plugins, 'Plugin')
    
    # Plugins can now be accessed as such:
    #   battery.loaded[plugin_name]
    # Events can be fired as follows:
    #   events.trigger(Event('my event'))
    # Easy as pie!
    
The above example assumes your plugins are stored in a package called
``plugins``.
"""
)

# EOF
