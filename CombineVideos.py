#Srinath Sibi for Ghost GhostDriver
#Combine Video Files in folder
# More than one file to combine
# GoPro files are broken down into  4 GB files as we keep recording. The numbers in a GOPRO file name indicate the order of...
# file creation. For example for files ['GP019354.MP4', 'GOPR9354.MP4', 'GP029354.MP4']...
# The first file ends with numbers 9354, then 019354 and 029354 and so on. So we combine the files starting with lowest..
# number in filename and then move to the maximum number in the filenames. For now , a simple sort() functio
import csv,argparse,sys,os,ffmpeg
import subprocess, re
from decimal import Decimal
import glob

os.chdir("L_Corner") # Remove this statemnt, since the files will be pasted in each folder.
try:
    filelist = glob.glob('*.MP4') # Searching for all files with MP4 extension
    print "List of MP4 files in the folder right now" , filelist, "  ", type(filelist[1])
except NameError:
    print "Error Encountered" # Make sure you are in the right folder if this error messsage pops output
    # It could also be lack of any MP4 files in the folder
if len(filelist) > 1:
    print "here we go!"
    filelist.sort()
    print filelist
else:
    print "Insufficent number of files in folder"
#ffmpeg -i "concat:GOPR9354.MP4|GP019354.MP4|GP029354.MP4" -c:a copy -c:v copy output.mp4
#ffmpeg is cauding weird errors. Output file is smaller than it should be and the above command needs to be run from bash => Not optimal
