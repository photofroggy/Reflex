''' Example reactor
    Copyright (c) 2011, Henry "photofroggy" Rapley.
    Released under the ISC License.

    Part of the ReactorBattery test.
'''

from reflex.base import Reactor

class Plugin(Reactor):
    
    def init(self):
        # Test flag
        self.handled = False
        # Full Test flag
        self.full_test = False
        
        # Create some event bindings.
        self.bind(self.evt_handler, 'basic')
        self.bind(self.evt_handler, 'conditional', condition=1)
        
        # Create decorated event handler
        @self.handler('decorated')
        def handler(event):
            self.handled = True
            
        # This is to help test ruleset subclassing
        self.bind(self.rule_test, 'example')
    
    def reset(self):
        self.handled = False
    
    def evt_handler(self, event):
        self.handled = True
    
    def rule_test(self, event):
        self.full_test = True
    
# EOF