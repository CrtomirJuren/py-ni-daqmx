# -*- coding: utf-8 -*-
"""
Created on Mon Jun  7 10:54:38 2021

https://github.com/ni/nidaqmx-python

@author: crtjur
"""
import nidaqmx
import time
import numpy as np
import matplotlib.pyplot as plt

def file_write(t, value):
    time = str(t)
    value = str(round(value,3))
    file.write(time +"\t" + value)
    file.write("\n")

T_duration = 5 # seconds
sampling_freq = 2 # Hz
N_samples = T_duration*sampling_freq # sampling time in seconds
T_sampling = 1/sampling_freq # 10Hz
data_buffer = []

# create task
task = nidaqmx.Task()
device = nidaqmx.system.Device("Dev2")
print(device.ai_physical_chans.channel_names)
# before starting task, reset device if not shotdown correctly
device.reset_device()

# config task
task.ai_channels.add_ai_voltage_chan("Dev2/ai0","U", min_val=-10, max_val=10)
# start task
task.start()

# open and create file
file = open("tempdata.txt", "w")

# read
for sample in range(N_samples):
    time_rel = sample*T_sampling
    # read value
    value = task.read()
    # add to buffer
    data_buffer.append(value)
    print("U [V] =", round(value,3))
    # log to file
    file_write(time_rel, value)
    # wait
    time.sleep(T_sampling)

# close file
file.close()
# stop task
task.stop()
# destroy task
task.close()

# plotting

t = np.arange(0, T_duration, T_sampling)
plt.plot(t, data_buffer, "-o")
plt.title('NI DAQmx Voltage')
plt.xlabel('t [s]')
plt.ylabel('U [V]')
plt.grid()
plt.show()