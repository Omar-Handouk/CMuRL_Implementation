import __future__

import os
from scripts.random_train import gen_scenario

file_path = os.path.dirname(__file__)
file_name = os.path.join(file_path, './scenarios.txt')

file = open(file_name, 'w')

print('---------------Generating network scenarios---------------')

n = 0
while n < 12:
    scenario = gen_scenario()
    if scenario is None:
        continue
    else:
        file.write(scenario + ('\n' if n != 11 else ''))
        n += 1

file.close()

print('---------------Generating network scenarios completed---------------')