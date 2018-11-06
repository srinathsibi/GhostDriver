#Author : Srinath Sibi (ssibi@stanford.edu)
#Users : Becky Currano and Dylan Moore
#Purpose : To clip quad video, imu, can data streams into small pieces based on
#timings in the csv files made by Dylan and Becky. The end goal is to make individual
#folders in clipped data folder based and then store clipped data in them.
#Steps : Order of clipping Data :
#1. Read the clip timing files. Extract all times from it and store it in two arrays
#2. Open the quad video and clip it using MoviePy
#3. Clip the IMU data.
#4. Clip the CAN data streams.
#5. Store the other information from the same row as aux info in the same sub folder
#5.1 The column are hardcoded in. So any change in the order or the number of the columns needs rework
import csv,argparse,sys,os,shutil
import subprocess, re, glob
from decimal import Decimal
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
StartTimeList = []#List of all start times, Sixth Column
StopTimeList = []#List of all stop times, Seventh Column
infoline = []#List of all information lines. Beware: It is a list of lists
headerrow = []# Header row read once to store in info file for all short clips
#Starting funciton to read clip ClipTimings
def ReadClipInfo():
    global StartTimeList
    global StopTimeList
    global infoline
    global headerrow
    try:
        os.chdir('ClipTimings/')
    except OSError:#use OSError instead
        print "\nThe folder name does not exist, please start again."
    print "In ClipTimings Folder"
    cliptimingfile = open(glob.glob('*Clip timing*')[0])#Locating the csv file using phrase in name
    #print "\nClip Timings File found :\n",cliptimingfile
    cliptimingreader = csv.reader(cliptimingfile)
    #we are going to do one read operation to get the first line of headers
    headerrow = next(cliptimingreader)
    print "\n Header row: \n", headerrow
    for row in cliptimingreader:
        try:
            #print "\nClip Start Time: ", Converttimetoseconds(row[5]) , "\nClip Stop Time: ", Converttimetoseconds(row[6])
            StartTimeList.append(Converttimetoseconds(row[5]))
            StopTimeList.append(Converttimetoseconds(row[6]))
            infoline.append(row)
        except ValueError:
            print "Empty cell in Start and Stop Time. Try to clear lines with no data to avoid conflict in processing!"
    print "\n", StartTimeList, "\n\n" , StopTimeList , "\n\n", infoline
    os.chdir('../')#SWITCHING TO TOP LEVEL STUDY FOLDER
#Function to convert time in mm:ss to seconds.
def Converttimetoseconds(timeinminandsec):
    minutes = float(timeinminandsec.split(':')[0])
    seconds = float(timeinminandsec.split(':')[1])
    timeinseconds = minutes*60 + seconds
    return timeinseconds
#Function to create Folders for Short Clips in the Clipped Data Folder
def CreateFoldersForShortClips():
    print " Creating folders for each start and stop point defined in the StartTimeList"
    os.chdir('ClippedData/')#Moved in to the ClippedDataFolder
    for i in range(len(StartTimeList)):
        subfoldername = 'Clip_'+str(i)
        if not os.path.exists(subfoldername):
            os.makedirs(subfoldername)
    print "\n\nSubfolders created.\n"#os.listdir('.') is you need to view all the subfolders in the ClippedData Folder
    os.chdir('../')
#Function to load and create clips in the subfolders from start and stop times
def ClippingQuadVideo():
    print "This function is meant to load and create clips in the subfolders from start and stop times."
    os.chdir('QUAD/')#In the QUAD folder
    #Now we need to iterate between each clip_* folder.
    for i in range(len(StartTimeList)):
        ffmpeg_extract_subclip(glob.glob('*quad.mov')[0], StartTimeList[i],StopTimeList[i], targetname=('Clip'+str(i)+'.mov'))
        shutil.move( 'Clip'+str(i)+'.mov' , '../ClippedData/Clip_'+str(i)+'/Clip'+str(i)+'.mp4')
    print '\nClipped Video Files created and moved to the respective folders!!!\n\n'
    os.chdir('../')#Now in the top level folder again
