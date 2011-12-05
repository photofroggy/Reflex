''' Testing out the command stuff.
    Only a crappy brief example and stuffs.
'''


import os
import sys

sys.path.append(os.getcwd())

from reflex.base import Reactor
from reflex.control import EventManager

from reflex.examples.commands import rules
from reflex.examples.commands import data


class Example(Reactor):
    
    def init(self):
        self.bind(self.cmd, 'command', cmd='cmd')
        self.bind(self.cmd, 'command', cmd='cmd')
    
    def cmd(self, event, **args):
        print 'hi'



def writeout(msg=''):
    sys.stdout.write('{0}\n'.format(msg))
    sys.stdout.flush()

events = EventManager(stddebug=writeout)
events.define_rules('command', rules.Ruleset)

e = Example(events)

print 'bound commands:'
for item in events.map['command']:
    print '>', item.options['cmd']

cmd = data.Command('command', [
    ('trigger', 'cmd'),
    ('channel', 'chat:Botdom'),
    ('user', 'photofroggy'),
    ('message', 'cmd sub lol'),
    ('priv', 'Guests')])

print '-------------------------'
print 'firing commands'

print '> expecting \'hi\''
events.trigger(cmd)

cmd.trigger = 'foo'

print '> expecting command not found'
events.trigger(cmd)

# EOF
