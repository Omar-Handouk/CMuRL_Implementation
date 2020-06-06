import __future__

import random
import json
import gym
from gym import spaces
import numpy as np
import os
import random
import numpy
import subprocess

# state
states = [0, 1, 2, 3]  # Loss, Band up, Band down, stable

# Parameter
MAX_ALPHA = 1024
MIN_ALPHA = 1
PERC_ALPHA = 0.5

MAX_BETA = 1024
MIN_BETA = 1
PERC_BETA = 0.7

TCP_FRIENDLINESS = 1
FAST_CONVERGENCE = 1

# Hyper parameters
mean_interval = 5  # Used to average bandwidths over a period

delta_max = 0.5  # Maximum lost bandwidth MB/s
delta_min = 0.5  # Minimum gained bandwisth MB/s

base_reward = 0.1


def state_factor(state):
    if state == 0 or state == 2:
        return -1
    else:
        return 1


def scale_factor(state):
    if state == 0:
        return 5
    elif state == 1 or state == 2:
        return 2
    else:
        return 1


def reward_func(state, time_step):
    # Check if we are !time_step % 5, if True then check after loss if band gained
    return state_factor(state) * (base_reward ** (1 / (time_step * scale_factor(state))))

def bandwidth_mean
# https://thispointer.com/python-get-last-n-lines-of-a-text-file-like-tail-command/
def get_last_n_lines(file_name, N):
    list_of_lines = []
    with open(file_name, 'rb') as read_obj:
        read_obj.seek(0, os.SEEK_END)
        buffer = bytearray()
        pointer_location = read_obj.tell()

        while pointer_location >= 0:

            read_obj.seek(pointer_location)

            pointer_location = pointer_location - 1

            new_byte = read_obj.read(1)

            if new_byte == b'\n':

                list_of_lines.append(buffer.decode()[::-1])

                if len(list_of_lines) == N:
                    return list(reversed(list_of_lines))

                buffer = bytearray()
            else:

                buffer.extend(new_byte)

        if len(buffer) > 0:
            list_of_lines.append(buffer.decode()[::-1])

    return list(reversed(list_of_lines))


def intervalData(line):
    indices = [4, 6, 8, 9]

    tokenized_data = line.replace("   ", " ").replace("  ", " ").split(" ")

    data = []
    for i in indices:
        data.append(float(tokenized_data[i])) if i != 8 else data.append(int(tokenized_data[i]))

    return data


class CMuRLEnv(gym.Env):
    """Custom Environment that follows gym interface"""
    metadata = {'render.modes': ['human']}

    # Define reward range, observation space, & action space
    def __init__(self):
        super(CMuRLEnv, self).__init__()

        action_dictionary = {
            'TCP_FRIENDLINESS': spaces.Discrete(2),
            'FAST_CONVERGENCE': spaces.Discrete(2),
            'ALPHA': spaces.Box(low=0, high=1, shape=(1, 1)),
            'BETA': spaces.Box(low=0, high=1, shape=(1, 1))
        }

        self.action_space = spaces.Dict(action_dictionary)
        self.observation_space = spaces.Box(low=0, high=999, shape=(5, 4))  # 5 Logs, 4 Properties (see result.txt)

        self.time_step = 0  # Check bandwidth after 5 time_steps
        self. acc_rewards = 0

    def step(self, action):
        # return observation, reward, done, info
        # If after 5 rounds no increase in bandwidth
        observation = []
        reward = None
        done = None
        info = None

        self.time_step += 1

        iperf_data = get_last_n_lines('../iperf_results/results.txt', 6)
        del iperf_data[-1]  # Remove

        for entry in iperf_data:
            data = intervalData(entry)
            observation.append(data)

            if data[2] != 0:
                reward = reward_func(0, self.time_step)
            elif not(self.time_step % 2)

        return observation, reward, done, info

    def seed(self, seed=None):
        pass

    def reset(self):
        observation = None

        return observation

    def render(self, mode='human'):
        pass

    def close(self):
        pass
