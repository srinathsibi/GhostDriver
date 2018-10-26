#This is the file to edit CAN data from GhostDriver
#Author: Srinath Sibi
#Users: Becky and Dylan


## imports for CSV file reading and interacting on the command line
import csv,argparse,sys,os

###########################################################################################################
############### Reading the CAN file ######################################################################
try:
	os.chdir("../GDData/CAN")	#Path for CAN data
	f = open('20180726-1_can.txt')	#Name of CAN data file
	csv_f = csv.reader(f)
except NameError:
	print "No such file exists!!!!"

## Opening a new file to write data that is being read from the main CAN file
filename =  raw_input(' Please Enter the file name for the clipped CAN file ')
time_start = raw_input(' Please enter the start time for clipping CAN data')
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


############################################################################################################
################# Reading the IMU file ############################################################################################################
try:
	os.chdir("../../GDData/IMU")	#Path for CAN data
	f = open('imuLog_1532371925.csv')	#Name of CAN data file
	csv_f = csv.reader(f)
except NameError:
	print "No such file exists!!!!"
## Opening a new file to write data that is being read from the main CAN file
filename =  raw_input(' Please Enter the file name for the clipped IMU file ')
time_start = raw_input(' Please enter the start time for clipping IMU data')
time_stop = raw_input(' Please enter the stop time for clipping IMU data')
out_file = open(filename, 'w')
with out_file:
	for row in csv_f:
		#print(row)		
		array = [i.split(',',2)[0] for i in row]
		if float(array[0]) >= float(time_start) and float(array[0]) <= float(time_stop):
			#print type(float(array[0]))," : ",float(array[0])		
			writer = csv.writer(out_file)
			writer.writerows([row])
## Closing files after reading and writing
f.close()
out_file.close()


############################################################################################################
################### Reading and editing video files ##################################################
#######################################################################################################

