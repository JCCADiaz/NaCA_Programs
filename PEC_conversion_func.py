# -*- coding: utf-8 -*-
"""
Created on Thu Jan 25 13:32:49 2024

@author: jccad
"""
from tkinter import (LabelFrame, Entry, Button, Toplevel, Label, END, Checkbutton, BooleanVar)

from tkinter.filedialog import (askopenfilename, askdirectory)
import pandas as pd
import math
import os
import matplotlib.pyplot as plt

def top_PEC_conv():
    top = Toplevel()
    top.title("Linear Sweep Voltammetry_Tool")
    top.geometry("360x330+330+60")
    
    ###############################
    def open_file():
        if var_one.get()== False and var_several.get()==False:
            print('Choose one option!')
        if var_one.get()== True and var_several.get()==True:
            print('Choose only one option!')
            var_one.set(False)
            var_several.set(False)  
        if var_one.get()== True and var_several.get()==False:
            open_file_name = askopenfilename()
            select_box.delete(0,"end")
            select_box.insert(0, open_file_name)
        if var_one.get()== False and var_several.get()==True:
            open_folder_name = askdirectory()
            select_box.delete(0,"end")
            select_box.insert(0, open_folder_name) 
    ###############################

    ###############################
    def from_PEC_convert(path):
        ph = float(pH_box.get())
        Area = float(Area_box.get())
        data = pd.read_excel(path, usecols=["Potential applied (V)", "WE(1).Current (A)"])
        data["Potential(V_Vs_RHE)"] = data["Potential applied (V)"]+(0.059*ph)+0.1976
        data['Current_density(mA/cm^2)'] = (data["WE(1).Current (A)"]*1000)/Area
        data = data.rename(columns={"WE(1).Current (A)": "Current(A)"})
        return data
    
    def subPath():
    	#global sub_path
        if select_box.get()[-5:]==".xlsx":
            sub_path = select_box.get()[:-5]
        else:
            sub_path = select_box.get()
        return sub_path
    
    def file_to_Save():
        if var_one.get()== True and var_several.get()==False:
            path = select_box.get()
            return from_PEC_convert(path)
        else:
            data_txt = [file for file in os.listdir(select_box.get()) if file[-4:]=='XLSX' or file[-4:]=='xlsx']  
            data_dic = {}
            for file in data_txt:
                path = select_box.get()+'/'+file
                data_dic[file] = from_PEC_convert(path)
            return data_dic
    
    def save_Data1():
        sub_path = subPath()
        new_df = file_to_Save()
        if isinstance(new_df, pd.DataFrame) == True:
            path = sub_path +"_converted.txt"
            print('Saving data...')
            new_df.to_csv(path, index=False, sep='\t')
            print(':::  ended successfully!  :::')
        else:
            for key in new_df:
                path = sub_path +'/'+ key[:-5]+"_converted.txt"
                print(f'\nSaving data...{key[:-12]}...')
                new_df[key].to_csv(path, index=False, sep='\t')
                print(':::  ended successfully!  :::\n') 
        
    def nothing():
        var_one.get()
        
    ###############################
    def view_Data():
        data = file_to_Save()
        if isinstance(data, pd.DataFrame) == True:
            path = select_box.get()
            label = path.split('/')[-1][:-5]
            columns = data.columns
            
            # Placing the plots in the plane
            plot1 = plt.subplot2grid((2,1), (0, 0))
            plot2 = plt.subplot2grid((2,1), (1, 0))
    
            plot1.plot(data[columns[0]], data[columns[1]], label = label)
            plot1.legend()

            plot2.plot(data[columns[2]], data[columns[3]])

        else:
            # Placing the plots in the plane
            plot1 = plt.subplot2grid((2,1), (0, 0))
            plot2 = plt.subplot2grid((2,1), (1, 0))
            
            for key in data:
                columns = data[key].columns
                
                plot1.plot(data[key][columns[0]], data[key][columns[1]], label = key[:-5])
                plot1.legend()
    
                plot2.plot(data[key][columns[2]], data[key][columns[3]])
                
        plot2.axvline(x = 1.23, color = 'r', linestyle='--', label = 'Potential = 1.23 V_Vs_RHE')
                
        plot1.set_xlabel('Potential applied (V)')
        plot1.set_ylabel('Current (A)')
        plot2.set_xlabel('Potential(V_Vs_RHE)')
        plot2.set_ylabel('Current density (mA/cm^2)')
        
        # Packing all the plots and displaying them
        plt.tight_layout()
        plt.show()
    ###############################
    
    ##############################
    # Between frame select file
    frame_select_file = LabelFrame(top, padx=5, pady=5)#padx and pady inside of the frame
    # in frame text="..." is optional
    
    frame_select_file.grid(row=1, column=0, padx=10, pady=5, sticky="nsew")#padx and pady outside of the frame
    
    #select file: box and button 
    select_box = Entry(frame_select_file, width=23, font=("", 11))
    select_box.insert(0, "Type or select the file / folder")
    select_box.grid(row=0, column=1, pady=5, padx=5, ipady=3)
    
    select_button = Button(frame_select_file, text="Select File / Folder",
                          font=("", 10), background="#E8E8E8", width=14, 
                          command=lambda: open_file())
    select_button.grid(row=0, column=0, pady=5, padx=5)
    ###############################


    ###############################
    # Between frame PEC quantity
    frame_PEC_quantity = LabelFrame(top, text="Quantity of files", padx=5, pady=5)#padx and pady inside of the frame
    # in frame text="..." is optional
    frame_PEC_quantity.grid(row=0, column=0, padx=10, pady=5, sticky="nsew")#padx and pady outside of the frame
    
    var_one = BooleanVar()
    var_one.set(True)
    check_one_file = Checkbutton(frame_PEC_quantity, text="Only one file", width=20, 
                                      variable = var_one, command = nothing)
    
    check_one_file.grid(row=1, column=1, pady=5, columnspan=1)

    var_several = BooleanVar()
    check_several_files = Checkbutton(frame_PEC_quantity, text="Several files", 
                                      variable = var_several)
    var_several.set(False)
    check_several_files.grid(row=1, column=2, pady=5, columnspan=2)
    ###############################
    
    
    ###############################
    # Between frame PEC
    
    frame_file_PEC = LabelFrame(top, text="PEC Data", padx=5, pady=5)#padx and pady inside of the frame
    
    frame_file_PEC.grid(row=2, column=0, padx=10, pady=5, sticky="nsew")#padx and pady outside of the frame
    
    pH_label= Label(frame_file_PEC, text="pH",width=10)
    pH_label.grid(row=0, column=0, pady=5, columnspan=1)
    
    pH_box = Entry(frame_file_PEC, font=("", 12), width=8)
    pH_box.insert(0, "7")
    pH_box.grid(row=0, column=1, pady=5)
    
    Area_label= Label(frame_file_PEC, text="Area (cm^2)",width=10)
    Area_label.grid(row=1, column=0, pady=5, columnspan=1)
    
    Area_box = Entry(frame_file_PEC, font=("", 12), width=8)
    Area_box.insert(0, "1")
    Area_box.grid(row=1, column=1, pady=5)
    
    #convert file: button 
    conv_button = Button(frame_file_PEC, text="Save Data",
                          font=("", 12), background="#E8E8E8", width=17, 
                          command=lambda: save_Data1())
    conv_button.grid(row=0, column=2, rowspan=2, sticky="nsew", pady=5, padx=5)
    
    ###############################

    ###############################
    # Between frame options

    view_file = LabelFrame(top, text="View Measurement Without Saving", padx=5, pady=5)#padx and pady inside of the frame

    view_file.grid(row=3, column=0, padx=10, pady=5, sticky="nsew")#padx and pady outside of the frame

    conv_button = Button(view_file, text="View Measurement",
                          font=("", 12), background="#E8E8E8", width=34, 
                          command=lambda: view_Data())
    conv_button.grid(row=0, column=1, sticky="nsew", pady=5, padx=5)
    ###############################

    
