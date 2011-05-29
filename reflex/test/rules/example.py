''' Example ruleset
'''

from reflex.interfaces import Ruleset as BaseRuleset

class Ruleset(BaseRuleset):
    
    def init(self, *args):
        self.reset_called()
    
    def reset_called(self):
        self.called = False
    
    def bind(self, source, meth, event, options=None, *additional):
        self.called = True
        return super(Ruleset, self).bind(source, meth, event, options, *additional)
    
    def unbind(self, source, meth, event, options=None):
        self.called = True
        return super(Ruleset, self).bind(source, meth, event, options)
    
    def run(self, binding, data, rules, *args):
        self.called = True
        return super(Ruleset, self).run(binding, data, rules, *args)

# EOF