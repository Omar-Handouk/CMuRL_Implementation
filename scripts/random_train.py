import __future__

import sys
import time
import random
from subprocess import call

# Modes: 0 - No traffic rule set, 1 - Packet limit set to 1000 outstanding packet, 2 - Delay + Loss
# 3 - CORRUPTION + DUPLICATION

# This script is intended to use Linux tc and netem modules to simulate different conditions
#  that lead to network congestion

if len(sys.argv) <= 1:
    print('Network interface need to be defined')
    print('Available interfaces:')
    call('ifconfig', shell=True)
    sys.exit(1)

network_interface = sys.argv[1]
authorization = "echo 'CMurl@dmin213!' | sudo -S "
add_rule = authorization + 'tc qdisc add dev ' + network_interface + ' root netem'
delete_rule = authorization + 'tc qdisc delete dev ' + network_interface + ' root'

intervals = [5, 10, 20, 40, 60]
commands = ['limit', 'delay', 'loss', 'corrupt', 'duplicate']


def construct_rules(n_rules):
    taken = []  # List of taken commands

    t_rules = ''
    first = True

    while n_rules != 0:
        rule = random.randint(0, len(commands) - 1)  # Choose a random rule
        if rule in taken:  # If rule is already taken, retry
            continue

        value = None
        rule_string = None
        if rule == 0:  # Limit rule
            value = random.randint(1000, 5000)
            rule_string = '{} {}'.format('limit', str(value))
        elif rule == 1:
            value = random.randint(50, 150)
            variation = random.randint(10, 15)
            rule_string = '{} {}ms {}ms'.format('delay', str(value), str(variation))
        else:
            value = random.uniform(10, 35)
            rule_string = '{} '.format(commands[rule]) + str('{0:.3g}'.format(value)) + '%'

        t_rules += ('' if first else ' ') + rule_string

        # Check if first rule, append taken rule, decrease rules
        if first:
            first = False
        taken.append(rule)
        n_rules -= 1

    return t_rules


while True:
    interval = random.randint(0, len(intervals) - 1)
    number_of_rules = random.randint(0, 5)

    if number_of_rules == 0:
        pass
    else:
        traffic_rules = construct_rules(number_of_rules)
        net_rule = add_rule + ' ' + traffic_rules
        call(net_rule, shell=True)

    time.sleep(intervals[interval])

    # Clear traffic rules
    if number_of_rules != 0:
        call(delete_rule, shell=True)
