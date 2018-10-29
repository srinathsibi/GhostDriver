#Srinath Sibi for Ghost GhostDriver ssibi@stanford.edu
#Combine Video Files in folder
# More than one file to combine
# GoPro files are broken down into  4 GB files as we keep recording. The numbers in a GOPRO file name indicate the order of...
# file creation. For example for files ['GP019354.MP4', 'GOPR9354.MP4', 'GP029354.MP4']...
# The first file ends with numbers 9354, then 019354 and 029354 and so on. So we combine the files starting with lowest..
# number in filename and then move to the maximum number in the filenames. For now , a simple sort() function

# Prereqs : This piece of code uses MoviePy library. To be able to use this, you need to install pip (python package manager),
#and then use pip to install moviepy . The instructions: http://zulko.github.io/moviepy/install.html
import csv,argparse,sys,os
import subprocess, re
from decimal import Decimal
import glob
from moviepy.editor import VideoFileClip, concatenate_videoclips

def concatenatefunction():
    try:
        filelist = glob.glob('*.MP4') # Searching for all files with MP4 extension
        print "List of MP4 files in the folder right now" , filelist, "  ", type(filelist[1])
    except IndexError:
        print "Error Encountered. There are either no MP4 files here or you are using this script in the wrong folder!" # Make sure you are in the right folder if this error messsage pops up.
        # It could also be lack of any MP4 files in the folder
    if len(filelist) > 1:
        print "Concatening Files : "
        filelist.sort()
        print filelist
    else:
        print "Insufficent number of files in folder"
    #Non - Iterative Clip Formation
    #clip1 = VideoFileClip(filelist[0]).subclip(0,5)
    #clip2 = VideoFileClip(filelist[1]).subclip(0,5)
    #clip3 = VideoFileClip(filelist[2]).subclip(0,5)
    #cliplist = [clip1,clip2,clip3]
    #Iterative clip formation
    cliplist = [ VideoFileClip(name) for name in filelist ]
    #Concatenation procedure
    final_clip = concatenate_videoclips([clip for clip in cliplist])
    final_clip.write_videofile("my_concatenation.mp4")

# We are going to ask for input on which folder to search for clips. We will maintain a list of all folders in the study folder and
#then make sure the folder is in the list and is not one of the CAN, QUAD, IMU, ClippedData folders
print "\n Hey Becky and Dylan! This script is meant to concatenate videos.\n", "\n", "This process is slow and tedious since the videos are large" ,\
" and the video stitching and encoding takes a long time even for a single file. Use this process only when the main quad is failing you."
study_folder = raw_input("\n Enter the name of the study folder which contains all the data \n")
print "\n Study folder received : ", study_folder
if os.path.exists('../'+study_folder+'/'):
    os.chdir('../'+study_folder+'/')
else:
    sys.exit("Folder doesn't exist! Please restart with correct name")
#Compiling a list of all folders in the study_folder
folderlist = list(list(os.walk('.'))[0][1])
print " Here are all the folders in the study_folder : ", folderlist
#Get name of folder needing video Concatenation
while True:
    foldername = raw_input("\nEnter the folder whose videos you would like to concatenate. (Enter 'Done' if you want to exit): \n")
    print "\nFolder name received : ", foldername, "\n"
    if (foldername in ['Done']):
        print "Done concatenating!"
        break
    elif (foldername in ['QUAD', 'IMU', 'CAN', 'ClippedData']) or (foldername not in folderlist):
        print "Enter a different folder name. Can't operate on this folder!"
        pass
    else:
        print "Concatenation function called."
        os.chdir(foldername + '/')#Entering Folder
        concatenatefunction()
        os.chdir('../')#Exiting folder
        pass
print "Concatenation Done! Bye!"
