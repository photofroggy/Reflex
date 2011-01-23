''' Reflex data objects.
    Created by photofroggy.
    Released under GNU GPL v3.
    
    This module contains data objects used in Reflex!
    Mainly just the Binding and Event classes!
'''

class Binding:
    """ Event binding.
    
        Each instance represents a different binding. A binding stores
        information showing how a certain method is related to a certain
        event. Different attributes define the conditions for the
        relationship. The attributes are as follows:
        
        * *str* **source** - The source defines a name describing where
          the binding came from, or what the method belongs to.
        * *callable* **call** - The method used to handle the specified
          event.
        * *str* **event** - The name of the event that the method
          defined in ``call`` is used to handle.
        * *list* **optoins** - This list defines a set of items that,
          when defined, must match the respective items provided when
          the event defined by ``event`` is triggered. If the items do
          not match, then the handler is not used. Different Rulesets
          can modify this behaviour.
        * *list* **additional** - Any additional information about the
          binding.
        * *str* **type** - A string representation of the binding.
        
        The constructor of this class takes the above fields as input,
        apart from ``type``.
    """
    
    source = None
    call = None
    event = None
    options = []
    additional = []
    type = None
    
    def __init__(self, source, method, event, options, additional):
        """All the given values are stored on instantiation of an event binding."""
        self.source = source
        self.call = method
        self.event = event
        self.options = options
        self.additional = additional
        self.type = '<event[\''+event+'\'].binding>'
        self.__inst__()
        
    def __inst__(self):
        """Overwrite this method when doing stuff on instantiation."""
        pass

class Event:
    """ Event class.
        
        Instances of this class are used to represent events, and store
        information specific to the event being represented. The
        constructor takes the following input:
        
        * *str* **event** - The name of the event that the object
          represents.
        * *list* **data** - The data relating to the event being
          represented by the object.
        
        The event name is stored under the attribute ``name``. The
        ``data`` parameter should be a list of pairs, defining a key and
        a value each. The object stores these ``(key, value)`` pairs as
        ``obj.<key> = <value>``.
    """
    
    def __init__(self, event, data=[]):
        self.name = event
        self.rules = []
        for key, value in data:
            if key.lower() in ['rules', 'name']:
                continue
            setattr(self, key, value)
            self.rules.append(value)
        self.__inst__(event, data)
    
    def __inst__(self, event, data):
        """Overwrite this method if you need to do stuff on instatiation. Do not overwrite __init__."""
        pass
    
    def __str__(self):
        return '<event[\'' + self.name + '\']>'
    
# EOF