def top_chronoA_conv():
    top = Toplevel()
    top.title("Chronoamperometry_Tool")
    top.geometry("360x310+330+430")
    
    ###############################
    def open_file():
        if var_one.get()== False and var_several.get()==False:
            print('Choose one option!')
        if var_one.get()== True and var_several.get()==True:
            print('Choose only one option!')
            var_one.set(False)
            var_several.set(False)  
        if var_one.get()== True and var_several.get()==False:
            open_file_name = askopenfilename()
            select_box.delete(0,"end")
            select_box.insert(0, open_file_name)
        if var_one.get()== False and var_several.get()==True:
            open_folder_name = askdirectory()
            select_box.delete(0,"end")
            select_box.insert(0, open_folder_name) 
    ###############################
    
    def from_PEC_convert(path):
        Area = float(Area_box.get())
        data = pd.read_excel(path, usecols=['Time (s)', 'WE(1).Current (A)'])
        data['Current_density(mA/cm^2)'] = (data["WE(1).Current (A)"]*1000)/Area
        data = data.rename(columns={"WE(1).Current (A)": "Current(A)"})
        return data
    
    def subPath():
    	#global sub_path
        if select_box.get()[-5:]==".xlsx":
            sub_path = select_box.get()[:-5]
        else:
            sub_path = select_box.get()
        return sub_path
    
    def file_to_Save():
        if var_one.get()== True and var_several.get()==False:
            path = select_box.get()
            return from_PEC_convert(path)
        else:
            data_txt = [file for file in os.listdir(select_box.get()) if file[-4:]=='XLSX' or file[-4:]=='xlsx']  
            data_dic = {}
            for file in data_txt:
                path = select_box.get()+'/'+file
                data_dic[file] = from_PEC_convert(path)
            return data_dic
    
    def save_Data1():
        sub_path = subPath()
        new_df = file_to_Save()
        if isinstance(new_df, pd.DataFrame) == True:
            path = sub_path +"_converted.txt"
            print('Saving data...')
            new_df.to_csv(path, index=False, sep='\t')
            print(':::  ended successfully!  :::')
        else:
            for key in new_df:
                path = sub_path +'/'+ key[:-5]+"_converted.txt"
                print(f'\nSaving data...{key[:-12]}...')
                new_df[key].to_csv(path, index=False, sep='\t')
                print(':::  ended successfully!  :::\n') 
        
    def nothing():
        var_one.get()
        
    ###############################
    def view_Data():
        data = file_to_Save()
        if isinstance(data, pd.DataFrame) == True:
            path = select_box.get()
            label = path.split('/')[-1][:-5]
            columns = data.columns
            
            # Placing the plots in the plane
            plot1 = plt.subplot2grid((2,1), (0, 0))
            plot2 = plt.subplot2grid((2,1), (1, 0))
    
            plot1.plot(data[columns[0]], data[columns[1]], label = label)
            plot1.legend()

            plot2.plot(data[columns[0]], data[columns[2]])

        else:
            # Placing the plots in the plane
            plot1 = plt.subplot2grid((2,1), (0, 0))
            plot2 = plt.subplot2grid((2,1), (1, 0))
            
            for key in data:
                columns = data[key].columns
                
                plot1.plot(data[key][columns[0]], data[key][columns[1]], label = key[:-5])
                plot1.legend()
    
                plot2.plot(data[key][columns[0]], data[key][columns[2]])

        plot1.set_xlabel('time (s)')
        plot1.set_ylabel('Current (A)')
        plot2.set_xlabel('time (s)')
        plot2.set_ylabel('Current density (mA/cm^2)')
        
        # Packing all the plots and displaying them
        plt.tight_layout()
        plt.show()
    ###############################
    
    ##############################
    # Between frame select file
    frame_select_file = LabelFrame(top, padx=5, pady=5)#padx and pady inside of the frame
    # in frame text="..." is optional
    
    frame_select_file.grid(row=1, column=0, padx=10, pady=5, sticky="nsew")#padx and pady outside of the frame
    
    #select file: box and button 
    select_box = Entry(frame_select_file, width=23, font=("", 11))
    select_box.insert(0, "Type or select the file / folder")
    select_box.grid(row=0, column=1, pady=5, padx=5, ipady=3)
    
    select_button = Button(frame_select_file, text="Select File / Folder",
                          font=("", 10), background="#E8E8E8", width=14, 
                          command=lambda: open_file())
    select_button.grid(row=0, column=0, pady=5, padx=5)
    ###############################


    ###############################
    # Between frame PEC quantity
    frame_PEC_quantity = LabelFrame(top, text="Quantity of files", padx=5, pady=5)#padx and pady inside of the frame
    # in frame text="..." is optional
    frame_PEC_quantity.grid(row=0, column=0, padx=10, pady=5, sticky="nsew")#padx and pady outside of the frame
    
    var_one = BooleanVar()
    var_one.set(True)
    check_one_file = Checkbutton(frame_PEC_quantity, text="Only one file", width=20, 
                                      variable = var_one, command = nothing)
    
    check_one_file.grid(row=1, column=1, pady=5, columnspan=1)

    var_several = BooleanVar()
    check_several_files = Checkbutton(frame_PEC_quantity, text="Several files", 
                                      variable = var_several)
    var_several.set(False)
    check_several_files.grid(row=1, column=2, pady=5, columnspan=2)
    ###############################
    
    
    ###############################
    # Between frame PEC
    
    frame_file_PEC = LabelFrame(top, text="Data", padx=5, pady=5)#padx and pady inside of the frame
    
    frame_file_PEC.grid(row=2, column=0, padx=10, pady=5, sticky="nsew")#padx and pady outside of the frame
    
    Area_label= Label(frame_file_PEC, text="Area (cm^2)",width=10)
    Area_label.grid(row=0, column=0, pady=5, columnspan=1)
    
    Area_box = Entry(frame_file_PEC, font=("", 12), width=8)
    Area_box.insert(0, "1")
    Area_box.grid(row=0, column=1, pady=5)
    
    #convert file: button 
    conv_button = Button(frame_file_PEC, text="Save Data",
                          font=("", 12), background="#E8E8E8", width=17, 
                          command=lambda: save_Data1())
    conv_button.grid(row=0, column=2, rowspan=1, sticky="nsew", pady=5, padx=5)
    
    ###############################

    ###############################
    # Between frame options

    view_file = LabelFrame(top, text="View Measurement Without Saving", padx=5, pady=5)#padx and pady inside of the frame

    view_file.grid(row=3, column=0, padx=10, pady=5, sticky="nsew")#padx and pady outside of the frame

    conv_button = Button(view_file, text="View Measurement",
                          font=("", 12), background="#E8E8E8", width=34, 
                          command=lambda: view_Data())
    conv_button.grid(row=0, column=1, sticky="nsew", pady=5, padx=5)
    ###############################
