#This is the file to edit only the CAN data from GhostDriver
#Author: Srinath Sibi @ ssibi@stanford.edu
#Users: Becky and Dylan


## imports for CSV file reading and interacting on the command line
import csv,argparse,sys,os
import subprocess, re, glob
from decimal import Decimal

# This function takes the relative path to the quad video file and then gets the length of the quad video
def get_video_length(path):
	process = subprocess.Popen(['/usr/bin/ffmpeg', '-i', path], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
	stdout, stderr = process.communicate()
	#print stdout
	for line in stdout.split(os.linesep):
		#print line , "\n", type(line), "\n"
		#print line.split(":")[0],"\n" , type(line.split(":")[0])
		output_label = line.split(":")[0]
		#print output_label
		if output_label.find('Duration')>=0: #trying to find the output string that has the
			duration = str(line.split(" ")[3])
			#print duration# Different split than above to get to the duration varibales
			time_values = duration.split(':')
			#print "Length of video is : ", (float(time_values[0])*3600 + float(time_values[1])*60 )
			video_length = (float(time_values[0])*3600 + float(time_values[1])*60)
			quad_video_length = video_length
	process.wait()
	return quad_video_length

#Function to parse the IMU data
def imuparser(imufilereader):
	global IMU_START_LINE
	#print "File reader received" , imufilereader
	for i, line in enumerate(imufilereader):
		if len(line)>1 and line[1] == 'IMU calibration complete! Ready for use.':
			IMU_START_LINE = i#In this loop, line number = i + 1
			break
	print "IMU start read at : " , IMU_START_LINE
	os.chdir('../ClippedData/')
	imuoutfile = open('Clipped_imu.txt','w')
	with imuoutfile:
		imuoutputwriter = csv.writer(imuoutfile)#opening file writer
		for i, line in enumerate(imufilereader):#Parsing the IMU file
			if i >= IMU_START_LINE:
				if float(line[0])>TIME_START and float(line[0])<TIME_STOP:
					imuoutputwriter.writerows([line])
					#print line , "\n\n"
	imuoutfile.close()
	print "\n\nSuccess!!!Clipped IMU file written!!!\n\n"

##################################Main Function#####################################
if __name__ == '__main__':
	###In main function
	global quad_video_length
	###Get User Input for Folder Name###
	foldername = raw_input("\nHey Dylan and Becky! Good job on collecting more study data. Please enter the name of the folder for which we will be analyzing the data\n")
	print "\nFolder name received : ", foldername, "\n"
	#############################################################################################################
	############# Opening the CAN file ##########################################################################
	try:
		os.chdir("../" + foldername +"/CAN")#Path for CAN folder
		canfile = glob.glob('*can.txt')#Searching for the CAN file in the folder with '*can.txt' in name
		f = open(canfile[0])	#Name of CAN data file
		print "\n \nCAN file found :", canfile, "\n\n"
		csv_f = csv.reader(f)
	except IndexError:
		print "No such file exists!!!!"
	#############################################################################################################
	############# Opening the quad video to determine start and end times ####################################
	try:
		os.chdir("../QUAD/") # Path for QUAD folder
		startfilename=glob.glob('*videoStart.txt') #Search for video start file with 'videoStart.txt' in name
		g = open(startfilename[0]) # Name of the start time file changed from the actual name to this format
    	#Note that here it is assumed that the video file was started the last, hence its start time
    	# and end time are the actual clip points for all data.
		print "Video Start file found :", startfilename, "\n\n"
		csv_g = csv.reader(g)
	except IndexError:
		print "No such file exists!!!!"
	#############################################################################################################
	################ Reading start time and end time from the video start file###################################
	for row in csv_g:
		array = [i.split(' ',4)[3] for i in row]
    	#print type(float(array[0]))," : ",float(array[0])
	TIME_START = float(array[0])
	print "Time Start : \n\n", TIME_START # Time at the CAN files need to be clipped.
	try:
		VIDEO_LENGTH = get_video_length(glob.glob('*quad.mov')[0])#Searching and returning the name of the quad movie
	except NameError or UnboundLocalError:
		print "There seems to be an error due to the mislabeling of folder names or the quad file is not present here. Unable to Proceed."
	print "Video Length : \n\n", VIDEO_LENGTH , "\n"
	TIME_STOP = TIME_START + VIDEO_LENGTH
	g.close()#Closing the reader for video start file
	#############################################################################################################
	################ Writing the output file for clipped CAN ####################################################
	os.chdir("../")#Creating a new folder for the Clipped CAN and IMU dat
	CLIPPEDFOLDERPATH = "ClippedData/"
	if not os.path.exists(CLIPPEDFOLDERPATH):
		os.makedirs(CLIPPEDFOLDERPATH)
	OUTPUTFILENAME = 'clipped_can.txt'
	os.chdir("ClippedData")
	outfile = open(OUTPUTFILENAME,'w')
	#Begin Writing here
	with outfile:
		outputwriter = csv.writer(outfile)
		outputwriter.writerows([row] for row in csv_f if ((float((row[0].strip().split(" ")[1]).split(':')[0]) > TIME_START) and (float((row[0].strip().split(" ")[1]).split(':')[0]) < TIME_STOP)))
		#the humongous line above iteratively clips the data as between start and end points.
	outfile.close()
	f.close()
	print "Success!!! CAN file clipped and written in the ClippedData folder!!! \n"
	###############################################################################################################
	# Searching and opening IMU file ######## Doing this here to avoid problems in Path resolution for os.chdir####
	try:
		os.chdir("../IMU/") #Path for IMU folders
		imufile = glob.glob('*imu.csv')# Search for IMU data with ending 'imu.csv' in name
		h = open(imufile[0])
		print "IMU file located ", imufile , "\n\n"
		csv_h = csv.reader(h)
	except IndexError:
		print "No IMU file here"
	imuparser(csv_h)#Function to read and write the IMU file
	h.close()
	# Printing name of files in the ClippedData Folder to double check
	print "\n\nFiles in Current Working Directory:", os.listdir(os.curdir)
	timestampfile = open('TIMESTAMPS.txt','w')
	with timestampfile:
		timestampwriter = csv.writer(timestampfile)
		timestampwriter.writerow(['Start '+ str(TIME_START)])
		timestampwriter.writerow(['Stop ' + str(TIME_STOP)])
		timestampwriter.writerow(['Length ' + str(VIDEO_LENGTH)])
	timestampfile.close()
	print "\n\nTime stamp file written, Use this file for further analysis if needed\n\n"
	print "\n\n ############ End of Clipping Process ################## \n\n"
### End of the File, Code beneath is retained for reference purposes only
"""
	#############################################################################################################
	################ Reading from the CAN file and wriing into a clipped file####################################
#	for row in csv_f:
#		#print "Timestamp: ", row[0].strip().split(" ")[1], "length: ", len(row[0].strip().split(" ")[1]);
#		timestamp = float((row[0].strip().split(" ")[1]).split(':')[0]); # TimeStamp for each writerows
#		print timestamp

############################################################################################################
############### Writing the time clipped files simultaneously###############################################

## Opening a new file to write data that is being read from the main CAN file
filename =  raw_input(' Please Enter the file name for the clipped CAN file ')
#TIME_START = raw_input(' Please enter the start time for clipping CAN data')
time_stop = raw_input(' Please enter the stop time for clipping CAN data')
# Outputting the parameters to confirm the input
print " Start time:",type(TIME_START)," ",TIME_START,"\n", "Stop Time: ",type(time_stop)," ",time_stop,"\n",	\
	" File Name: " , type(filename)," ",filename
out_file = open(filename, 'w')
with out_file:
	for row in csv_f:
		#print(row) # row is a list item. Including this line prints all the lines in the
		array = [i.split(' ',8)[1] for i in row]
		#print type(float(array[0]))," : ",float(array[0])
		#if float(array[0]) > 1532643404.314273:
		if float(array[0]) >= float(TIME_START) and float(array[0]) <= float(time_stop):
			writer = csv.writer(out_file)
			writer.writerows([row])

## Closing files after reading and writing
f.close()
out_file.close()
"""
