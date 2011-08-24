''' Main test suite for reflex.
    Copyright (c) 2011, Henry "photofroggy" Rapley.
    Released under the ISC License.
'''

if __name__ == '__main__':
    # Run all test suites if the test package is run as a script!
    # Start with the imports
    import unittest
    from reflex.test.test_basic_events import TestBasicEvents
    from reflex.test.test_reactor import TestReactor
    from reflex.test.test_ruleset import TestRulesetLoading
    from reflex.test.test_ruleset import TestRuleset
    from reflex.test.test_battery import TestReactorBattery
    from reflex.test.test_battery import TestRulesetBattery
    from reflex.test.test_battery_system import TestBatteryBasedSystem
    
    # Create the test suites
    basic_event_suite = unittest.TestLoader().loadTestsFromTestCase(TestBasicEvents)
    reactor_suite = unittest.TestLoader().loadTestsFromTestCase(TestReactor)
    rule_suite = unittest.TestSuite([
        unittest.TestLoader().loadTestsFromTestCase(TestRulesetLoading),
        unittest.TestLoader().loadTestsFromTestCase(TestRuleset)
    ])
    battery_suite = unittest.TestSuite([
        unittest.TestLoader().loadTestsFromTestCase(TestReactorBattery),
        unittest.TestLoader().loadTestsFromTestCase(TestRulesetBattery)
    ])
    bbs_suite = unittest.TestLoader().loadTestsFromTestCase(TestBatteryBasedSystem)
    
    # Group the suites
    tests = unittest.TestSuite([
        basic_event_suite,
        reactor_suite,
        rule_suite,
        battery_suite,
        bbs_suite
    ])
    
    # Run the tests
    unittest.TextTestRunner(verbosity=2).run(tests)
