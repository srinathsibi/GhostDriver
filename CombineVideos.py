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

# The line below is a way to change directory into a subfolder if needed.
#os.chdir("L_Corner") # Remove this statemnt, since the files will be pasted in each folder.

try:
    filelist = glob.glob('*.MP4') # Searching for all files with MP4 extension
    print "List of MP4 files in the folder right now" , filelist, "  ", type(filelist[1])
except IndexError:
    print "Error Encountered. There are either no MP4 files here or you are using this script in the wrong folder!" # Make sure you are in the right folder if this error messsage pops up.
    # It could also be lack of any MP4 files in the folder
if len(filelist) > 1:
    print "here we go!"
    filelist.sort()
    print filelist
else:
    print "Insufficent number of files in folder"
#ffmpeg -i "concat:GOPR9354.MP4|GP019354.MP4|GP029354.MP4" -c:a copy -c:v copy output.mp4
#ffmpeg is cauding weird errors. Output file is smaller than it should be and the above command needs to be run from bash => Not optimal

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

# Unfortunately, this piece of code cannot be iterated, so I am hoping that there are no more than 5 MP4 files in individual folders...
for i in range(len(filelist)):
    cliplist[i] = VideoFileClip(filelist[i])
