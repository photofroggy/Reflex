''' Reactor unittest
    Created by photofroggy.
    
    This unittest tests Reactor subclassing.
'''

import unittest
# reflex imports
from reflex.data import Event
from reflex.control import EventManager
from reflex.interfaces import Reactor

class MyReactor(Reactor):
    
    def init(self):
        # Test flag
        self.handled = False
        
        # Create some event bindings.
        self.bind(self.evt_handler, 'basic')
        self.bind(self.evt_handler, 'conditional', [1])
        self.bind(self.evt_handler, 'ignored', [None, 1])
        
        # Create decorated event handler
        @self.handler('decorated')
        def handler(event):
            self.handled = True
    
    def reset(self):
        self.handled = False
    
    def evt_handler(self, event):
        self.handled = True


class TestReactor(unittest.TestCase):
    
    def setUp(self):
        self.events = EventManager()
        self.reactor = MyReactor(self.events)
    
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
    
    def test_ignorant_event(self):
        # Test an ignored condition event
        
        # Should be false.
        self.events.trigger(Event('ignored',
            [('ignore', 1), ('condition', 0)]))
        self.assertFalse(self.reactor.handled,
            'Ignorant event handler called for the wrong event')
        
        # Shoud be true
        self.events.trigger(Event('ignored',
            [('ignore', 1), ('condition', 1)]))
        self.assertTrue(self.reactor.handled, 'Ignorant event handler not called')
        
        self.reactor.reset()
    
    def test_decorated_event(self):
        # Test an decorated event
        
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
