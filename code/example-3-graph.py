# -*- coding: utf-8 -*-
"""
Created on Mon Jun  7 10:54:38 2021

https://github.com/ni/nidaqmx-python

@author: crtjur
"""
import nidaqmx
import time
import numpy as np


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

# read
for sample in range(N_samples):
    # read value
    value = task.read()
    # add to buffer
    data_buffer.append(value)
    print("U [V] =", round(value,3))
    # wait
    time.sleep(T_sampling)

# stop task
task.stop()
# destroy task
task.close()



# create time data
t = np.arrange(0, T_duration, T_sampling)

# plotting
plt.plot(t, data_buffer, "-o")
plt.title('NI DAQmx Voltage')
plt.xlabel('t [s]')
plt.ylabel('U [V]')
plt.grid()
plt.show()