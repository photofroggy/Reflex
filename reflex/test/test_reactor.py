''' Reactor unittest
    Copyright (c) 2011, Henry "photofroggy" Rapley.
    Released under the ISC License.
    
    This unittest tests Reactor subclassing.
'''

import unittest
# reflex imports
from reflex.data import Event
from reflex.control import EventManager
# plugin reactor
from reflex.test.reactors import Example

class TestReactor(unittest.TestCase):
    
    def setUp(self):
        self.events = EventManager()
        self.reactor = Example.Plugin(self.events)
    
    def test_basic_event(self):
        # Test a basic event
        
        # This should not call evt_handler
        self.events.trigger(Event('something'))
        self.assertFalse(self.reactor.handled,
            'Basic event handler called for the wrong event')
        
        #This should do the trick
        self.events.trigger(Event('basic'))
        self.assertTrue(self.reactor.handled, 'Basic event handler not called')
        
        self.reactor.reset()
    
    def test_conditional_event(self):
        # Test a conditional event
        
        # Should be false.
        self.events.trigger(Event('conditional', [('condition', 0)]))
        self.assertFalse(self.reactor.handled,
            'Conditional event handler called for the wrong event')
        
        # Shoud be true
        self.events.trigger(Event('conditional', [('condition', 1)]))
        self.assertTrue(self.reactor.handled, 'Conditional event handler not called')
        
        self.reactor.reset()
    
    def test_decorated_event(self):
        # Test a decorated event
        
        # Should be false.
        self.events.trigger(Event('something'))
        self.assertFalse(self.reactor.handled,
            'Event handler called for the wrong event')
        
        # Shoud be true
        self.events.trigger(Event('decorated'))
        self.assertTrue(self.reactor.handled, 'Decorated event handler not called')
        
        self.reactor.reset()
    
if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestReactor)
    unittest.TextTestRunner(verbosity=2).run(suite)

# EOF
