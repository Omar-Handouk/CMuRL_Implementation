import __future__

import os
import sys
import time
import signal
from subprocess import call

print('---------------Loading Fixed scenario---------------')

file_dir = os.path.dirname(__file__)
scenarios = open(os.path.join(file_dir, '../scenarios.txt'), 'r')

interface = open(os.path.join(file_dir, './interface.txt'), 'r')
network_interface = interface.read()
interface.close()


def signal_handler(sig, frame):
    print('<<<<<<Training interrupted, reverting network interface to normal>>>>>>')
    call('echo \'CMurl@dmin213!\' | sudo -S tc qdisc delete dev ' + network_interface + ' root', shell=True)
    sys.exit(0)


signal.signal(signal.SIGINT, signal_handler)
call('echo \'CMurl@dmin213!\' | sudo -S tc qdisc delete dev ' + network_interface + ' root', shell=True)

for scene in scenarios:
    print('Current rule:', scene)
    call(scene, shell=True)
    time.sleep(10)
    call('echo \'CMurl@dmin213!\' | sudo -S tc qdisc delete dev ' + network_interface + ' root', shell=True)

scenarios.close()

print('---------------Fixed scenario complete---------------')