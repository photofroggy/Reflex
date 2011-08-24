''' System unittest
    Copyright (c) 2011, Henry "photofroggy" Rapley.
    Released under the ISC License.
    
    This tests whether the battery system works together as a whole
    or not.
'''

import sys
import unittest
# reflex imports
from reflex.data import Event
from reflex.control import EventManager
from reflex.control import ReactorBattery
from reflex.control import RulesetBattery
# Rulesets
from reflex.test import rules
# Reactors
from reflex.test import reactors

class TestBatteryBasedSystem(unittest.TestCase):
    def runTest(self):
        
        sys.stdout.write('\n')
        
        # Load an event system
        events = EventManager() #stddebug=lambda n: sys.stdout.write('{0}\n'.format(n)))
        
        # Load rulesets
        rulesets = RulesetBattery() #stddebug=lambda n: sys.stdout.write('{0}\n'.format(n)))
        rulesets.load_objects(events, rules)
        
        self.assertIsNotNone(events.rules.get('example', None),
            'Failed to load test ruleset')
        
        # Load plugins!
        plugins = ReactorBattery() #stddebug=lambda n: sys.stdout.write('{0}\n'.format(n)))
        plugins.load_objects(events, reactors, 'Plugin')
        
        self.assertIsNotNone(events.map.get('example', None),
            'Event bindings failed')
        
        events.rules['example'].reset_called()
        
        # Fire an event!
        events.trigger(Event('example'))
        
        # Test Results!
        self.assertTrue(events.rules['example'].called,
            'Example ruleset not called properly')
        
        self.assertTrue(plugins.loaded['Example'].full_test,
            'Example reactor not called properly')
    
    
if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestBatteryBasedSystem)
    unittest.TextTestRunner(verbosity=2).run(suite)


# EOF
