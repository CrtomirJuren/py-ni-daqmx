# -*- coding: utf-8 -*-
"""
Low speed DAQ example
Created on Mon Jun  7 10:54:38 2021

https://github.com/ni/nidaqmx-python

@author: crtjur
"""
import nidaqmx
import time
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

def readdaq(channel):
    # create task
    task = nidaqmx.Task()
    # config task
    # task.ai_channels.add_ai_voltage_chan("Dev2/ai0","U", min_val=-10, max_val=10)
    task.ai_channels.add_ai_voltage_chan(channel,"U", min_val=-10, max_val=10)
    # start task
    task.start()
    # read data
    value = task.read()
    # stop task
    task.stop()
    # destroy task
    task.close()
    return value

# save data function
def writefiledata(t, x):
    # open and create file
    file = open("tempdata.txt", "w")
    # write data
    time = str(t)
    value = str(round(x,3))
    file.write(time +"\t" + value)
    file.write("\n")

    # close file
    file.close()

def logging(i, ys):
    global k
    k += 1
    current_time = k*T_sampling
    # read value
    value = readdaq(channels[0])
    print("U [V] =", round(value,3))
    # add to buffer
    data.append(value)
    # wait
    time.sleep(T_sampling)

    # log to file
    writefiledata(current_time, value)

    # plotting
    ys.append(value)
    # limit y list to set number of items
    ys = ys[-x_len:]
    line.set_data(ys)
    # print(ys)
    return line,


# constants
k = 0
T_duration = 5 # seconds
sampling_freq = 1 # Hz
N_samples = T_duration*sampling_freq # sampling time in seconds
T_sampling = 1/sampling_freq # 10Hz
data = []

Tmax = 0.1; Tmin = -0.1
y_range = [Tmin, Tmax] # graph range
x_len = N_samples # number of points to display

# create figure for plotting
fig = plt.figure()
ax = fig.add_subplot(1,1,1)
xs = list(range(0,N_samples))
ys = [0]*x_len
ax.set_ylim(y_range)

# create blank line
line, = ax.plot(xs,ys)

# configure plot
plt.title('NI DAQmx Voltage')
plt.xlabel('t [s]')
plt.ylabel('U [V]')
plt.grid()

# start DAQ
device = nidaqmx.system.Device("Dev2")
channels = device.ai_physical_chans.channel_names
# print(channels)
# before starting task, reset device if not shotdown correctly
device.reset_device()

# print(readdaq(channels[0]))
ani = animation.FuncAnimation(fig,
                              logging,
                              fargs=(ys,),
                              interval = 100,
                              blit = True)
plt.show()
