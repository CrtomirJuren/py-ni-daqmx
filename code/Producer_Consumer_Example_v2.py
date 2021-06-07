#########################################################################
# DAQmx Python - Producer/Consumer example
# Updated 10/19/2018
#
# Reads continuous samples from a single physical channel and writes
# them to a log file. Uses two parallel threads to perform
# DAQmx Read calls and data processing.
#
# Note: The number of samples per execution varies slightly since
# the task's start and stop times are specified in software.
#
# Input Type: Analog Voltage
# Dependencies: nidaqmx
#########################################################################

import nidaqmx
import time
import queue
import threading

# Constants
DEVICE_NAME = "Dev2"
PHYSICAL_CHANNEL = DEVICE_NAME+ "/ai0"   # Physical channel name from NI-MAX
SAMPLE_RATE = 100               # DAQ sample rate in samples/sec
ACQ_DURATION = 5               # DAQ task duration in sec

LOG_FILE_PATH = "log.txt"

# Reads any available samples from the DAQ buffer and places them on the queue.
# Runs for ACQ_DURATION seconds.
def producer_loop(q, task):
    start_time = time.time();
    while(time.time() - start_time < ACQ_DURATION):
        data = task.read(number_of_samples_per_channel=nidaqmx.constants.READ_ALL_AVAILABLE)
        # print(len(data))
        q.put_nowait(data)
    task.stop()
    return

# Takes samples from the queue and writes them to LOG_FILE_PATH.
def consumer_loop(q, task, file):
    while(True):
        try:
            temp = q.get(block=True, timeout=2)
        except:
            if (task.is_task_done()):
                return
        for val in temp:
            file.write("{}\n".format(val))
        time.sleep(0.5) # Simulate 0.5 seconds of extra processing per sample
        q.task_done()

# Main program
if __name__ == "__main__":

    device = nidaqmx.system.Device(DEVICE_NAME)
    channels = device.ai_physical_chans.channel_names
    # print(channels)
    # before starting task, reset device if not shotdown correctly
    device.reset_device()

    # Set up DAQ vars
    task = nidaqmx.task.Task()
    task.ai_channels.add_ai_voltage_chan(PHYSICAL_CHANNEL)
    task.timing.cfg_samp_clk_timing(rate=SAMPLE_RATE,
                                    sample_mode=nidaqmx.constants.AcquisitionType.CONTINUOUS)

    out_file = open(LOG_FILE_PATH,"w+")
    out_file.write("\n~~New Test Started~~\n")

    # Set up threading vars
    q = queue.Queue()
    prod = threading.Thread(target=producer_loop, args=(q, task))
    cons = threading.Thread(target=consumer_loop, args=(q, task, out_file))

    # Start acquisition and threads
    task.start()
    prod.start()
    cons.start()
    print("Task is running")

    while(not task.is_task_done()):
        pass # Spin parent thread until task is done
    print("Task is done")

    while(cons.isAlive()):
        pass # Wait for consumer to finish
    print("Consumer finished")

    # Clean up
    out_file.close()
    task.close()
    print("Done!")