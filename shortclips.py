#Author : Srinath Sibi (ssibi@stanford.edu)
#Users : Becky Currano and Dylan Moore
#Purpose : To clip quad video, imu, can data streams into small pieces based on
#timings in the csv files made by Dylan and Becky. The end goal is to make individual
#folders in clipped data folder based and then store clipped data in them.
#Steps : Order of clipping Data :
#1. Read the clip timing files. Extract all times from it
#2. Open the quad video and clip it using MoviePy
#3. Clip the IMU data.
#4. Clip the CAN data streams.
#5. Store the other information from the same row as aux info in the same sub folder
import csv,argparse,sys,os
import subprocess, re, glob
from decimal import Decimal
