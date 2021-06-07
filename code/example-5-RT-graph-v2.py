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
from matplotlib.animation import FuncAnimation

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
def writefiledata(x, y):
    # open and create file
    file = open("tempdata.txt", "a")
    # write data
    time = str(x)
    value = str(round(y,3))
    file.write(time +"\t" + value)
    file.write("\n")
    # close file
    file.close()


# # constants
# k = 0
T_duration = 5 # seconds
sampling_freq = 10 # Hz
N_samples = T_duration*sampling_freq # sampling time in seconds
T_sampling = 1/sampling_freq # 10Hz
# data = []

# Tmax = 0.1; Tmin = -0.1
# y_range = [Tmin, Tmax] # graph range
# x_len = N_samples # number of points to display

# # create figure for plotting
# fig = plt.figure()
# ax = fig.add_subplot(1,1,1)
# xs = list(range(0,N_samples))
# ys = [0]*x_len
# ax.set_ylim(y_range)

# # create blank line
# line, = ax.plot(xs,ys)



device = nidaqmx.system.Device("Dev2")
channels = device.ai_physical_chans.channel_names
# print(channels)
# before starting task, reset device if not shotdown correctly
device.reset_device()



fig, ax = plt.subplots()
xdata, ydata = [], []
ln, = plt.plot([], [], '.-')
k = 0
xs = list(range(0,N_samples))
ys = [np.NaN]*N_samples

def init():
    # fig = plt.figure()
    # ax = fig.add_subplot(1,1,1)
    # configure plot
    plt.title('NI DAQmx Voltage')
    plt.xlabel('t [s]')
    plt.ylabel('U [V]')
    plt.grid()
    ax.set_xlim(0, N_samples)
    ax.set_ylim(-0.1, 0.1)
    ln.set_label(channels[0])
    ax.legend()
    # line.set_label('Label via method')
    return ln,

def update(i):
    global k, xs, ys
    k += 1 # iteration for sampling info
    rel_time = k*T_sampling
    # read daq
    value = readdaq(channels[0])
    print("U [V] =", round(value,3))
    # append new data to buffer
    ys.append(value)
    # and remove old data
    ys = ys[-N_samples:]
    # show data on graph
    ln.set_data(xs, ys)

    # log new arrived sample
    print(rel_time, value)
    writefiledata(rel_time, value)

    return ln,

ani = FuncAnimation(fig
                    ,update
                    # ,frames=5
                    ,init_func=init
                    # ,repeat=True
                    ,interval=1000 # update speed in ms
                    ,blit=True)
plt.show()
