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
import traceback
from functools import wraps
from collections import Callable
# Custom
from reflex.data import Binding

class Reactor:
    """ Reactor base class.
        
        Input parameters:
            
        * **manager** - This is a reference to an instance of a
          :ref:`reflex.control.EventManager <eventmanager>` object.
          This is used here to provide the base reactor class with the ``bind()``,
          ``unbind()``, ``handler()`` and ``trigger`` methods. For
          more information about these methods, see the
          documentation for the ``reflex.control.EventManager``
          class.
        * *args* and *kwargs* - Any additional parameters given here
          are passed to the ``init()`` method.
        
        In the reflex system, a *reactor* is an object containing several
        methods which react to *events*, based on certain parameters.
        The methods that react to events are usually referred to as
        *'event handlers'*.
        
        To define a method as an *event handler*, the method must be
        *bound* to an event using the ``bind()`` method. This creates an
        *event binding*. An *event binding* is an object (instance of
        ``reflex.data.Binding``) that holds information about the
        relationship between a method and an event.
        
        Developers adapting Reflex for their own applications are
        advised to use the ``reactor`` class as a base for any base
        classes they might want to create.
        
        To get an idea of how to properly create and use reactors, refer
        to the tutorials.
    """
    
    name = None
    
    def __init__(self, manager, *args, **kwargs):
        """ This method stores references to utility methods from the
            *event manager*.
        """
        self._bind = manager.bind
        self._unbind = manager.unbind
        self.trigger = manager.trigger
        
        if self.name is None:
            self.name = str(self.__class__).split('.')[-2].replace('_', ' ')
        
        self.init(*args, **kwargs)
    
    def init(self, *args, **kwargs):
        """ Reactor configuration.
            
            This is a do-nothing method. Subclasses should extend this
            method and use it to create *event bindings*.
        """
        pass
        
    def bind(self, method, event, options=None, *additional):
        """ This is a wrapper for :py:meth:`reflex.control.EventManager.bind`.
            The ``name`` attribute of this object is used as the binding
            ``source``.
        """
        return self._bind(self.name, method, event, options, *additional)
    
    def unbind(self, method, event, options=None):
        """ Another wrapper like ``bind``. """
        return self._unbind(self.name, method, event, options)
        
    def handler(self, event, options=None, *additional):
        """ Can be used as a decorator to bind events. """
        def decorate(func):
            if not isinstance(func, Callable):
                return func
            func.binding = self.bind(func, event, options, *additional)
            return func
        return decorate


class Ruleset:
    """ Default Ruleset.
        
        Input parameters:
        
        * *args* - Any arguments passed to the
          :ref:`event manager <eventmanager>` object when the instance
          is created.
        * *dict* **mapref** - A reference to the dictionary storing all of the
          event bindings stored in the system.
        * *callable* **stdout** - A reference to the method being used to write
          output to the screen. This is given by the :ref:`event manager
          <eventmanager>` object.
        * *callable* **stddebug** - A reference to the method being used to write
          debug messages to the screen. This is given by the :ref:`event manager
          <eventmanager>` object.
        
        The Ruleset object provides an interface for managing bindings
        and events on a per-event basis. One Ruleset is assigned to *one*
        type of event only.
        
        An instance of this class is used for all events that do not have
        a specific ruleset assigned to them.
    """

    def __init__(self, args, mapref, stdout, stddebug):
        self.mapref = mapref
        self._write = stdout
        self.debug = stddebug
        
        self.init(*args)
    
    def init(self, *args):
        """ init method.
            
            This method is called by the ``__init__()`` method.
            Subclasses should overwrite this method if they need to do
            anything on initialisation.
            
            This is a do-nothing method by default.
        """
        pass
    
    def set_map(self, mapref):
        """ Set the reference for the event map.
            
            Input parameters:
            
            * *dict* **mapref** - As in the ``__init__()`` method, this
              parameter is a reference to the dictionary storing all of
              the event bindings being stored in the event system.
            
            This method should only ever be called by the
            :ref:`event manager <eventmanager>` object's
            ``clear_bindings()`` method.
        """
        self.mapref = mapref

    def bind(self, source, meth, event, options=None, *additional):
        """ Create an event binding.
            
            This is the method called by the :ref:`event manager
            <eventmanager>` object's own ``bind()`` method. It ensures
            that there are no clashes between the given binding details
            and any existing event bindings.
            
            If there is a clash, then the method returns ``None``,
            otherwise an instance of the :ref:`Binding <data-binding>`
            class is returned. The instance is also added to the object
            referenced by ``self.mapref``.
        """
        options = options if options else []
        if event in self.mapref.keys():
            for binding in self.mapref[event]:
                if (binding.source, binding.call, binding.options) is (source, meth, options):
                    return None
        else: self.mapref[event] = []
        new_binding = Binding(source, meth, event, options, additional)
        self.mapref[event].append(new_binding)
        return new_binding
    
    def unbind(self, source, meth, event, options=None):
        """ Remove an event binding.
            
            Similar to the ``bind()`` method of this class, except the
            binding is removed rather than added. This method ``True``
            if a matching event binding was found and removed, ``False``
            if no bindings were removed.
        """
        rmd = False
        options = options if options else []
        if event in self.mapref.keys():
            for binding in self.mapref[event]:
                if (binding.source, binding.call, binding.options) == (source, meth, options):
                    del self.mapref[event][self.mapref[event].index(binding)]
                    rmd = True
                    break
        if event in self.mapref.keys():
            if not self.mapref[event]:
                del self.mapref[event]
        return rmd
    
    def run(self, binding, data, rules, *args):
        """ Run a given event binding.
            
            Input parameters:
            
            * **binding** - An instance of the :ref:`Binding
              <data-binding>` class.
            * **data** - An instance of the :ref:`Event <data-event>`
              class. This represents the event being triggered.
            * **rules** - This is a list of the items related to the
              event. Typically, these items are compared to the
              :ref:`binding's <data-binding>` own ``options`` list.
              Custom Rulesets may use both lists in their own way, if
              appropriate.
            * *args* - Additional arguments given to the :ref:`event
              manager's <eventmanager>` ``trigger()`` method.
        """
        if len(rules) < len(binding.options):
            return None
        last_item = len(rules)
        for i, option in enumerate(binding.options):
            # Ignore None
            if option is None:
                continue
            # Process event item i
            rule = rules[i]
            if isinstance(option, str):
                try:
                    if str(rule).lower() == option.lower():
                        continue
                except Exception:
                    return None
            if type(rule) != type(option):
                return None
            if rule == option:
                continue
            return None
        try:
            return binding.call(data, *args)
        except Exception as e:
            log = self._write
            log('Source "{0}" failed to handle event "{1}"!'.format(binding.source, binding.event))
            log('Error:')
            tb = traceback.format_exc().splitlines()
            for line in tb:
                log('>> {0}'.format(line))
        return None

# EOF
