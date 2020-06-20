#!/usr/bin/env python
import __future__

import os
import sys
from scripts.random_train import gen_scenario

file_path = os.path.dirname(__file__)
file_name = os.path.join(file_path, './scenarios.txt')

file = open(file_name, 'w')

print('---------------Generating network scenarios---------------')

i = 12 if len(sys.argv) <= 1 else int(sys.argv[2])
n = 0
while n < i:
    scenario = gen_scenario()
    if scenario is None:
        continue
    else:
        file.write(scenario + ('\n' if n != 11 else ''))
        n += 1

file.close()

print('---------------Generating network scenarios completed---------------')
