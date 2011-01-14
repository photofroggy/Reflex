''' Reactor interface for Reflex events.
    Created by photofroggy.
    Released under GNU GPL v3.
    
    This module provides interfaces for different parts of the event
    system. The one that will be most commonly used by other developers
    is the reactor class.
'''

# Standard Lib imports.
import os
import sys
import inspect
from functools import wraps
# Custom
from reflex.data import Binding

class reactor:
    """ This object is a basic API for reactors! """
    
    name = 'Base Reactor'
    
    def __init__(self, manager, *args, **kwargs):
        """ Initialise the reactor! Do not overwrite this method, use
            __inst__ instead!
        """
        self.bind, self.unbind = manager.bindset(self.name)
        self.trigger = manager.trigger
        self.__inst__(*args, **kwargs)
    
    def __inst__(self, *args, **kwargs):
        pass
    
class Ruleset:

    def __init__(self, args, mapref, output, dbug):
        self.mapref = mapref
        self._write = output
        self.debug = dbug
        self.__inst__(*args)
    
    def __inst__(self, *args):
        """Overwrite this method, not __init__!"""
        pass

    def bind(self, source, meth, event, options=None, *additional):
        """Extensions can create event bindings. When they do, the information comes through here."""
        options = options if options else []
        if event in self.mapref.keys():
            for binding in self.mapref[event]:
                if (binding.source, binding.call, binding.options) is (source, meth, options):
                    return None
        else: self.mapref[event] = []
        new_binding = Binding(source, meth, event, [str(i) for i in options], additional)
        self.mapref[event].append(new_binding)
        return new_binding
    
    def unbind(self, source, meth, event, options=None):
        """Remove an event binding from the events system!"""
        options = options if options else []
        if event in self.mapref.keys():
            for binding in self.mapref[event]:
                if (binding.source, binding.call, binding.options) == (source, meth, options):
                    del self.mapref[event][self.mapref[event].index(binding)]
                    break
        if event in self.mapref.keys():
            if not self.mapref[event]:
                del self.mapref[event]
    
    def run(self, binding, data, rules, *args):
        """Attempt to execute a given event binding."""
        for i, option in enumerate(binding.options):
            if option is None:
                continue
            rule = rules[i]
            if isinstance(option, str):
                if str(rule).lower() == option.lower():
                    continue
            if type(rule) != type(option): return None
            if rule == option: continue
            return None
        try:
            binding.call(data, *args)
        except Exception as e:
            log = self._write
            log('>> Source "{0}" failed to handle event "{1}"!'.format(binding.source, data.name))
            log('>> Error message: {0}.'.format(e.args[0]))
        return None

# EOF
