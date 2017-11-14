from sweeppy import Sweep

import time
import picamera
import picamera.array
import numpy as np

with picamera.PiCamera(sensor_mode=2, resolution='2592x1952', framerate=8) as camera, Sweep('/dev/ttyUSB0') as sweep:

    # Camera Setup
    camera.resolution = (2592,1944)
    camera.framerate = 30 # higher frame rate reduces smearing in stills
    camera.start_preview()

    # let the camera warm up and set gain/white balance
    time.sleep(2)

    # Scanse Setup
    sweep.set_motor_speed(4)
    sweep.set_sample_rate(800)
    print('Motor Speed: ' + str(sweep.get_motor_speed()))
    print('Sample Speed: ' + str(sweep.get_sample_rate()))

    sweep.start_scanning()
    for scan in sweep.get_scans():
        scantime = int(time.time()*1000)
        print(scantime)
#debug
#        print('{}\n'.format(scan))
        with open('scans.txt','a') as f:
            for nn in range(0,len(scan.samples)):
                line = str(scantime) + "\t" + str(scan.samples[nn].angle) + "\t" + str(scan.samples[nn].distance) + "\t" + str(scan.samples[nn].signal_strength) + "\n"
#                print(line)
                f.write(line)

        camera.capture_sequence(['%d.jpg' % scantime],use_video_port=True)



