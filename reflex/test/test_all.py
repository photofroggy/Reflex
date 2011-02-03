
if __name__ == '__main__':
    # Run all test suites if the test package is run as a script!
    # Start with the imports
    import unittest
    from reflex.test.test_basic_events import TestBasicEvents
    from reflex.test.test_reactor import TestReactor
    
    # Create the test suites
    basic_event_suite = unittest.TestLoader().loadTestsFromTestCase(TestBasicEvents)
    reactor_suite = unittest.TestLoader().loadTestsFromTestCase(TestReactor)
    
    # Group the suites
    tests = unittest.TestSuite([
        basic_event_suite,
        reactor_suite
    ])
    
    # Run the tests
    unittest.TextTestRunner(verbosity=2).run(tests)
