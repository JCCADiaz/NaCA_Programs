# -*- coding: utf-8 -*-
"""
Created on Tue Jan 30 15:16:47 2024

@author: jccad
"""

##############
## Script listens to serial port and writes contents into a file
##############
## requires pySerial to be installed 

import serial
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
import time
from drawnow import *

from tkinter import (LabelFrame, Entry, Button, Toplevel, Label)


def top_arduino_measure():
    top = Toplevel()
    top.title("Temperature measurement with Arduino")
    top.geometry("385x255+330+60")
    ###############################
    
    DataArray=[]
    TimeArray=[]
    def Figure():
        plt.plot(TimeArray,DataArray,'bo-')
        plt.grid(True)
        plt.grid(linestyle='dotted',linewidth=0.5)
        plt.xlabel('time (s)')
        plt.ylabel('Temperature (°C)')
    
    def connect_and_measure(port = 'COM8'):
        serial_port = port;
        baud_rate = 9600; #In arduino, Serial.begin(baud_rate)
        
        ser = serial.Serial()
        ser.baudrate = baud_rate
        ser.port = port
        ser.open()
        
        #### Parameters 
        ## Change depending on the measure conditions
        write_to_file_path = name_box.get()+".txt";
        total_t = int(total_t_box.get()) # total time in seconds
        step_t = int(step_t_box.get()) # time step in seconds
        ###############
        
        delta_global = 0
        start_t = datetime.now()
        print(start_t.time())
        
        
        plt.ion() 
    
        while delta_global <= total_t:
            while (ser.inWaiting()==0):   #wait here until there is data
                pass                              #do nothing
            
            output_file = open(write_to_file_path, "a");
            tempdata = ser.readline()
            tempdata=tempdata.decode()   #convert the byte string to a unicode string
            data=float(tempdata)              #converting unicode string to float(decimal)
            
            t_now = datetime.now()
        
            # get difference
            delta_t = t_now - start_t
            delta_global = delta_t.total_seconds()
            
            output_file.write(str(delta_t.total_seconds())+'\t'+str(data)+'\n')
            output_file.close()
            
            print('t:',str(delta_t.total_seconds()), 's ::: T:', str(data), '°C') 

            ###### refresh plot
            
            DataArray.append(data)
            TimeArray.append(delta_global)
            
            drawnow(Figure)
            plt.pause(0.00001)
            plt.show()
            

            #df = pd.read_csv(write_to_file_path, sep="\t", names = ['time(s)','Temperature(°C)'])
            # plt.plot(df['time(s)'], df['Temperature(°C)'])
            # plt.draw()
            # plt.pause(0.0001)
            # plt.clf()
            # #time.sleep(step_t)
            
        end_t = datetime.now()
        print(end_t.time())    
        output_file = open(write_to_file_path, "a");
        output_file.write('\n'+'t_0'+'\t'+str(start_t.time())+'\n')
        output_file.write('t_f'+'\t'+str(end_t.time()))
        output_file.close()
            
        ser.close()
        

        
        # df = pd.read_csv(write_to_file_path, sep="\t", names = ['time(s)','Temperature(°C)'])
        
        # plt.plot(df['time(s)'], df['Temperature(°C)'],label='Furnace Temperature')
        # plt.legend()
        # plt.show()
    
    ##############################
    # Between frame Parameters
    frame_parameters = LabelFrame(top, text="time parameters", padx=5, pady=5)#padx and pady inside of the frame
    # in frame text="..." is optional
    
    frame_parameters.grid(row=0, column=0, padx=10, pady=5, sticky="nsew")#padx and pady outside of the frame
    
    #total_t box 
    total_t_label= Label(frame_parameters, text="Total time in seconds",width=18)
    total_t_label.grid(row=0, column=0, pady=5, columnspan=1)
    
    total_t_box = Entry(frame_parameters, width=18, font=("", 12))
    total_t_box.insert(0, "3600")
    total_t_box.grid(row=1, column=0, pady=5, padx=5, ipady=3)
    
    #step_t box 
    step_t_label= Label(frame_parameters, text="Step time in seconds",width=18)
    step_t_label.grid(row=0, column=1, pady=5, columnspan=1)
    
    step_t_box = Entry(frame_parameters, width=18, font=("", 12))
    step_t_box.insert(0, "2")
    step_t_box.grid(row=1, column=1, pady=5, padx=5, ipady=3)
    ###############################
    
    ##############################
    # Between frame file name
    frame_file_name = LabelFrame(top, text="Insert a file name to save the data", padx=5, pady=5)#padx and pady inside of the frame
    # in frame text="..." is optional
    
    frame_file_name.grid(row=1, column=0, padx=10, pady=5, sticky="nsew")#padx and pady outside of the frame
    
    #name_  label box 
    name_label= Label(frame_file_name, text="File Name",width=16)
    name_label.grid(row=0, column=0, pady=5, columnspan=1)
    
    name_box = Entry(frame_file_name, width=28, font=("", 11))
    name_box.insert(0, "Type a name for your file")
    name_box.grid(row=0, column=1, pady=5, padx=5, ipady=3)
    ###############################
    
    ###############################
    # Between frame start measure
    frame_start_measure = LabelFrame(top, text="", padx=5, pady=5)#padx and pady inside of the frame
    
    frame_start_measure.grid(row=2, column=0, padx=10, pady=5, sticky="nsew")#padx and pady outside of the frame
    
    #start_measure: button 
    start_button = Button(frame_start_measure, text="Start measure",
                          font=("", 12), background="#E8E8E8", width=36, 
                          command=lambda: connect_and_measure(port = 'COM8'))
    start_button.grid(row=0, column=1, rowspan=4, sticky="nsew", pady=5, padx=5)
    ###############################