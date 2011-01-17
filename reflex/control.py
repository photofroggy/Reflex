''' Events system for Python.
    Created by photofroggy.
    Released under GNU GPL v3.
    
    The idea of this was to keep things simple but still alow things to be
    quite powerful. Therefore I have introduced the idea of "event rules",
    where events can have a class assigned to them to handle bindings,
    unbindings, and triggers.
    
    Hopefully this will allow for a flexible and powerful module system.
'''

# Standard Lib imports.
import os
import sys
import inspect
from copy import copy
from functools import wraps
from collections import Callable
# Reflex imports
from reflex.data import Event
from reflex.data import Binding
from reflex.interfaces import Ruleset

def writeout(message=''):
    sys.stdout.write('{0}\n'.format(message))

class EventManager:
    """ The EventManager class provides a simple way to manage
        events and their bindings. This is one of the main things
        that application developers should be interested in using.
        
        Using the EventManager class is simple. All you have to do
        is make an instance of the class, then create event bindings
        using the ``bind()`` method. Once you have done that, you can trigger
        events using the ``trigger()`` method. A simple example is below::
        
            from reflex.data import Event
            from reflex.control import EventManager
            
            events = EventManager()
            
            def example(event, *args):
                print('Hello, world')
            
            events.bind('main app', example, 'test')
            
            events.trigger(Event('test'))
        
        The above example does not show the full power of the system. View
        the tutorials to get a better idea of how things can be used.
    """
    
    class info:
        version = 1
        build = 1
        stamp = 000000000
        name = 'Instinct'
        state = 'Alpha'
    
    def __init__(self, output=writeout, debug=False, *args, **kwargs):
        self._write = writeout
        self.debug = debug
        self.map = {}
        self.rules = {}
        self.init(*args)
        self.load_rules(*args)
    
    def init(self, *args):
        """ This method is called by ``__init__``.
            
            On its own, it doesn't do anything. This is designed as a
            method which can be overridden by child classes so developers
            don't have to interfere with ``__init__``.
            
            This method is given the same input given to ``__init__``.
        """
        pass
    
    def load_rules(self, *args):
        """ Load any rulesets that are present in reflex.rules.
            
            The method loads and stores any rulesets that are found. By
            definition, rulesets must be extensions of
            ``reflex.interfaces.Ruleset``, and must also be named
            Ruleset. The ruleset is applied to events of the same name
            as the module that the ruleset is saved in. For example,
            the class ``reflex.rules.example.Ruleset`` will be applied
            to the example event.
        """
        import reflex.rules
        self.rules = {'default': Ruleset(args, self.map, self._write, self.debug)}
        for event, mod in reflex.rules.__modules__().items():
            if not hasattr(mod, 'Ruleset'):
                continue
            if not issubclass(mod.Ruleset, Ruleset):
                continue
            self.rules[event] = mod.Ruleset(args, self.map, self._write, self.debug)
    
    def bind(self, source, method, event, options=None, *additional):
        """ Bind a method to an event.
            
            Input parameters:
            
            * **source** - The origin of the method given to handle the
              event. This should be a name describing where the
              method may have come from, so different things may be
              appropriate in different applications.
            * **method** - This is a method that will be invoked when
              the event defined in the event parameter is triggered.
            * **event** - The event that the method is being bound to.
            * **options** - An iterable of conditions the event must
              meet. If given, then corresponding items provided
              when the event is triggered must match these items.
            * **additional** - Any additional arguments which developers
              may want to use in their systems.
            
            This is essentially the same concept as creating an event
            listener. The binding is actually done in the ruleset object
            being used for the event.
            
            If the event has no explicit ruleset, then the default
            ruleset is used (reflex.interfaces.Ruleset).
            
            Returns ``None`` on failure. Otherwise, returns the binding
            created. The event binding is an instance of the
            ``refelx.data.Binding`` class.
        """
        if not isinstance(method, Callable):
            return None
        key = 'default' if not event in self.rules.keys() else event
        return self.rules[key].bind(source, method, event, options, *additional)
    
    def unbind(self, source, method, event, options=None):
        """ Remove an event binding for a method.
            
            This is the reverse of the bind method. Once again, the
            unbinding is actually done by the ruleset object being used
            for the event.
        """
        key = 'default' if not event in self.rules.keys() else event
        return self.rules[key].unbind(source, method, event, options)
    
    def handler(self, event, options=None, *additional):
        """ Create an event handler.
            
            This method provides a decorator interface for the ``bind()``
            method.
            
            The ``source`` parameter for the ``bind()`` method is given
            the name of the callable, using ``callable.__name__``. A
            brief example is given below::
            
                from reflex.data import Event
                from reflex.control import EventManager
                
                events = EventManager()
                
                # Create an event handler using the decorator method.
                
                @events.handler('example')
                def my_handler(data, *args):
                    print('Hello, world!')
                
                # Trigger the 'example' event.
                events.trigger(Event('example'))
                # >>> Hello, world!
        """
        def decorate(func):
            if not isinstance(func, Callable):
                return func
            func.binding = self.bind(func.__name__, func, event, options, *additional)
            return func
        return decorate
    
    def trigger(self, data=None, *args):
        """ Trigger an event.
            
            Input parameters:
            
            * **data** - This parameter should be an event object, using
              either the ``reflex.data.Event`` class or a subclass of
              it.
            * **args** - Any other additional arguments that developers
              want to pass to event handlers.
            
            This method is mainly a wrapper for the ``run()`` method of
            the ruleset object being used for the event defined by the
            object given in the ``data`` parameter.
        """
        if not hasattr(data, 'name') or not hasattr(data, 'rules'):
            return []
        event = data.name
        rules = data.rules
        del data.rules
        if not event in self.map.keys():
            return []
        key = 'default' if not event in self.rules.keys() else event
        return [self.rules[key].run(binding, data, rules, *args) for binding in self.map[event]]
    
    def clear_bindings(self):
        """ This method removes all event bindings that are being stored
            in the event manager.
        """
        self.map = {}
        for rule in self.rules:
            self.rules[rule].set_map(self.map)
    
    def bindset(self, source):
        """ Returns a bindset.
            
            Input parameters:
            
            * **source** - The binding source to be used when binding or
              unbinding events.
            
            This method is only meant for use in
            ``reflex.interfaces.reactor``. This method returns a tuple
            containing both the ``bind()`` and ``unbind()`` methods,
            except that the methods have been wrapped to always use the
            same ``source`` parameter, as given to this method.
        """
        def wrapit(func):
            @wraps(func)
            def new(*args, **kwargs):
                return func(source, *args, **kwargs)
            return new
        return (wrapit(self.bind), wrapit(self.unbind))

# EOF
