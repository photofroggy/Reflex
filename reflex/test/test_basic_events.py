''' Test basic events.
    
    Unit tests for basic reflex events.
'''

import unittest
# import the reflex stuffs
from reflex.data import Event
from reflex.data import Binding
from reflex.control import EventManager

class TestBasicEvents(unittest.TestCase):
    
    def test_basic_event(self):
        mgr = EventManager()
        
        self.handled = False
        
        def handler(event):
            self.handled = True
        
        binding = mgr.bind('mgr_test', handler, 'basic')
        self.assertEqual(binding.__class__, Binding,
            'EventManager().bind() returned something other than an instance of Binding')
        
        mgr.trigger(Event('something'))
        self.assertFalse(self.handled, 'Basic event handler called for the wrong event')
        
        mgr.trigger(Event('basic'))
        self.assertTrue(self.handled, 'Basic event handler not called')
    
    def test_conditional_event(self):
        mgr = EventManager()
        
        self.handled = False
        
        def handler(event):
            self.handled = True
        
        binding = mgr.bind('mgr_test', handler, 'basic', [1])
        self.assertEqual(binding.__class__, Binding,
            'EventManager().bind() returned something other than an instance of Binding')
        
        mgr.trigger(Event('basic'))
        self.assertFalse(self.handled, 'Conditional event handler called for the wrong event')
        
        mgr.trigger(Event('basic', [('condition', 0)]))
        self.assertFalse(self.handled, 'Conditional event handler called for the wrong event')
        
        mgr.trigger(Event('basic', [('condition', 1)]))
        self.assertTrue(self.handled, 'Conditional event handler not called')
    
    def test_ignore_condition(self):
        mgr = EventManager()
        
        self.handled = False
        
        def handler(event):
            self.handled = True
        
        binding = mgr.bind('mgr_test', handler, 'basic', [None, 1])
        self.assertEqual(binding.__class__, Binding,
            'EventManager().bind() returned something other than an instance of Binding')
        
        mgr.trigger(Event('basic'))
        self.assertFalse(self.handled, 'Ignorant event handler called for the wrong event')
        
        mgr.trigger(Event('basic', [('ignore', 1)]))
        self.assertFalse(self.handled, 'Ignorant event handler called for the wrong event')
        
        mgr.trigger(Event('basic', [('ignore', 1), ('condition', 0)]))
        self.assertFalse(self.handled, 'Ignorant event handler called for the wrong event')
        
        mgr.trigger(Event('basic', [('ignore', 1), ('condition', 1)]))
        self.assertTrue(self.handled, 'Ignorant event handler not called')
    
    def test_basic_decorator_event(self):
        mgr = EventManager()
        handles = mgr.handler
        
        self.handled = False
        
        @handles('basic')
        def handler(event):
            self.handled = True
        
        self.assertTrue(hasattr(handler, 'binding'),
            'Decorator did not apply a binding to the handler')
        
        self.assertEqual(handler.binding.__class__, Binding,
            'Decorator applied something other than an instance of Binding')
        
        mgr.trigger(Event('something'))
        self.assertFalse(self.handled, 'Decorated event handler called for the wrong event')
        
        mgr.trigger(Event('basic'))
        self.assertTrue(self.handled, 'Decorated event handler not called')
    
if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestBasicEvents)
    unittest.TextTestRunner(verbosity=2).run(suite)

# EOF
