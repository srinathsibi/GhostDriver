"""
convertCAN.py

Authors: Nik Martelaro (nikmart@stanford.edu)
         Jesus Mancilla (jesus@scrapworks.org)

Purpose: Convert the CAN data into a CSV that is readable by tools like
         ChronoViz and other data analysis software. Convert the UNIX timestamp
         to seconds since the start of the video

Requirements: Python 3

Usage: python convertCAM.py [can_data] [starttime]
[can_data]: csv file with the raw can data
[starttime]: UNIX timestamp from the start of the quad video

This file will create different CSV files for each data type. This is done
becasue each type of data is read at a diffrent time.
"""
import sys

## CONSTANTS
COMPTIME_IDX = 1
ID_IDX = 3

BRAKE_ID = 0x0224
BRAKE_DATA = 7
BRAKE_OFF = "00"
BRAKE_ON = "20"

SPEED_ID = 0x00B4
SPEED_DATA = 12

ACCEL_ID = 0x0245
ACCEL_DATA = 9

WHEEL_ID = 0x0025
WHEEL_ROTATION = 7
WHEEL_ANGLE = 8
angleValue = 360/255

can_data = sys.argv[1] # filename for CAN data
starttime = float(sys.argv[2]) # the UNIX start time of the video recording

speed_out = open('speed_out.csv','w') # write data to a converted output file
brake_out = open('brake_out.csv','w') # write data to a converted output file
accel_out = open('accel_pedal_out.csv','w') # write data to a converted output file
steering_wheel_out = open('steering_wheel_out.csv','w') # write data to a converted output file

speed_out.write('time,speed\n')
brake_out.write('time,brake\n')
accel_out.write('time,accel\n')
steering_wheel_out.write('time,angle\n')

# Load a data file as read only
with open(can_data, 'r') as f:
# run through each line and pick out the data we are interested in
# Timestamp: 1472338941.008668        ID: 01aa    000    DLC: 6    00 00 00 00 00 b1
    for line in f:
        data = line.strip().split() # strip out the whitespace

        data_time = float(data[COMPTIME_IDX]) - starttime
        if data_time > 0:
            canID = int(data[ID_IDX],16)

            # BRAKES
            if canID == BRAKE_ID:
                if data[BRAKE_DATA] == BRAKE_ON:
                    brake_out.write('{},{}\n'.format(data_time, 1))
                elif data[BRAKE_DATA] == BRAKE_OFF:
                    brake_out.write('{},{}\n'.format(data_time, 0))

            # SPEED
            if canID == SPEED_ID:
                hexSpeed = int("".join(data[SPEED_DATA:SPEED_DATA+2]), 16)
                speed = hexSpeed * 0.0062
                speed_out.write("{},{}\n".format(data_time, speed))

            # ACCELERATOR PEDAL PERCENTAGE
            if canID == ACCEL_ID:
                hexAccel = int("".join(data[ACCEL_DATA]), 16)
                accel_out.write("{},{}\n".format(data_time, hexAccel/2))

            # STEERING WHEEL ROTATION
            if canID == WHEEL_ID:
                rotationValue = int("".join(data[WHEEL_ROTATION]), 16)
                hexAngle = int("".join(data[WHEEL_ANGLE]), 16)
                if rotationValue == 15:
                    angle = 360 - (hexAngle * angleValue)
                elif rotationValue == 14:
                    angle = (360 - (hexAngle * angleValue)) + 360
                elif rotationValue == 0:
                    angle = -(hexAngle * angleValue)
                else:
                    angle = -(hexAngle * angleValue) -360
                steering_wheel_out.write("{},{}\n".format(data_time, angle))


brake_out.close()
speed_out.close()
accel_out.close()
steering_wheel_out.close()


print("Data time = {} minutes".format(round(data_time/60,2)))
if data_time/60 < 40:
    print("CAN data looks short...possibly not all there")
else:
    print("CAN data is longer than 40 mins, looks OK")

## References
# [1] Prius CAN Codes: https://www.vassfamily.net/ToyotaPrius/CAN/PriusCodes.xls
# [2] Prius CAN Codes: http://illmatics.com/car_hacking.pdf
