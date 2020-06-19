#!/usr/bin/env python
import __future__

import os
import sys
import time
import random
import signal
from subprocess import call

# Modes: 0 - No traffic rule set, 1 - Packet limit set to 1000 outstanding packet, 2 - Delay + Loss
# 3 - CORRUPTION + DUPLICATION

# This script is intended to use Linux tc and netem modules to simulate different conditions
#  that lead to network congestion

network_interface = None

if len(sys.argv) <= 1:
    file_path = os.path.dirname(__file__)
    file_name = os.path.join(file_path, './interface.txt')
    file = open(file_name, 'r')

    default_interface = file.read()

    print('No network interface selected, selecting interface from interface.txt:', default_interface)
    time.sleep(5)
    network_interface = default_interface

    file.close()
else:
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


def gen_scenario():
    number_of_rules = random.randint(0, 5)
    scenario = None

    if number_of_rules != 0:
        traffic_rules = construct_rules(number_of_rules)
        scenario = add_rule + ' ' + traffic_rules

    return scenario


def signal_handler(sig, frame):
    print('<<<<<<Training interrupted, reverting network interface to normal>>>>>>')
    call(delete_rule, shell=True)
    sys.exit(0)


def main():
    while True:
        interval = random.randint(0, len(intervals) - 1)
        generated_scenario = gen_scenario()

        if generated_scenario is None:
            pass
        else:
            call(generated_scenario, shell=True)
            print('Current rule:', generated_scenario)

        time.sleep(interval)

        if generated_scenario is not None:
            call(delete_rule, shell=True)


if __name__ == "__main__":
    print('---------------Loading random training scenarios---------------')
    call(delete_rule, shell=True)
    signal.signal(signal.SIGINT, signal_handler)
    main()
    print('---------------Random training scenarios complete---------------')
