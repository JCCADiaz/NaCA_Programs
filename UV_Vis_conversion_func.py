# -*- coding: utf-8 -*-
"""
Created on Thu Jan 25 15:32:31 2024

@author: jccad
"""

from tkinter import (LabelFrame, Entry, Button, Toplevel, Label, END, Checkbutton, BooleanVar)

from tkinter.filedialog import (askopenfilename, askdirectory)
import pandas as pd
import math
import os
import matplotlib.pyplot as plt

def top_Abs_conv():
    top_Abs = Toplevel()
    top_Abs.title("Absorbance_Tool")
    top_Abs.geometry("360x310+330+60")
    
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
    def from_Abs_convert(path):
        h = 4.135667696E-15 #eV s
        c = 299792458 # m s-1
        
        thickness = 1000*1E-9# float(thickness_box.get())*1E-9 # nm
        get_n = n_box.get()
        if get_n=='1/2':
            get_n = 0.5
            
        n = float(get_n) # 2 Direct, 1/2 Indirect

        ##########################################################
        # data = pd.read_csv(path, sep=",", skiprows = 43, encoding = 'ISO-8859-1', names = ['Wavelength(nm)','x','y','Absorbance'], 
        #         dtype={'Wavelength(nm)': 'int64',
        #                 'x': 'int64',
        #                 'y': 'string',
        #                 'Absorbance': 'float64'})

        # data['factor'] = [-1 if '-' in i else 1 for i in data['y']]

        # data = data.astype({'y': 'float64'})
        # data['y'] = data['y'].abs()

        # data['Absorbance'] = data['factor']*(data['y']+data['Absorbance']/1000)
        ##########################################################
        data = pd.read_csv(path, sep="\t", decimal=",", skiprows = 43, names = ['Wavelength(nm)','Absorbance'],
                dtype={'Wavelength(nm)': 'float64', 'Absorbance': 'float64'})

        data['Normalized A'] = 1*(data['Absorbance'] - data['Absorbance'].min()) / (data['Absorbance'].max() - data['Absorbance'].min())
        
        data['hc/lambda(eV)'] = h*c/(data['Wavelength(nm)']*1E-9)
       
        if n==2:
            data['(alpha h nu)^2(eV m-1)^2'] = ((data['Normalized A']*h*c)/(thickness*math.log10(math.e)*data['Wavelength(nm)']*1E-9))**n
            data_out = data[['Wavelength(nm)', 'Absorbance', 'hc/lambda(eV)', '(alpha h nu)^2(eV m-1)^2']].copy() 
        
        if n==1/2:
            data['(alpha h nu)^1/2(eV m-1)^1/2'] = ((data['Normalized A']*h*c)/(thickness*math.log10(math.e)*data['Wavelength(nm)']*1E-9))**n
            data_out = data[['Wavelength(nm)', 'Absorbance', 'hc/lambda(eV)', '(alpha h nu)^1/2(eV m-1)^1/2']].copy() 
        return data_out
    
    def subPath():
    	#global sub_path
        if select_box.get()[-4:]==".txt":
            sub_path = select_box.get()[:-12]
        elif select_box.get()[-2:]==".z":
            sub_path = select_box.get()[:-2]
        else:
            sub_path = select_box.get()
        return sub_path
        
    
    def file_to_Save():
        if var_one.get()== True and var_several.get()==False:
            path = select_box.get()
            return from_Abs_convert(path)
        else:
            data_txt = [file for file in os.listdir(select_box.get()) if file[-3:]=='TXT' or file[-3:]=='txt']  
            data_dic = {}
            for file in data_txt:
                path = select_box.get()+'/'+file
                data_dic[file] = from_Abs_convert(path)
            return data_dic
    
    def save_Data2():
        sub_path = subPath()
        new_df = file_to_Save()
        if isinstance(new_df, pd.DataFrame) == True:
            path = sub_path +"_converted.txt"
            print('Saving data...')
            new_df.to_csv(path, index=False, sep='\t')
            print(':::  ended successfully!  :::')
        else:
            for key in new_df:
                path = sub_path +'/'+ key[:-12]+"_converted.txt"
                print(f'\nSaving data...{key[:-12]}...')
                new_df[key].to_csv(path, index=False, sep='\t')
                print(':::  ended successfully!  :::\n') 
        
    def nothing():
        var_one.get()
        
    def view_Data():
        data = file_to_Save()
        if isinstance(data, pd.DataFrame) == True:
            path = select_box.get()
            label = path.split('/')[-1][:-12]
            columns = data.columns
            
            # Placing the plots in the plane
            plot1 = plt.subplot2grid((2,1), (0, 0))
            plot2 = plt.subplot2grid((2,1), (1, 0))
    
            # Plot Absorbance Vs.Wavelength
            plot1.plot(data[columns[0]], data[columns[1]], label = label)
            plot1.legend()

            # Plot (alpha h nu)^n Vs. hc/lambda
            plot2.plot(data[columns[2]], data[columns[3]])

        else:
            # Placing the plots in the plane
            plot1 = plt.subplot2grid((2,1), (0, 0))
            plot2 = plt.subplot2grid((2,1), (1, 0))
            
            for key in data:
                columns = data[key].columns
                
                # Plot Absorbance Vs.Wavelength
                plot1.plot(data[key][columns[0]], data[key][columns[1]], label = key[:-12])
                plot1.legend()
    
                # Plot (alpha h nu)^n Vs. hc/lambda
                plot2.plot(data[key][columns[2]], data[key][columns[3]])
                
        plot1.set_xlabel('Wavelength (nm)')
        plot1.set_ylabel('Absorbance')
        plot2.set_xlabel('hc/lambda (eV)')
        plot2.set_ylabel('(alpha h nu)^n (eV m-1)^n')
        
        # Packing all the plots and displaying them
        plt.tight_layout()
        plt.show()
    ###############################
    
    ##############################
    # Between frame select file
    frame_select_file = LabelFrame(top_Abs, padx=5, pady=5)#padx and pady inside of the frame
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
    # Between frame Abs quantity
    frame_Abs_quantity = LabelFrame(top_Abs, text="Quantity of files", padx=5, pady=5)#padx and pady inside of the frame
    # in frame text="..." is optional
    frame_Abs_quantity.grid(row=0, column=0, padx=10, pady=5, sticky="nsew")#padx and pady outside of the frame
    
    var_one = BooleanVar()
    var_one.set(True)
    check_one_file = Checkbutton(frame_Abs_quantity, text="Only one file", width=20, 
                                      variable = var_one, command = nothing)
    
    check_one_file.grid(row=1, column=1, pady=5, columnspan=1)

    var_several = BooleanVar()
    check_several_files = Checkbutton(frame_Abs_quantity, text="Several files", 
                                      variable = var_several)
    var_several.set(False)
    check_several_files.grid(row=1, column=2, pady=5, columnspan=2)
    ###############################
    
    ###############################
    # Between frame UVVis
    frame_file_UVVis = LabelFrame(top_Abs, text="", padx=5, pady=5)#padx and pady inside of the frame
    
    frame_file_UVVis.grid(row=2, column=0, padx=10, pady=5, sticky="nsew")#padx and pady outside of the frame
    
    # thickness_label= Label(frame_file_UVVis, text="thickness (nm)",width=17)
    # thickness_label.grid(row=0, column=0, pady=5, columnspan=1)
    
    # thickness_box = Entry(frame_file_UVVis, font=("", 12), width=17)
    # thickness_box.insert(0, "1")
    # thickness_box.grid(row=1, column=0, pady=5)
    
    n_label= Label(frame_file_UVVis, text="n -> 2 Direct, 1/2 Indirect",width=20)
    n_label.grid(row=0, column=0, pady=5, columnspan=1)
    
    n_box = Entry(frame_file_UVVis, font=("", 12), width=17)
    n_box.insert(0, "2")
    n_box.grid(row=1, column=0, pady=5)
    
    #convert file: button 
    conv_button = Button(frame_file_UVVis, text="Save Data",
                          font=("", 12), background="#E8E8E8", width=17, 
                          command=lambda: save_Data2())
    conv_button.grid(row=0, column=1, rowspan=4, sticky="nsew", pady=5, padx=5)
    ###############################
    
    ###############################
    # Between frame options

    view_file = LabelFrame(top_Abs, text="View Measurement Without Saving", padx=5, pady=5)#padx and pady inside of the frame

    view_file.grid(row=3, column=0, padx=10, pady=5, sticky="nsew")#padx and pady outside of the frame

    conv_button = Button(view_file, text="View Measurement",
                          font=("", 12), background="#E8E8E8", width=34, 
                          command=lambda: view_Data())
    conv_button.grid(row=0, column=1, sticky="nsew", pady=5, padx=5)

    ###############################