#Function to clip IMU data into pieces and store into subfolders
def ClipIMUdata():
    print '\nNow Clipping the IMU Data!!!\n'
    os.chdir('ClippedData/')#Now in the ClippedData folder
    imufile = open(glob.glob('*imu.txt')[0] ,'r')
    imufilereader = csv.reader(imufile)
    firstrow = next(imufilereader)
    #print "\n\nFirst timestamp of IMU file is: ", float(firstrow[0]),'\n\n'
    imustarttime = float(firstrow[0])# Reading start time of the imu file so that we can add to the clip timings for clipping data
    imufile.seek(0)
    for i in range(len(StartTimeList)):
        os.chdir('Clip_' + str(i) + '/')#Inside clip_* folder
        imuclip = open('IMUClip'+str(i)+'.txt','w')
        imuclipwriter = csv.writer(imuclip)
        for row in imufilereader:
            if float(row[0]) >= ( imustarttime + StartTimeList[i] ) and float(row[0]) <= ( imustarttime + StopTimeList[i] ):
                #print 'timestamp for printing' , row[0]
                imuclipwriter.writerows([row])
        imuclip.close()
        imufile.seek(0)#Reset the file read position to the start of the imufile for every time we create a new imu clip file.
        os.chdir('../')#In clipped data folder
    os.chdir('../')#Moving back to Study Folder
    #print "Current Folder contents:\n\n", os.listdir('.')#This line is to make sure that we are in the right folder
def ClipSplitCANData():
    print "\n\nNow clipping the different streams of CAN data\n\n"
    os.chdir('ClippedData/')
    try:
        accelfile = open(glob.glob('*accel_pedal*')[0] ,'r')
        accelreader = csv.reader(accelfile)
        brakefile = open(glob.glob('*brake*')[0] ,'r')
        brakereader = csv.reader(brakefile)
        speedfile = open(glob.glob('*speed*')[0] ,'r')
        speedreader = csv.reader(speedfile)
        steeringfile = open(glob.glob('*steering*')[0] ,'r')
        steeringreader = csv.reader(steeringfile)
    except:
        print "Error in opening the separated CAN files!"
    for i in range(len(StartTimeList)):
        os.chdir('Clip_' + str(i) + '/')#Inside clip_* folder
        accelclipout = open('AccelClip'+str(i)+'.txt','w')
        accelclipwriter = csv.writer(accelclipout)
        brakeclipout = open('BrakeClip'+str(i)+'.txt','w')
        brakeclipwriter = csv.writer(brakeclipout)
        speedclipout = open('SpeedClip'+str(i)+'.txt','w')
        speedclipwriter = csv.writer(speedclipout)
        steeringclipout = open('SteeringClip'+str(i)+'.txt','w')
        steeringclipwriter = csv.writer(steeringclipout)
        #Writing acceleration file
        for row in accelreader:
            if float(row[0])>=StartTimeList[i] and float(row[0])<=StopTimeList[i]:
                accelclipwriter.writerows([row])
        accelclipout.close()
        accelfile.seek(0)# Reset to top of the accelfilereader
        #Writing braking file
        for row in brakereader:
            if float(row[0])>=StartTimeList[i] and float(row[0])<=StopTimeList[i]:
                brakeclipwriter.writerows([row])
        brakeclipout.close()
        brakefile.seek(0)# Reset to the top of the brakefilereader
        #Writing speed file
        for row in speedreader:
            if float(row[0])>=StartTimeList[i] and float(row[0])<=StopTimeList[i]:
                speedclipwriter.writerows([row])
        speedclipout.close()
        speedfile.seek(0)# Reset to the top of the speedfile
        #Writing the steering file
        for row in steeringreader:
            if float(row[0])>=StartTimeList[i] and float(row[0])<=StopTimeList[i]:
                steeringclipwriter.writerows([row])
        steeringclipout.close()
        steeringfile.seek(0)#Reset to the top of the steeringfile
        os.chdir('../')#Out of the Clip_i folder
    os.chdir('../')#moving back to the Study Folder
    #print "Current Folder contents:\n\n", os.listdir('.')#This line is to make sure that we are in the right folder
#Writing the Info line in each clip folder
def WriteClipInfoLine():
    print "\n\nWriting Infoline in each clip folder\n\n"
    os.chdir('ClippedData/')
    for i in range(len(StartTimeList)):
        os.chdir('Clip_' + str(i) + '/')#Inside clip_* folder
        infofile = open('Info'+str(i)+'.txt','w')
        infowriter = csv.writer(infofile)
        infowriter.writerow(headerrow)#Header Row for each info file
        infowriter.writerow(infoline[i])#Info line as entered by Becky and Dylan
        os.chdir('../')
    os.chdir('../')#Moving back to the study folder
    #print "\n\nCurrent Folder contents:\n\n", os.listdir('.')#This line is to make sure that we are in the right folder
#Starting main function
if __name__ == '__main__':
    #Open the clip timins information in the ClipTimings
    foldername = raw_input("\nHey Dylan and Becky! Please enter the name of the folder for which we will be creating the short clips.\n")
    print "\nFolder name received : ", foldername, "\n"
    try:
        os.chdir('../'+foldername+'/')
    except OSError:#use OSError instead
        print "\nThe folder name does not exist, please start again."
    ReadClipInfo()
    CreateFoldersForShortClips()
    ClippingQuadVideo()
    ClipIMUdata()
    ClipSplitCANData()
    WriteClipInfoLine()
