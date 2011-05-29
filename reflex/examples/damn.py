''' Example program
    Created by photofroggy.
    
    This uses both Reflex and dAmnViper.
'''

# Reflex imports
from reflex.data import Event
from reflex.control import EventManager
from reflex.interfaces import Reactor
# dAmnViper imports
from dAmnViper.base import ReconnectingClient

''' Create a basic client class that manages the
    connection to dAmn, reactors, and events.
    
    This means the class has a lot to do, in theory,
    but dAmnViper and Reflex should make it all easy!
'''

class MyClient(ReconnectingClient):
    
    def __inst__(self, un, pw, admin, trigger, autojoin, events):
        # Store everything.
        self.events_ = events
        self.reactors = []
        # Stuff to do with the client
        self.user.username = un
        self.user.password = pw
        self._admin = admin
        self._trigger = trigger
        self.autojoin = autojoin
        # Make sure the parent gets its fair share.
        ReconnectingClient.__inst__(self)
        # Load reactors!
        self.load_reactors()
        # Tell the reactors we are ready.
        self.events_.trigger(Event('ready'), self)
    
    def load_reactors(self):
        # We only really have one reactor for this example.
        self.reactors.append(example(self.events_, self))
    
    def pkt_generic(self, data):
        self.events_.trigger(Event(data['event'], data['rules']), self)
    
''' Create a basic reactor!
    This is just a simple example of what can be done!
'''

class example(Reactor):
    
    def init(self, dAmn):
        # Store these for easy reference!
        self.badmin = dAmn._admin
        self.btrig = dAmn._trigger
        
        # This binding is needed here so we can have commands!
        self.bind(self.check_command, 'recv_msg')
        
        # Use the command event name to hook commands.
        self.bind(self.c_about, 'command', ['about'])
        self.bind(self.c_quit, 'command', ['quit', self.badmin])
    
    def check_command(self, event, dAmn):
        # Check if the message starts with the trigger!
        if event.message[:len(self.btrig)] != self.btrig:
            return
        # Manipulate event data!
        msg = event.message[len(self.btrig):]
        args = msg.split(' ')
        # Create an event object!
        cmd = Event('command',
            [('cmd', args[0]),
                ('user', event.user),
                ('ns', event.ns),
                ('message', msg),
                ('args', args),
                ('raw', event.raw)])
        # Trigger the event!
        self.trigger(cmd, dAmn)
    
    # Below are our command handlers!
    
    def c_about(self, cmd, dAmn):
        dAmn.say(cmd.ns, '{0}: Reflex bot by photofroggy.'.format(cmd.user))
    
    def c_quit(self, cmd, dAmn):
        dAmn.say(cmd.ns, '{0}: Closing down!'.format(cmd.user))
        dAmn.flag.quitting = True
        dAmn.disconnect()
    
if __name__ == '__main__':
    # So yeah, create an event manager.
    events = EventManager()
    # How about a client?
    dAmn = MyClient('username', 'password', 'admin', '!',
        ['chat:Botdom'], events)
    # Start the client! This will connect it to dAmn!
    # dAmn Viper essentially runs its own main loop.
    dAmn.start()
        

# EOF
