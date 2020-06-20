import __future__

import gym
from stable_baselines.common.vec_env import VecCheckNan
from stable_baselines.common import make_vec_env
from stable_baselines import PPO2

env = make_vec_env('CMuRL_Env:CMuRL-Env-v0')
env = VecCheckNan(env, raise_exception=True)

model = PPO2.load('CMuRL_Model_v3')

obs = env.reset()
while True:
    action, _states = model.predict(obs)
    obs, rewards, _, _ = env.step(action)
    env.render()
