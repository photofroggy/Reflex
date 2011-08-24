''' Ruleset unittest
    Copyright (c) 2011, Henry "photofroggy" Rapley.
    Released under the ISC License.
    
    This unittest tests Ruleset subclassing.
'''

import unittest
# reflex imports
from reflex.data import Event
from reflex.control import EventManager
# plugin reactor
from reflex.test.reactors import Example
# example ruleset
from reflex.test.rules import example

class TestRulesetLoading(unittest.TestCase):
    
    def setUp(self):
        self.events = EventManager()
        self.events.define_rules('example', example.Ruleset)
    
    def test_actually_loaded(self):
        # Test that the ruleset was properly loaded in the setup bit.
        
        self.assertTrue(len(self.events.rules) > 1,
            'No additional rulesets loaded. Further tests will fail')
        
        rules = self.events.rules.get('example', None)
        
        self.assertIsNotNone(rules,
            'Example ruleset not loaded properly. Further tests will fail')

            
class TestRuleset(unittest.TestCase):
    
    def setUp(self):
        self.events = EventManager()
        self.events.define_rules('example', example.Ruleset)
        self.rules = self.events.rules.get('example', None)
        self.reactor = Example.Plugin(self.events)
    
    def test_bind(self):
        self.assertTrue(self.rules.called,
            'Either the ruleset was not called or the reactor failed')
    
    def test_unbind(self):
        self.rules.reset_called()
        self.reactor.unbind(self.reactor.rule_test, 'example')
        self.assertTrue(self.rules.called,
            'Unbind called on the wrong object')
    
    def test_run(self):
        self.rules.reset_called()
        self.events.trigger(Event('example'))
        self.assertTrue(self.rules.called,
            'Event runner called on the wrong object')
    
if __name__ == '__main__':
    suite = unittest.TestSuite([
        unittest.TestLoader().loadTestsFromTestCase(TestRulesetLoading),
        unittest.TestLoader().loadTestsFromTestCase(TestRuleset)
    ])
    unittest.TextTestRunner(verbosity=2).run(suite)

# EOF
