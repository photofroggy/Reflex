''' Reflex data objects.
    Created by photofroggy.
    Released under GNU GPL v3.
    
    This module contains data objects used in Reflex!
    Mainly just the Binding and Event classes!
'''

class Binding:
    """Event binding. Each instance represents a different binding."""
    
    source = None
    call = None
    options = []
    additional = []
    type = None
    
    def __init__(self, source, method, event, options, additional):
        """All the given values are stored on instantiation of an event binding."""
        self.source = source
        self.call = method
        self.options = options
        self.additional = additional
        self.type = '<event[\''+event+'\'].binding>'
        self.__inst__()
        
    def __inst__(self):
        """Overwrite this method when doing stuff on instantiation."""
        pass

class Event:
    """Event class. The objects represent different events!"""
    
    def __init__(self, event, data=[]):
        self.name = event
        self.rules = []
        for key, value in data:
            if key.lower() == 'rules':
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
