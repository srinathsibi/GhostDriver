# Author: Srinath Sibi
#Users: Becky Currano and Dylan Moore
#Purpose: Parse the CAN data to convert codes to actual values.
#Note: This code is based on Nik's convertCAN.py code which is also in the github repo.
# There is very little difference between this part and Nik's code. Unlike Nik's code, this code
# finds the CAN file since it was created during post processing and doesn't need user input.
# The crux of the code has been retained while the overall code has been changed to fit in with the remainder of the scripts.
import sys,os,glob,csv

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
foldername = raw_input("\nHey Dylan and Becky! Good job on clipping the data. Now please enter the folder name\n")
print "\nFolder name received : ", foldername, "\n"
os.chdir('../' + foldername + '/ClippedData/')# Changing search location to the requisite location of Clipped Data
#Opening the can file for reading and separation into relevant parts
try:
    canfile = glob.glob('clipped_can.txt')# filename for CAN data
    f = open(canfile[0] ,'r')#Opening CAN data file
    print "\nCAN file found :", canfile[0], "\n"
    csv_f = csv.reader(f)
except IndexError:
	print "No such file exists!!!!"
try:
    timestamps = glob.glob('TIMESTAMPS.txt')# filename for timestamps file written earlier in ClipCanAndIMU.py
    g = open(timestamps[0],'r')#opening timestamps file
    print "\nTimeStamps file found :", timestamps[0], "\n"
    csv_g = csv.reader(g)
except IndexError:
    print "No such file exists!!!!"
#Searcing for starttime in the file. Note that if no start time is printer, then the file is not able to get the start
for row in csv_g:
    if row[0].split(' ')[0].strip() == 'Start':
        starttime = float(row[0].split(' ')[1].strip())
print "Start time identified as: ", starttime
#Opening the separated file for writing
speed_out = open('speed_out.csv','w') # write data to a converted output file
brake_out = open('brake_out.csv','w') # write data to a converted output file
accel_out = open('accel_pedal_out.csv','w') # write data to a converted output file
steering_wheel_out = open('steering_wheel_out.csv','w') # write data to a converted output file
#Avoiding the next lines to make sure the clipping process is easier
#speed_out.write('time,speed\n')
#brake_out.write('time,brake\n')
#accel_out.write('time,accel\n')
#steering_wheel_out.write('time,angle\n')

# Load a data file as read only
with f:
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
