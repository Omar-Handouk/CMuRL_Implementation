import __future__

import os
import sys
import time
from subprocess import call

file_dir = os.path.dirname(__file__)
file_name = os.path.join(file_dir, './scenarios.txt')
scenarios = open(file_name, 'r')

if len(sys.argv) <= 1:
    print('Network interface need to be defined')
    print('Available interfaces:')
    call('ifconfig', shell=True)
    sys.exit(1)

network_interface = sys.argv[1]

for scene in scenarios:
    call(scene, shell=True)
    time.sleep(10)
    call('echo \'CMurl@dmin213!\' | sudo -S tc qdisc delete dev ' + network_interface + ' root', shell=True)