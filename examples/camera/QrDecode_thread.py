# -*- coding: utf-8 -*-
"""
Created on Fri Dec  2 13:26:50 2022

@author: frank.kubler
"""

import barcodeQrSDK
import numpy as np
import cv2
import json
import threading 
import os

my_mutex = threading.Lock()
g_results = None


 
class print_thread(threading.Thread): # manipulation du résultat du scan
      
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        global my_mutex
        last_results=''
        while True:
            os.system('cls')
            my_mutex.acquire()     
                      
                  
            if g_results !=None:
                for result in g_results[0]:
                    if last_results != result.text:
                        print('resultat = ',result.text)
                        last_results=result.text
            else:
                last_results=''
                print('vide')
            ch = cv2.waitKey(1)
            if ch == 27:
                break    
    
class QrDecode(threading.Thread):
    
    def __init__(self):
        threading.Thread.__init__(self)


    def run(self):
        # set license
      
        global my_mutex
        
        barcodeQrSDK.initLicense("DLS2eyJoYW5kc2hha2VDb2RlIjoiMjAwMDAxLTE2NDk4Mjk3OTI2MzUiLCJvcmdhbml6YXRpb25JRCI6IjIwMDAwMSIsInNlc3Npb25QYXNzd29yZCI6IndTcGR6Vm05WDJrcEQ5YUoifQ==")
    
        # initialize barcode scanner
        scanner = barcodeQrSDK.createInstance()
        params = scanner.getParameters()
    
        
    
    
        # register callback function to native thread
        scanner.addAsyncListener(QrDecode.callback)
    
        cap = cv2.VideoCapture(1,cv2.CAP_DSHOW)
        
        while True:
            ret, image = cap.read()
            if image is not None:
                scanner.decodeMatAsync(image)
                
            if g_results != None:
                # print('Elapsed time: ' + str(g_results[1]) + 'ms')
                cv2.putText(image, 'Elapsed time: ' + str(g_results[1]) + 'ms', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                for result in g_results[0]:
                    x1 = result.x1
                    y1 = result.y1
                    x2 = result.x2
                    y2 = result.y2
                    x3 = result.x3
                    y3 = result.y3
                    x4 = result.x4
                    y4 = result.y4
                    
                    cv2.drawContours(image, [np.int0([(x1, y1), (x2, y2), (x3, y3), (x4, y4)])], 0, (0, 255, 0), 2)
                    cv2.putText(image, result.text, (x1, y1), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    
            cv2.imshow('Barcode QR Code Scanner', image)
            ch = cv2.waitKey(1)
            if ch == 27:
                break
        cv2.destroyWindow('Barcode QR Code Scanner')
        scanner.clearAsyncListener()
      
        
        
    
    def callback(results, elapsed_time):
        global g_results
               
        g_results = (results, elapsed_time)
        my_mutex.release()

        

if __name__ == '__main__':
    
    my_mutex.acquire()
    m=print_thread()
    m.start()
    
    m1=QrDecode()
    m1.start()
    
    
    m.join()
    m1.join()
     
    
    
 
    