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

T_duration = 2 # seconds
sampling_freq = 5 # Hz
N_samples = T_duration*sampling_freq # sampling time in seconds
T_sampling = 1/sampling_freq # 10Hz
data_buffer = []

# create task
task = nidaqmx.Task()

# config task
task.ai_channels.add_ai_voltage_chan("Dev2/ai0","U", min_val=-10, max_val=10)
# start task
task.start()

# read
for sample in range(N_samples):
    value = task.read()
    data_buffer.append(value)
    print("U [V] =", round(value,3))
    time.sleep(T_sampling)

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