##############################################################
##############################################################


def top_Ref_conv():
    top_Abs = Toplevel()
    top_Abs.title("Reflectance_Tool")
    top_Abs.geometry("360x310+330+330")
    
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
    def from_Ref_convert(path):
        h = 4.135667696E-15 #eV s
        c = 299792458 # m s-1
        
        get_n = n_box.get()
        if get_n=='1/2':
            get_n = 0.5
            
        n = float(get_n) # 2 Direct, 1/2 Indirect
        ##########################################################
        # data = pd.read_csv(path, sep=",", skiprows = 43, encoding = 'ISO-8859-1', names = ['Wavelength(nm)','x','y','Reflectance'], 
        #         dtype={'Wavelength(nm)': 'int64',
        #                 'x': 'int64',
        #                 'y': 'string',
        #                 'Reflectance': 'float64'})

        # data['factor'] = [-1 if '-' in i else 1 for i in data['y']]

        # data = data.astype({'y': 'float64'})
        # data['y'] = data['y'].abs()

        # data['Reflectance'] = data['factor']*(data['y']+data['Reflectance']/10)/100
        ##########################################################
        data = pd.read_csv(path, sep="\t", decimal=",", skiprows = 43, names = ['Wavelength(nm)','Reflectance'],
                dtype={'Wavelength(nm)': 'float64', 'Reflectance': 'float64'})

        data['hc/lambda(eV)'] = h*c/(data['Wavelength(nm)']*1E-9)
        
        # F(R)= (1-R)^2/(2*R) 
        if n==2:
            data['(F(R) h nu)^2(eV m-1)^2'] = ((((1-data['Reflectance'])**2)/(2*data['Reflectance']))*(h*c/(data['Wavelength(nm)']*1E-9)))**n
            data_out = data[['Wavelength(nm)', 'Reflectance', 'hc/lambda(eV)', '(F(R) h nu)^2(eV m-1)^2']].copy()   
        if n==1/2:
            data['(F(R) h nu)^1/2(eV m-1)^1/2'] = ((((1-data['Reflectance'])**2)/(2*data['Reflectance']))*(h*c/(data['Wavelength(nm)']*1E-9)))**n
            data_out = data[['Wavelength(nm)', 'Reflectance', 'hc/lambda(eV)', '(F(R) h nu)^1/2(eV m-1)^1/2']].copy()   

        return data_out
    
    def subPath():
    	#global sub_path
        if select_box.get()[-4:]==".txt":
            sub_path = select_box.get()[:-12]
        elif select_box.get()[-2:]==".z":
            sub_path = select_box.get()[:-2]
        else:
            sub_path = select_box.get()
        return sub_path
        
    def file_to_Save():
        if var_one.get()== True and var_several.get()==False:
            path = select_box.get()
            return from_Ref_convert(path)
        else:
            data_txt = [file for file in os.listdir(select_box.get()) if file[-3:]=='TXT' or file[-3:]=='txt']  
            data_dic = {}
            for file in data_txt:
                path = select_box.get()+'/'+file
                data_dic[file] = from_Ref_convert(path)
            return data_dic
    
    def save_Data2():
        sub_path = subPath()
        new_df = file_to_Save()
        if isinstance(new_df, pd.DataFrame) == True:
            path = sub_path +"_converted.txt"
            print('Saving data...')
            new_df.to_csv(path, index=False, sep='\t')
            print(':::  ended successfully!  :::')
        else:
            for key in new_df:
                path = sub_path +'/'+ key[:-12]+"_converted.txt"
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
            label = path.split('/')[-1][:-12]
            columns = data.columns
            
            # Placing the plots in the plane
            plot1 = plt.subplot2grid((2,1), (0, 0))
            plot2 = plt.subplot2grid((2,1), (1, 0))
    
            # Plot Absorbance Vs.Wavelength
            plot1.plot(data[columns[0]], data[columns[1]], label = label)
            plot1.legend()

            # Plot (alpha h nu)^n Vs. hc/lambda
            plot2.plot(data[columns[2]], data[columns[3]])

        else:
            # Placing the plots in the plane
            plot1 = plt.subplot2grid((2,1), (0, 0))
            plot2 = plt.subplot2grid((2,1), (1, 0))
            
            for key in data:
                columns = data[key].columns
                
                # Plot Absorbance Vs.Wavelength
                plot1.plot(data[key][columns[0]], data[key][columns[1]], label = key[:-12])
                plot1.legend()
    
                # Plot (alpha h nu)^n Vs. hc/lambda
                plot2.plot(data[key][columns[2]], data[key][columns[3]])
                
        plot1.set_xlabel('Wavelength (nm)')
        plot1.set_ylabel('Reflectance')
        plot2.set_xlabel('hc/lambda (eV)')
        plot2.set_ylabel('(F(R) h nu)^n (eV m-1)^n')
        
        # Packing all the plots and displaying them
        plt.tight_layout()
        plt.show()
    ###############################
    
    ##############################
    # Between frame select file
    frame_select_file = LabelFrame(top_Abs, padx=5, pady=5)#padx and pady inside of the frame
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
    # Between frame Abs quantity
    frame_Abs_quantity = LabelFrame(top_Abs, text="Quantity of files", padx=5, pady=5)#padx and pady inside of the frame
    # in frame text="..." is optional
    frame_Abs_quantity.grid(row=0, column=0, padx=10, pady=5, sticky="nsew")#padx and pady outside of the frame
    
    var_one = BooleanVar()
    var_one.set(True)
    check_one_file = Checkbutton(frame_Abs_quantity, text="Only one file", width=20, 
                                      variable = var_one, command = nothing)
    
    check_one_file.grid(row=1, column=1, pady=5, columnspan=1)

    var_several = BooleanVar()
    check_several_files = Checkbutton(frame_Abs_quantity, text="Several files", 
                                      variable = var_several)
    var_several.set(False)
    check_several_files.grid(row=1, column=2, pady=5, columnspan=2)
    ###############################
    
    ###############################
    # Between frame UVVis
    frame_file_UVVis = LabelFrame(top_Abs, text="", padx=5, pady=5)#padx and pady inside of the frame
    
    frame_file_UVVis.grid(row=2, column=0, padx=10, pady=5, sticky="nsew")#padx and pady outside of the frame
    
    n_label= Label(frame_file_UVVis, text="n -> 2 Direct, 1/2 Indirect",width=20)
    n_label.grid(row=0, column=0, pady=5, columnspan=1)
    
    n_box = Entry(frame_file_UVVis, font=("", 12), width=17)
    n_box.insert(0, "2")
    n_box.grid(row=1, column=0, pady=5)
    
    #convert file: button 
    conv_button = Button(frame_file_UVVis, text="Save Data",
                          font=("", 12), background="#E8E8E8", width=17, 
                          command=lambda: save_Data2())
    conv_button.grid(row=0, column=1, rowspan=4, sticky="nsew", pady=5, padx=5)
    ###############################
    
    ###############################
    # Between frame options

    view_file = LabelFrame(top_Abs, text="View Measurement Without Saving", padx=5, pady=5)#padx and pady inside of the frame

    view_file.grid(row=3, column=0, padx=10, pady=5, sticky="nsew")#padx and pady outside of the frame

    conv_button = Button(view_file, text="View Measurement",
                          font=("", 12), background="#E8E8E8", width=34, 
                          command=lambda: view_Data())
    conv_button.grid(row=0, column=1, sticky="nsew", pady=5, padx=5)

    ###############################
    
