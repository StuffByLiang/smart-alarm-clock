import sys
import time
import pyaudio
import numpy as np
import csv

from mpu6050 import mpu6050

MPU6050_ADDRESS = 0x68

FORMAT = pyaudio.paInt16
CHANNELS = 1
CHUNK = 1024*8
RATE = 44100

sensor = mpu6050(MPU6050_ADDRESS)

def main(argv):
    if len(argv) == 0:
        sys.exit("usage: sudo python3 sleepanalysis.py filename")
    
    filename = argv[0]

    file = open(filename + ".log", "a")

    # open audio stream
    p=pyaudio.PyAudio()
    stream=p.open(format=FORMAT,
                  channels=1,
                  rate=RATE,
                  input=True,
                  frames_per_buffer=CHUNK)

    # create file and write the header
    writer = csv.writer(file)
    writer.writerow(['time', 'sound', 'accel_x', 'accel_y', 'accel_z', 'gyro_x', 'gyro_y', 'gyro_z'])

    # collect data
    while True:
        accel_data = sensor.get_accel_data()
        gyro_data = sensor.get_gyro_data()
        sound_data = np.fromstring(stream.read(CHUNK, exception_on_overflow = False), dtype=np.int16)

        # calculate peak
        sound_peak=np.average(np.abs(sound_data))
        bars="#"*int(sound_peak)

        # print sound peak to console
        print("%s %05d %s"%(str(time.time()), sound_peak, bars))

        # write to logs
        writer.writerow([time.time(), sound_peak, accel_data['x'], accel_data['y'], accel_data['z'], gyro_data['x'], gyro_data['y'], gyro_data['z']])

    stream.stop_stream()
    stream.close()
    p.terminate()

if __name__ == "__main__":
   main(sys.argv[1:])