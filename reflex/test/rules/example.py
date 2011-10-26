''' Example ruleset
    Copyright (c) 2011, Henry "photofroggy" Rapley.
    Released under the ISC License.
'''

from reflex.base import Ruleset as BaseRuleset

class Ruleset(BaseRuleset):
    
    def init(self, *args):
        self.reset_called()
    
    def reset_called(self):
        self.called = False
    
    def bind(self, meth, event, **options):
        self.called = True
        return super(Ruleset, self).bind(meth, event, **options)
    
    def unbind(self, meth, event, **options):
        self.called = True
        return super(Ruleset, self).bind(meth, event, **options)
    
    def run(self, binding, data, *args):
        self.called = True
        return super(Ruleset, self).run(binding, data, *args)

# EOF