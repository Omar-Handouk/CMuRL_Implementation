import __future__
import subprocess
import os
import time
from env.CMuRLEnv import CMuRLEnv
# command = 'bash ./scripts/test.sh nigga'
# print(command.split())
# process = subprocess.Popen(command, shell=True)
# process.communicate()

print('asdasd' + ' alpha' + str(123))
# def get_last_n_lines(file_name, N):
#     list_of_lines = []
#     with open(file_name, 'rb') as read_obj:
#         read_obj.seek(0, os.SEEK_END)
#         buffer = bytearray()
#         pointer_location = read_obj.tell()
#
#         while pointer_location >= 0:
#
#             read_obj.seek(pointer_location)
#
#             pointer_location = pointer_location - 1
#
#             new_byte = read_obj.read(1)
#
#             if new_byte == b'\n':
#
#                 list_of_lines.append(buffer.decode()[::-1])
#
#                 if len(list_of_lines) == N:
#                     return list(reversed(list_of_lines))
#
#                 buffer = bytearray()
#             else:
#
#                 buffer.extend(new_byte)
#
#         if len(buffer) > 0:
#             list_of_lines.append(buffer.decode()[::-1])
#
#     return list(reversed(list_of_lines))
#
#
# def intervalData(line):
#     indices = [4, 6, 8, 9]
#
#     tokenized_data = line.replace("   ", " ").replace("  ", " ").split(" ")
#
#     data = []
#     for i in indices:
#         data.append(float(tokenized_data[i])) if i != 8 else data.append(int(tokenized_data[i]))
#
#     return data

env = CMuRLEnv()

action = env.action_space.sample()

env.step(action)