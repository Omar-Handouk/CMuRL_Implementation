import __future__

import gym
from stable_baselines.common.vec_env import VecCheckNan
from stable_baselines.common.policies import MlpPolicy
from stable_baselines.common import make_vec_env
from stable_baselines import PPO2

env = make_vec_env('CMuRL_Env:CMuRL-Env-v0', n_envs=1)
env = VecCheckNan(env, raise_exception=True)

model = PPO2(MlpPolicy, env, verbose=1)
model.learn(total_timesteps=100000)

model.save('CMuRL_Model_v6')
