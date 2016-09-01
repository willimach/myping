import io
import os
import picamera
import time
from datetime import datetime
from PIL import Image
from time import sleep

camera = picamera.PiCamera()
camera.rotation = 0
# sets black/white pictures
camera.color_effects= (128,128)  

difference = 20
pixels = 10

pic_width = 2592
pic_height = 1944
vid_width = 1024
vid_height = 768
vid_length=5

def compare():
   camera.resolution = (100, 75)
   stream = io.BytesIO()
   camera.capture(stream, format = 'bmp') 
   stream.seek(0)
   im = Image.open(stream)
   buffer = im.load()
   stream.close()
   return im, buffer

def newimage(pic_width, pic_height,changedpixels):
   mytime = datetime.now()
   filename = "motion-%04d%02d%02d-%02d%02d%02d-%04d.jpg" % (mytime.year, mytime.month, mytime.day, mytime.hour, mytime.minute, mytime.second,changedpixels)
   filenamevid = "motion-%04d%02d%02d-%02d%02d%02d.h264" % (mytime.year, mytime.month, mytime.day, mytime.hour, mytime.minute, mytime.second)
   camera.resolution = (pic_width, pic_height)
   camera.capture(filename)
   camera.resolution = (vid_width,vid_height)
#   camera.start_recording(filenamevid)
#   time.sleep(vid_length)
#   camera.stop_recording()
   print "Captured %s" % filename

image1, buffer1 = compare()

timestamp = time.time()

while (True):

   image2, buffer2 = compare()

   changedpixels = 0
   for x in xrange(0, 100):
      for y in xrange(0, 75):
         pixdiff = abs(buffer1[x,y][1] - buffer2[x,y][1])
         if pixdiff > difference:
            changedpixels += 1
   print changedpixels
   if changedpixels > pixels:
      timestamp = time.time()
      newimage(pic_width, pic_height,changedpixels)

   image1 = image2
   buffer1 = buffer2
