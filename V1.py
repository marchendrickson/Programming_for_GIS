#Authors: Marc Hendrickson, Bart Bauer, Nathaniel Geis
#Final Assignment for Programming for GIS
#May 2018

#import packages-------------------------------------------------------------------------

import arcpy              #check out the arcpy package
from arcpy import env	  #this is so we can use the environment package
from arcpy.sa import*	  #This checks out the Spatial Analyst package in Arc
import time				   #So we can time how long the process takes
import os				   #This will import the os package check it out: http://www.pythonforbeginners.com/os/pythons-os-module

#https://community.esri.com/thread/118848 - example script that may help
#https://stackoverflow.com/questions/31346790/unzip-all-zipped-files-in-a-folder-to-that-same-folder-using-python-2-7-5/31355555 - this is a tutorial on how to use python to unzip all folders 

# Start the timer for the entire process and set up directory---------------------------
start_time = datetime.datetime.now()
print start_time
print ('--------------------------------------------------------')

arcpy.env.workspace = "..\Final_Proj"
temp_workspace = "..\Final_Proj"
arcpy.env.overwriteOutput = True			# Overwrite is turned ON for this script
IMGList = arcpy.ListRasters()				#The ListRasters function will get all of the images in the folder you have
GDB = temp_workspace + "/basemap.gdb"

#Some print statements to tell you how long this will take
print "01. Starting the Process to Mosaic."
print "Number of images to be Mosaicked:" + str(len(IMGList))  #This argument takes the number of images in your folder and makes it a string to appear in the Python Prompt

if str(len(IMGList)) < "6":				#This will determine the number of rasters in your folder and return either statement
    print ("This should not take that long")
else:
    print ("This is probably going to take a long time. Go get a coffee and walk around.")

#Iterate through the rasters and make them into 32 bit floating point if they are not already
for raster in IMGList:
	pixelType = str(arcpy.GetRasterProperties_management(raster, "VALUETYPE"))
	
	if pixelType == "6":
		print "You do not need to convert any of your rasters"
	else:
		arcpy.CopyRaster_management(raster, raster, "", "", "", "", "", "16_BIT_UNSIGNED")
'''
#This step will mosaic the images you have in your directory-----------------------------

arcpy.MosaicToNewRaster_management(IMGList, temp_workspace, "IMG_Mosaic.tif",  pixel_type="32_BIT_FLOAT", cellsize="", number_of_bands="1", mosaic_method="", mosaic_colormap_mode="MATCH")

print "Mosaic All Done"


# Now lets use the times tool to put the DEM into feet if its not already

print "Now we are changing the DEM from Meters to Feet"
arcpy.CheckOutExtension("3D")     #This will check out the 3d-Analyst extension so that we can run the times tool
arcpy.Times_3d("IMG_Mosaic.tif", "0.3048", "..\Final_Proj\IMG_Times")   #This is how to convert the DEM which comes in meters to feet


# Now lets make a hillshade out of the DEM
#We are going to try to make a swiss hillshade
Divide_By= "5"    #This is the amount that we will divide the original dem by in order to combine it and make something cool
DEM_div_5 = "Divide_DEM"   #This is going to be the DEM we create when we divide by 5
Default_Hillshade = "HillSha_1"   #This is creating a variable for our Hillshade we are about to create
arcpy.CheckOutExtension("Spatial")  #Check out the Spatial Analyst Tools

arcpy.gp.Divide_sa("..\Final_Proj\IMG_Times", Divide_By, DEM_div_5) #This is giving us the Original DEM divided by a factor of 5
print "DEM Division Done"

arcpy.gp.Hillshade_sa("..\Final_Proj\IMG_Times", Default_Hillshade, "315", "45", "NO_SHADOWS", ".00001") #This is where we create our hillshade
print "Hillshade Done!"

FocalStatistics(Default_Hillshade, NbrRectangle(4,4, "CELL"), "MEDIAN", "DATA")  #This uses the Focal Statistics Tool and uses a moving 4x4 window to calculate the Median value and fill that in to a new raster
print "Focal Statistics Done"

arcpy.gp.Plus_sa(DEM_div_5, Default_Hillshade, "aerial_persp") #We are creating an Aerial Perspective Raster that looks like a lighter hillshade
print "Aerial Perspective Done"

#Now lets make contours

Contour("..\Final_Proj\IMG_Times", "..\Final_Proj\contour.shp", 20) #Making contours on the 20 foot mark
Contour("..\Final_Proj\IMG_Times", "..\Final_Proj\contour100.shp", 100) #Making contours on the 100 foot mark
print "Contours are made!!"

#Create final GDB if needed-----------------------------------------------------------------------

if not arcpy.Exists(GDB): 
	arcpy.CreateFileGDB_management(temp_workspace, "basemap.gdb")

print "Geodatabase is made!"


catalog = arcpy.CreateRasterCatalog_management( GDB, "raster")



#Import Rasters and Shapefile into GDB
arcpy.WorkspaceToRasterCatalog_managment("..\Final_Proj", "..\Final_Proj\basemap.gdb\raster")

#Now lets apply a color scheme to the DEM 

#Finally lets export all as TIFF's so that we can mess with them in Adobe Photoshop


# end time and report it
'''
print ('------------------------------------------')
print "Script finished processing at:"
print datetime.datetime.now()
print ('-------')
print "Script total runtime:"
print datetime.datetime.now() - start_time

