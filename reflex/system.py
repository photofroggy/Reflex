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

class Pulse:
    
    Map = {}
    rules = {}
    reloading = False
    debug = False
    
    def __init__(self, args=[], output=sys.stdout.write, dbug=False):
        self._write = output
        self.debug = dbug
        self.__inst__(args, output, dbug)
        self.load_rules(args)
        
    def __inst__(self, args, output, debug):
        pass
    
    def load_rules(self, args):
        import reflex.rules
        self.rules = {'default': Ruleset(args, self.Map, self._write, self.debug)}
        for evt_name, mod in reflex.rules.__modules__().items():
            if hasattr(mod, 'Ruleset'):
                if not issubclass(mod.Ruleset, Ruleset):
                    self._write('>> Failed to load rules for event ' + evt_name + '.')
                    self._write('>> Ruleset provided is not a sub-ruleset.')
                    continue
                self.rules[evt_name] = mod.Ruleset(args, self.Map, self._write, self.debug) # Thems tha rulez!
                continue
            self._write('>> Failed loading rules for event ' + evt_name + '.')
                
    def bind(self, source, meth, event, options=None, *additional):
        """Extensions can create event bindings. When they do, the information comes through here."""
        options = options if options else []
        if not isinstance(meth, Callable):
            self._write('>> Source {0} tried to bind non-existent method {1}.'.format( source, meth.__name__ ))
            return None
        key = 'default' if not event in self.rules.keys() else event
        return self.rules[key].bind(source, meth, event, options, *additional)
    
    def unbind(self, source, meth, event, options=None):
        """Remove an event binding from the events system!"""
        options = options if options else []
        if not isinstance(meth, Callable):
            self._write('>> Source '+source+' provided a non-method for unbinding.')
            return None
        key = 'default' if not event in self.rules.keys() else event
        self.rules[key].unbind(source, meth, event, options)
        return True
    
    def trigger(self, data, *args):
        """Events are triggered by this method. Other methods and rulesets may be called."""
        if not hasattr(data, 'name') or not hasattr(data, 'rules'):
            return []
        event = data.name
        rules = data.rules
        del data.rules
        if not event in self.Map.keys():
            return []
        key = 'default' if not event in self.rules.keys() else event
        if hasattr(self.rules[key], 'trigger'):
            return self.rules[key].trigger(data, rules, *args)
        return [self.rules[key].run(binding, data, rules, *args) for binding in self.Map[event]]

    def bindset(self, source):
        def wrapit(func):
            @wraps(func)
            def new(*args, **kwargs):
                return func(source, *args, **kwargs)
            return new
        return (wrapit(self.bind), wrapit(self.unbind))
    
    def clear_bindings(self):
        """ Clear event bindings! """
        bindings = copy(self.Map)
        for event in bindings.keys():
            for binding in bindings[event]:
                self.unbind(binding.source, binding.call, event, binding.options)

# EOF
