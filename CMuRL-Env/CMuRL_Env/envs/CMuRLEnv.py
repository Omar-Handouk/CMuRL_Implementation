import os
import subprocess

import gym
import numpy as np
from gym import spaces

# We have four states: Packet loss, Bandwidth gained, Bandwidth loss, Stable
states = [0, 1, 2, 3]

# Hyper-parameters
MEAN_INTERVAL = 5  # Interval for averaging bandwidth
LAMBDA = 1.5  # Base reward
RETRIES_THRESH = 0.35  # Threshold for retries
DELTA_MAX = 0.7  # Maximum bandwidth lost, percentage compared to last bandwidth
DELTA_MIN = 0.3  # Minimum bandwidth gained, percentage compared to last bandwidth

# Base-values
# Alpha: Multiplicative increase factor to increase CWNDmax, CWNDmax = CWNDmax * alpha
MAX_ALPHA = 1024
MIN_ALPHA = 1

# Beta: Multiplicative decrease factor to decrease CWNDmax
# (TCP CUBIC: https://www.cs.princeton.edu/courses/archive/fall16/cos561/papers/Cubic08.pdf)
MAX_BETA = 1024
MIN_BETA = 1

# Base parameters
PERC_ALPHA = 0.5
PERC_BETA = 0.7
TCP_FRIENDLINESS = 1.0
FAST_CONVERGENCE = 1.0


class CMuRLEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self):
        super(CMuRLEnv, self).__init__()

        self.dir = os.path.dirname(__file__)
        self.net_logs = os.path.join(self.dir, '../../../iperf_results/results.txt')

        # Initialize environment variables
        self.time_step = 0
        self.accumulated_rewards = 0
        self.average_bandwidth = None
        self.perc_alpha = PERC_ALPHA
        self.perc_beta = PERC_BETA
        self.tcp_friendliness = TCP_FRIENDLINESS
        self.fast_convergence = FAST_CONVERGENCE
        self.state = None
        self.retries = None

        # Call TCPTuner initial values
        self.call_tcptuner()

        # Initialize observation space and action space
        # Observation spaces: 5 logs from iperf3.
        # Properties Transmitted bytes, Bandwidth, Retries, Congestion Window size (All in KBytes)
        self.observation_space = spaces.Box(low=0, high=175000, shape=(5, 4), dtype=np.float64)
        # Actions that map to environment variables
        self.action_space = spaces.Box(low=np.array([0, 0, 0, 0]), high=np.array([1, 1, 1, 1]), dtype=np.float64)

    def call_tcptuner(self):
        if self.time_step % 1000:
            return None
        base_command = "echo 'CMurl@dmin213!' | sudo -S /bin/bash " + \
                       str(os.path.join(self.dir, '../../../scripts/manage_cc.sh '))

        alpha = base_command + 'alpha ' + str(max(min(int(round(MAX_ALPHA * self.perc_alpha)), MAX_ALPHA), MIN_ALPHA))
        beta = base_command + 'beta ' + str(max(min(int(round(MAX_BETA * self.perc_beta)), MAX_BETA), MIN_ALPHA))
        tcp_friendliness = base_command + 'tcp_friendliness ' + str(int(round(self.tcp_friendliness)))
        fast_convergence = base_command + 'fast_convergence ' + str(int(round(self.fast_convergence)))

        commands = [alpha, beta, tcp_friendliness, fast_convergence]

        for command in commands:
            (subprocess.Popen(command, shell=True)).communicate()

    def step(self, action):
        observation = get_observation(self.dir, self.net_logs, 5)
        reward = None
        done = False
        info = {}
        state = -1

        self.time_step += 1

        for log in observation:
            # If number of retries is not zero, self.retries is not None,
            # and retires is greater than retries_thresh of self.retires
            if (log[2] != 0) and (self.retries is not None) and \
                    (self.retries + self.retries * RETRIES_THRESH < log[2]):
                state = states[0]
                reward = calculate_reward(state, self.time_step)
            self.retries = log[2]

        calculated_avg = average_bandwidth(observation)

        if not (self.time_step % MEAN_INTERVAL) and state == -1:  # If 5 transmissions passed and no state is set
            # Check if we have no average bandwidth set

            if self.average_bandwidth is None:  # Double check if is not None
                pass
            else:
                # That means if our average increase by DELTA_MIN% we have a substantial increase in bandwidth
                if self.average_bandwidth + self.average_bandwidth * DELTA_MIN <= calculated_avg:
                    state = states[1]
                # Average is increase by DELTA_MAX%, substantial decrease in bandwidth
                elif self.average_bandwidth - self.average_bandwidth * DELTA_MAX > calculated_avg:
                    state = states[2]

                # If bandwidth changed, calculate reward
                if state != -1:
                    reward = calculate_reward(state, self.time_step)

        self.average_bandwidth = calculated_avg

        if state == -1:
            state = states[3]
            reward = calculate_reward(state, self.time_step)

        self.state = state

        # Update Accumulated rewards, perc_alpha, perc_beta, tcp_friendliness & fast_convergence
        self.accumulated_rewards += reward
        self.perc_alpha = action[0]
        self.perc_beta = action[1]
        self.tcp_friendliness = action[2]
        self.fast_convergence = action[3]
        # Call TCPTuner with new updated parameters
        self.call_tcptuner()

        return np.array(observation), reward, done, info

    def render(self, mode='human'):
        print('---------------Time step:', self.time_step, '---------------')
        print('Accumulated rewards:', self.accumulated_rewards)
        print('Alpha:', str(min(int(round(MAX_ALPHA * self.perc_alpha)), MAX_ALPHA)))
        print('Beta:', str(min(int(round(MAX_BETA * self.perc_beta)), MAX_BETA)))
        print('TCP_Friendliness:', str(int(round(self.tcp_friendliness))))
        print('Fast_Convergence:', str(int(round(self.fast_convergence))))
        print('State:', str(self.state))
        print('Retries:', str(self.retries))
        print('---------------------------------------------------------------')

    def reset(self):
        # Reset environment variables
        self.time_step = 0
        self.accumulated_rewards = 0
        self.average_bandwidth = None
        self.perc_alpha = PERC_ALPHA
        self.perc_beta = PERC_BETA
        self.tcp_friendliness = TCP_FRIENDLINESS
        self.fast_convergence = FAST_CONVERGENCE
        self.state = None
        self.retries = None

        # Call TCPTuner initial values
        self.call_tcptuner()

        return np.array(get_observation(self.dir, self.net_logs, 5))


