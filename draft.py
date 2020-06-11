import __future__

import gym
from env.CMuRLEnv import CMuRLEnv

env = CMuRLEnv()

action = env.action_space.sample()

env.step(action)