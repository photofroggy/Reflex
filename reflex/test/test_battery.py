''' ReactorBattery unittest
    Copyright (c) 2011, Henry "photofroggy" Rapley.
    Released under the ISC License.
    
    This unittest tests Reactor subclassing.
'''

import sys
import unittest
# reflex imports
from reflex.control import EventManager
from reflex.control import ReactorBattery
from reflex.control import RulesetBattery
# Test reactors
from reflex.test import rules
from reflex.test import reactors

def debug(message=''):
    sys.stdout.write('{0}\n'.format(message))

class TestReactorBattery(unittest.TestCase):
    
    def setUp(self):
        self.events = EventManager()
    
    def test_loading_reactors(self):
        # Test loading reactors into a battery.
        # sys.stdout.write('\n')
        # Add `stddebug=debug` to the constructors here to see debug messages
        # during the tests.
        good_battery = ReactorBattery(lambda n: None)
        bad_battery = ReactorBattery(lambda n: None)
        
        # This should fail
        bad_battery.load_objects(self.events, reactors, 'Extension')
        self.assertFalse(len(bad_battery.loaded) > 0,
            'Reactors loaded into the wrong battery')
        
        # This should do the trick
        good_battery.load_objects(self.events, reactors, 'Plugin')
        self.assertTrue(len(good_battery.loaded) > 0, 'Reactors not loaded by the right battery')


class TestRulesetBattery(unittest.TestCase):
    
    def setUp(self):
        self.events = EventManager()
    
    def test_loading_rulesets(self):
        # Test loading rulesets into a battery.
        # sys.stdout.write('\n')
        # Add `stddebug=debug` to the constructors here to see debug messages
        # during the tests.
        good_battery = RulesetBattery(lambda n: None)
        bad_battery = RulesetBattery(lambda n: None)
        
        # This should fail
        bad_battery.load_objects(self.events, rules, 'Wrong')
        self.assertFalse(len(bad_battery.loaded) > 0,
            'Rulesets loaded into the wrong battery')
        
        # This should do the trick
        good_battery.load_objects(self.events, rules,)
        self.assertTrue(len(good_battery.loaded) > 0, 'Rulesets not loaded by the right battery')
    
if __name__ == '__main__':
    suite1 = unittest.TestLoader().loadTestsFromTestCase(TestReactorBattery)
    suite2 = unittest.TestLoader().loadTestsFromTestCase(TestRulesetBattery)
    tests = unittest.TestSuite([suite1, suite2])
    unittest.TextTestRunner(verbosity=2).run(tests)

# EOF
