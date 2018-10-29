Author : Srinath Sibi (ssibi@stanford.edu)

Users: Becky Currano and Dylan Moore

Experiment: Ghost Driver

Purpose: To clip and analyze the Ghost driver IMU and CAN data. Combine Go-Pro videos to create single larger file.

NOTE: Please read the warning before employing the code.

Warning: The code ClipCANandIMU.py sometimes might fail if the working directory is not exactly as preplanned. If you encounter any difficulties, please contact me.

Warning: The code is meant to create a new folder for Clipped data called 'ClippedData'. This folder willcontain the clipped IMU and CAN data.

Warning: This code assumes that the Quad video is the shortest ( time-wise ) data stream of all the streams of data gathered. That is to say that IMU and CAN data were started before and ended after the Quad video.

Warning: To run this code, certain python packages need to be installed first. The python package is MoviePy. To do this, pip (python package manager) needs to be installed. Please contact me for this process if you are unsure on how to proceed.

To install pip : https://www.makeuseof.com/tag/install-pip-for-python/

To install MoviePy : http://zulko.github.io/moviepy/install.html

If there are other errors due to missing packages, please contact me.

The codes for analyzing the data are dependent on the folder structure since they naviagate between folder to folder to get the data for cliiping. The recommended folder structure is shown below. The repo is cloned into a folder in the same directory level as the study data folder. Make sure to organize all the study data this way.

![FileStructure](/FolderStructureGD.jpg)

Please ensure that the folder name does not contain any '-', '/', or other special characters. The only special characters allowed are '_'. Other characters cause issues when entering the name through user input.
