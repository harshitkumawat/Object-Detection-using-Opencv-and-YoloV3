import time
from datetime import datetime
#import pymysql
import io,os
import numpy as np
#from datetime import datetime
#import pymysql
#from imgarray import save_array_img, load_array_img
#from os import fsync
import cv2
from PIL import Image


'''im = cv2.imread("a.jpg")
img = Image.fromarray(im, 'RGB')
print(type(img),img)
img.save('m.png')
img.show()
import base64
with open("m.png", "rb") as img_file:
    my_string = base64.b64encode(img_file.read())
print(my_string.decode('utf-8'))'''
i=0
now = datetime.now()
date = now.strftime("%Y-%m-%d")
timee = now.strftime("%H-%M-%S")
cap = cv2.VideoCapture("video/cam1.mp4")
while(cap.isOpened()):
	ret, frame = cap.read()
	is_success, im_buf_arr = cv2.imencode(".png", frame)
	byte_im = im_buf_arr.tobytes()
	print(type(byte_im))
	aa = io.BytesIO(byte_im)
	image = Image.open(aa).convert("RGBA")
	image.save(str(date)+str(timee)+".png")
	i+=1
	image.show()
	time.sleep(5)
#con = pymysql.connect('localhost','root','','object_detection')
#cur = con.cursor()

#now = datetime.now()
#print(now)
#date = now.strftime("%Y-%m-%d")
#time = now.strftime("%H:%M:%S")
#print(date,time)
'''lab = "Person_Count"
count = 3
d = {'a':1,'b':2,'c':3}
c = list(d.keys())
print(c)
a = str(1)
print(type(str(0)),type(a),c[0])'''
#query = "insert into Objects_Count(Date,Time,"+lab+") values(%s,%s,%s)"
#cur.execute(query,(date,time,count))
#con.commit()
#con.close()