##############################################################
##############################################################


def top_Tra_conv():
    top_Abs = Toplevel()
    top_Abs.title("Transmitance_Tool")
    top_Abs.geometry("360x210+330+600")
    
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
    def from_Tra_convert(path):
        ##########################################################
        # data = pd.read_csv(path, sep=",", skiprows = 43, encoding = 'ISO-8859-1', names = ['Wavelength(nm)','x','y','Transmittance(%)'])
        # data['Transmittance(%)'] = data['y']+(data['Transmittance(%)']/10)
        ##########################################################
        data = pd.read_csv(path, sep="\t", decimal=",", skiprows = 43, names = ['Wavelength(nm)','Transmittance(%)'],
                dtype={'Wavelength(nm)': 'float64', 'Transmittance(%)': 'float64'})
        
        data_out = data[['Wavelength(nm)', 'Transmittance(%)']].copy()
        return data_out
    
    def subPath():
    	#global sub_path
        if select_box.get()[-4:]==".txt":
            sub_path = select_box.get()[:-12]
        elif select_box.get()[-2:]==".z":
            sub_path = select_box.get()[:-2]
        else:
            sub_path = select_box.get()
        return sub_path
        
    def file_to_Save():
        if var_one.get()== True and var_several.get()==False:
            path = select_box.get()
            return from_Tra_convert(path)
        else:
            data_txt = [file for file in os.listdir(select_box.get()) if file[-3:]=='TXT' or file[-3:]=='txt']  
            data_dic = {}
            for file in data_txt:
                path = select_box.get()+'/'+file
                data_dic[file] = from_Tra_convert(path)
            return data_dic
    
    def save_Data2():
        sub_path = subPath()
        new_df = file_to_Save()
        if isinstance(new_df, pd.DataFrame) == True:
            path = sub_path +"_converted.txt"
            print('Saving data...')
            new_df.to_csv(path, index=False, sep='\t')
            print(':::  ended successfully!  :::')
        else:
            for key in new_df:
                path = sub_path +'/'+ key[:-12]+"_converted.txt"
                print(f'\nSaving data...{key[:-12]}...')
                new_df[key].to_csv(path, index=False, sep='\t')
                print(':::  ended successfully!  :::\n') 
        
    def nothing():
        var_one.get()
        
    ###############################
    
    ##############################
    # Between frame select file
    frame_select_file = LabelFrame(top_Abs, padx=5, pady=5)#padx and pady inside of the frame
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
    # Between frame Abs quantity
    frame_Abs_quantity = LabelFrame(top_Abs, text="Quantity of files", padx=5, pady=5)#padx and pady inside of the frame
    # in frame text="..." is optional
    frame_Abs_quantity.grid(row=0, column=0, padx=10, pady=5, sticky="nsew")#padx and pady outside of the frame
    
    var_one = BooleanVar()
    var_one.set(True)
    check_one_file = Checkbutton(frame_Abs_quantity, text="Only one file", width=20, 
                                      variable = var_one, command = nothing)
    
    check_one_file.grid(row=1, column=1, pady=5, columnspan=1)

    var_several = BooleanVar()
    check_several_files = Checkbutton(frame_Abs_quantity, text="Several files", 
                                      variable = var_several)
    var_several.set(False)
    check_several_files.grid(row=1, column=2, pady=5, columnspan=2)
    ###############################
    
    ###############################
    # Between frame UVVis
    frame_file_UVVis = LabelFrame(top_Abs, text="", padx=5, pady=5)#padx and pady inside of the frame
    
    frame_file_UVVis.grid(row=2, column=0, padx=10, pady=5, sticky="nsew")#padx and pady outside of the frame
    
    #convert file: button 
    conv_button = Button(frame_file_UVVis, text="Save Data",
                          font=("", 12), background="#E8E8E8", width=34, 
                          command=lambda: save_Data2())
    conv_button.grid(row=0, column=1, rowspan=4, sticky="nsew", pady=5, padx=5)
    ###############################