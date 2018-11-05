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
import csv,argparse,sys,os,shutil
import subprocess, re, glob
from decimal import Decimal
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
StartTimeList = []#List of all start times
StopTimeList = []#List of all stop times
infoline =[]#List of all information lines. Beware: It is a list of lists
headerrow = []# Header row read once to store in info file for all short clips
#Starting funciton to read clip ClipTimings
def ReadClipTImings():
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
    #print "\n", StartTimeList, "\n\n" , StopTimeList , "\n\n", infoline
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
    os.chdir('../')
def ClipIMUdata():
    print '\nNow Clipping the IMU Data!!!\n'
#Starting main function
if __name__ == '__main__':
    #Open the clip timins information in the ClipTimings
    foldername = raw_input("\nHey Dylan and Becky! Please enter the name of the folder for which we will be creating the short clips.\n")
    print "\nFolder name received : ", foldername, "\n"
    try:
        os.chdir('../'+foldername+'/')
    except OSError:#use OSError instead
        print "\nThe folder name does not exist, please start again."
    ReadClipTImings()
    CreateFoldersForShortClips()
    ClippingQuadVideo()
    ClipIMUdata()
