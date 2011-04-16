''' ReactorPlatform unittest
    Created by photofroggy.
    
    This unittest tests Reactor subclassing.
'''

import unittest
# reflex imports
from reflex.data import Event
from reflex.control import EventManager
from reflex.control import ReactorPlatform
# Test reactors
from reflex.test import reactors


class TestReactorPlatform(unittest.TestCase):
    
    def setUp(self):
        self.events = EventManager()
    
    def test_loading_reactors(self):
        # Test loading reactors into a platform.
        print('')
        good_platform = ReactorPlatform(debug=True)
        bad_platform = ReactorPlatform(debug=True)
        
        # This should fail
        bad_platform.load_reactors(reactors, 'Extension', self.events)
        self.assertFalse(len(bad_platform.loaded) > 0,
            'Reactors loaded into the wrong platform')
        
        # This should do the trick
        good_platform.load_reactors(reactors, 'Plugin', self.events)
        self.assertTrue(len(good_platform.loaded) > 0, 'Reactors loaded by the right platform')
    
if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestReactorPlatform)
    unittest.TextTestRunner(verbosity=2).run(suite)

# EOF
