import tensorflow as tf
import tensornets as nets
import cv2
import numpy as np
from datetime import datetime
import pymysql
import io
import base64
from PIL import Image
#from firebase import firebase
#import json
#firebase = firebase.FirebaseApplication('https://object-detection-34ff9.firebaseio.com/', None)


#import time
con = pymysql.connect('localhost','root','','object_detection')
cur = con.cursor()

inputs = tf.placeholder(tf.float32, [None, 416, 416, 3]) 
model = nets.YOLOv3COCO(inputs, nets.Darknet19)

classes={'0':'Person_Count','1':'Bicycle_Count','2':'Car_Count','3':'Bike_Count','5':'Bus_Count','7':'Truck_Count'}
list_of_classes=[0,1,2,3,5,7]#to display other detected #objects,change the classes and list of classes to their respective #COCO indices available in their website. Here 0th index is for #people and 1 for bicycle and so on. If you want to detect all the #classes, add the indices to this list
try:
    with tf.Session() as sess:
        sess.run(model.pretrained())
        
        cap = cv2.VideoCapture("video/cam1.mp4")
        #change the path to your directory or to '0' for webcam
        while(cap.isOpened()):
            ret, frame = cap.read()
            img=cv2.resize(frame,(416,416))
            imge=np.array(img).reshape(-1,416,416,3)
            #start_time=time.time()
            preds = sess.run(model.preds, {inputs: model.preprocess(imge)})
            #print("--- %s seconds ---" % (time.time() - start_time)) #to time it
            boxes = model.get_boxes(preds, imge.shape[1:3])
            cv2.namedWindow('image',cv2.WINDOW_NORMAL)
            cv2.resizeWindow('image', 700,700)
            d = {}
            boxes1=np.array(boxes)
            for j in list_of_classes: #iterate over classes
                count =0
                if str(j) in classes:
                    lab=classes[str(j)]
                if len(boxes1) !=0:
            #iterate over detected vehicles
                    for i in range(len(boxes1[j])): 
                        box=boxes1[j][i] 
                        #setting confidence threshold as 40%
                        if boxes1[j][i][4]>=.40: 
                            count += 1    
                            cv2.rectangle(img,(box[0],box[1]),(box[2],box[3]),(0,255,0),3)
                            cv2.putText(img, lab, (box[0],box[1]), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 255), lineType=cv2.LINE_AA)
                print(lab,": ",count)
                d[lab] = count
            print("\n------------------------------------\n")
            keys = list(d.keys())
            value = list(d.values())
           
            now = datetime.now()
            date = now.strftime("%Y-%m-%d")
            time = now.strftime("%H:%M:%S")

            is_success, im_buf_arr = cv2.imencode(".png",img)
            byte_im = im_buf_arr.tobytes()
            read_image = io.BytesIO(byte_im)
            image = Image.open(read_image).convert("RGBA")
            image_name = str(date)+str(now.strftime("%H-%M-%S"))+".png"
            image.save(image_name)
            '''data = {
                'Date':date,
                'Time':time,
                'Person_Count':value[0],
                'Bicycle_Count':value[1],
                'Car_Count':value[2],
                'Bike_Count':value[3],
                'Bus_Count':value[4],
                'Truck_Count':value[5],
                'Frame':json.dumps(byte_im)
            }
            result = firebase.post('/Objects_Count/',data)
            print(result)'''
            print(date,time)
            query = "insert into Objects_Count(Date,Time,"+keys[0]+","+keys[1]+","+keys[2]+","+keys[3]+","+keys[4]+","+keys[5]+",Frame) values(%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            cur.execute(query,(date,time,str(value[0]),str(value[1]),str(value[2]),str(value[3]),str(value[4]),str(value[5]),image_name))
            con.commit()
            #Display the output      
            cv2.imshow("image",img)  
            if cv2.waitKey(1) & 0xFF == ord('q'):
                con.close()
                break
except KeyboardInterrupt:
    #cur.close()
    #con.close()
    print("Harshit")
    exit(0)