# --------------------------------------------------------------------------------------------------------------------
# Helper methods, non-class specific
# Reward Function
def calculate_reward(state, time_step):
    return state_factor(state) * (LAMBDA ** (1 / (time_step * scale_factor(state))))


def state_factor(state):
    return -1 if state == 0 or state == 2 else 1


def scale_factor(state):
    if state == 0:  # Packet loss
        return 5
    elif state == 3:  # Stable state
        return 1
    else:  # Bandwidth gain/loss
        return 2


def average_bandwidth(observation):
    total_bandwidth = 0.

    for log in observation:
        total_bandwidth += log[1]

    return total_bandwidth / MEAN_INTERVAL


def network_logs(file, n):
    lines = []

    with open(file, 'rb') as read_obj:
        read_obj.seek(0, os.SEEK_END)
        buffer = bytearray()
        pointer = read_obj.tell()

        while 0 <= pointer:
            read_obj.seek(pointer)
            pointer -= 1

            new_byte = read_obj.read(1)

            if new_byte == b'\n':
                lines.append(buffer.decode()[::-1])

                if len(lines) == n:
                    return list(reversed(lines))

                buffer = bytearray()
            else:
                buffer.extend(new_byte)

        if len(buffer) > 0:
            lines.append(buffer.decode()[::-1])

    return list(reversed(lines))


def extract_stats(line):
    # Indices 4 = Transmitted Bytes, 6 = Bandwidth, 8 = Retries & 9 = Congestion Window
    indices = [4, 6, 8, 9]

    tokenized_data = line.replace('   ', ' ').replace('  ', ' ').split(' ')
    data = []

    for i in indices:
        number = float(tokenized_data[i])
        # If transmitted bytes are in MB, convert to KB
        if i == 4 and tokenized_data[i + 1] == 'MBytes':
            number *= 1000
        data.append(number)

    return data


def get_observation(logs_dir, logs_relative_path, n):
    observation = []

    file_path = os.path.join(logs_dir, logs_relative_path)
    net_logs = network_logs(file_path, n + 1)
    del net_logs[-1]

    for log in net_logs:
        stats = extract_stats(log)
        observation.append(stats)

    return observation
