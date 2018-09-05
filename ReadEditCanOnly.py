#This is the file to edit only the CAN data from GhostDriver
#Author: Srinath Sibi
#Users: Becky and Dylan


## imports for CSV file reading and interacting on the command line
import csv,argparse,sys,os

###########################################################################################################
############### Reading the CAN file ######################################################################
try:
	os.chdir("../GDData/20180816-1/CAN")	#Path for CAN data
	f = open('20180816-1_can.txt')	#Name of CAN data file
	csv_f = csv.reader(f)
except NameError:
	print "No such file exists!!!!"

try:
    os.chdir("../VIDEO/QUAD") # Navigate to the video folder for start time of clipped
    g = open("20180816-1_videoStart.txt") # Name of the start time file changed from the actual name to this format
    #Note that here it is assumed that the video file was started the last, hence its start time
    # and end time are the actual clip points for all data.
    csv_g = csv.reader(g)
except NameError:
        print "No such file exists!!!!"

#############################################################################################################
################ Reading start time from the video start file###############################################
for row in csv_g:
    array = [i.split(' ',4)[3] for i in row]
    print type(float(array[0]))," : ",float(array[0])
time_start = float(array[0])
print "Time Start : ", time_start




"""
############################################################################################################
############### Writing the time clipped files simultaneously###############################################

## Opening a new file to write data that is being read from the main CAN file
filename =  raw_input(' Please Enter the file name for the clipped CAN file ')
#time_start = raw_input(' Please enter the start time for clipping CAN data')
time_stop = raw_input(' Please enter the stop time for clipping CAN data')
# Outputting the parameters to confirm the input
print " Start time:",type(time_start)," ",time_start,"\n", "Stop Time: ",type(time_stop)," ",time_stop,"\n",	\
	" File Name: " , type(filename)," ",filename
out_file = open(filename, 'w')
with out_file:
	for row in csv_f:
		#print(row) # row is a list item. Including this line prints all the lines in the
		array = [i.split(' ',8)[1] for i in row]
		#print type(float(array[0]))," : ",float(array[0])
		#if float(array[0]) > 1532643404.314273:
		if float(array[0]) >= float(time_start) and float(array[0]) <= float(time_stop):
			writer = csv.writer(out_file)
			writer.writerows([row])

## Closing files after reading and writing
f.close()
out_file.close()
"""