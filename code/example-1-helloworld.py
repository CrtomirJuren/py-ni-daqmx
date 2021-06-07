# -*- coding: utf-8 -*-
"""
Created on Mon Jun  7 10:54:38 2021

https://github.com/ni/nidaqmx-python

@author: crtjur
"""
import nidaqmx
# Dev2

# create task
task = nidaqmx.Task()

# config task
task.ai_channels.add_ai_voltage_chan("Dev2/ai0","U", min_val=-10, max_val=10)

# start task
task.start()

# read
value = task.read()
print(round(value,3))

# stop task
task.stop()

# destroy task
task.close()