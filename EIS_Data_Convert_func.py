# -*- coding: utf-8 -*-
"""
Created on Thu Jan 25 12:30:38 2024

@author: jccad
"""

from tkinter import (LabelFrame, Entry, Button, Checkbutton, Toplevel, Label, 
                    DISABLED, NORMAL, BooleanVar, END)
# StringVar,
from tkinter.filedialog import (askopenfilename, askdirectory)
import pandas as pd
import matplotlib.pyplot as plt
import math
import os

def top_EIS_Data_Convert():
    top1 = Toplevel()
    top1.title("EIS_Tool")
    top1.geometry("605x390+330+60")
    
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

    def from_Imp_Spect_Or_Sol(path): # From Solartron          
        # freq Z' and Z'' from columns 5, 9 and 10 respectively 
        data = pd.read_csv(path, sep="\t", skiprows = 4, encoding = 'ISO-8859-1', names = range(0, 12))
        #data.columns = range(0, data.columns.size)
        data = data.rename(columns={3: "Frequency (Hz)", 7: "Z'", 8: "Z''"})
        data["Z''"] = data["Z''"].astype(float)*(-1)
        data = data.rename(columns={"Z''": "-Z''"})
        #data = data.rename(columns={"Frequency": "Frequency (Hz)"})
        
        #data = data.drop(data.index[data["-Z''"] < 0])
        #data = data.drop(data.index[data["Z'"] < 0])
        
        new_df = data[["Z'", "-Z''", "Frequency (Hz)"]].copy()
        
        return new_df

    def from_Imp_Spect_Norm(path, geometricFactor):
        new_df = from_Imp_Spect_Or_Sol(path)
        new_df["Z'"] = geometricFactor * new_df["Z'"]
        new_df["-Z''"] = geometricFactor * new_df["-Z''"]
        return new_df

    def view_Data():
        path = select_box.get()
        label = path.split('/')[-1]
        new_df = file_to_Save()
        
        if isinstance(new_df, list) == True:

            data_to_plot = new_df[0] # plota somente dados originais
            data_to_plot.columns = ["Z'", "-Z''", "Frequency (Hz)"]
            
            # Placing the plots in the plane
            plot1 = plt.subplot2grid((2,2), (0, 0), colspan=2)
            plot2 = plt.subplot2grid((2,2), (1, 0))
            plot3 = plt.subplot2grid((2,2), (1, 1))
              
            # Plot Nyquist plot 
            plot1.plot(data_to_plot["Z'"], data_to_plot["-Z''"], 'ro', label = label)
            plot1.axis('scaled')
            plot1.legend()
            plot1.set_xlabel("Z' (Ohm)")
            plot1.set_ylabel("-Z'' (Ohm)")
            
            # Plot Z' vs. freq
            plot2.semilogx(data_to_plot["Frequency (Hz)"], data_to_plot["Z'"], 'bo')
            plot2.set_xlabel("frequency (Hz)")
            plot2.set_ylabel("Z' (Ohm)")
            
            # Plot -Z'' vs. freq
            plot3.semilogx(data_to_plot["Frequency (Hz)"], data_to_plot["-Z''"], 'go')
            plot3.set_xlabel("frequency (Hz)")
            plot3.set_ylabel("-Z'' (Ohm)")

        else:
            # Placing the plots in the plane
            plot1 = plt.subplot2grid((1,1), (0, 0))
            
            for key in new_df:
            
                new_df[key][0].columns = ["Z'", "-Z''", "Frequency (Hz)"]
                columns = new_df[key][0].columns
                
                # Plot Niquist plot 
                plot1.plot(new_df[key][0][columns[0]], new_df[key][0][columns[1]], label = key[:-4])
                plot1.legend()
                
            plot1.set_xlabel("Z' (Ohm)")
            plot1.set_ylabel("-Z'' (Ohm)")
        
        # Packing all the plots and displaying them
        plt.tight_layout()
        plt.show()

    def subPath():
        #global sub_path
        if select_box.get()[-4:]==".txt":
            sub_path = select_box.get()[:-4]
        elif select_box.get()[-4:]==".csv":
            #sub_path = select_box.get()[:-4]
            sample = ''#"SOME_TEXT" #'GDC60NiO_'
            sub_path = select_box.get()[:select_box.get().rfind("/")+1]+sample+select_box.get()[select_box.get().rfind("/")+1:-4]
        elif select_box.get()[-2:]==".z":
            sub_path = select_box.get()[:-2]
        else:
            sub_path = select_box.get()
        return sub_path
            
    ###############################
        
    ###############################
    def nothing():
        var_one.get()
    
    def nothing2():
        varOr_Sol.get() 
            
    def activate_NormData_SL():
        varSL.get()
        if S_L_box['state'] == DISABLED:
            S_L_box['state'] = NORMAL
        else:
            S_L_box['state'] = DISABLED
          
    def activate_NormData_At():
        varAt.get()
        if diametro_box['state'] == DISABLED or thickness_box['state'] == DISABLED:
            diametro_box['state'] = NORMAL
            thickness_box['state'] = NORMAL
        else:
            diametro_box['state'] = DISABLED
            thickness_box['state'] = DISABLED
        
    ###############################
    
    def Or_or_Norm(path):
        if varSL.get()==True and varAt.get()==True:
                varSL.set(False)
                varAt.set(False)
                activate_NormData_SL()
                activate_NormData_At()
        else:
            if varOr_Sol.get() == True:
                new_df_Or = from_Imp_Spect_Or_Sol(path)
                new_df_Or.columns=[str(new_df_Or.shape[0]), '', '']
            else: new_df_Or = 0
            
            if varSL.get()==True or varAt.get()==True:
                if varSL.get()==True:
                    geometricFactor = float(S_L_box.get())/10
                if varAt.get()==True:
                    Area = math.pi*(float(diametro_box.get())/2)**2
                    geometricFactor = Area/(float(thickness_box.get())*10)
                new_df_Norm = from_Imp_Spect_Norm(path, geometricFactor)
                new_df_Norm.columns=[str(new_df_Norm.shape[0]), '', '']  
            else: new_df_Norm = 0
            
        return new_df_Or, new_df_Norm
    
    def file_to_Save():
        if var_one.get()== True and var_several.get()==False:
            path = select_box.get()
            new_df_Or, new_df_Norm = Or_or_Norm(path)              
            return [new_df_Or, new_df_Norm]
        else:
            data_txt = [file for file in os.listdir(select_box.get()) if file[-3:]=='CSV' or file[-3:]=='csv']  
            data_dic = {}
            for file in data_txt:
                path = select_box.get()+'/'+file
                new_df_Or, new_df_Norm = Or_or_Norm(path)
                data_dic[file] = [new_df_Or, new_df_Norm]
            return data_dic

    ###############################

    def save_IS_Data():
        sub_path = subPath()
        new_df = file_to_Save()
        if isinstance(new_df, list) == True:
            for i in range(len(new_df)):
                if i==0:
                    sufix = "_Or.txt"
                if i==1:
                    sufix = "_Norm.txt"   
                if isinstance(new_df[i], pd.DataFrame) == True:
                    path = sub_path + sufix
                    print('Saving data...')
                    new_df[i].to_csv(path, index=False, sep='\t')
                    print(':::  ended successfully!  :::')
        else:
            for key in new_df:
                for i in range(len(new_df[key])):
                    if i==0:
                        sufix = "_Or.txt"
                    if i==1:
                        sufix = "_Norm.txt"   
                    if isinstance(new_df[key][i], pd.DataFrame) == True:
                        path = sub_path +'/'+ key[:-4]+sufix
                        print('Saving data...')
                        new_df[key][i].to_csv(path, index=False, sep='\t')
                        print(':::  ended successfully!  :::')
    
    ###############################
    

    ##############################
    # Between frame select file
    frame_select_file = LabelFrame(top1, padx=5, pady=5)#padx and pady inside of the frame
    # in frame text="..." is optional

    frame_select_file.grid(row=1, column=0, padx=10, pady=5, sticky="nsew")#padx and pady outside of the frame

    #select file: box and button 
    select_box = Entry(frame_select_file, width=43, font=("", 12))
    select_box.insert(0, "Type or select the file / folder")
    select_box.grid(row=0, column=1, pady=5, padx=5, ipady=3)

    select_button = Button(frame_select_file, text="Select File / Folder",
                          font=("", 12), background="#E8E8E8", width=17, 
                          command=lambda: open_file())
    select_button.grid(row=0, column=0, pady=5, padx=5)
    ############################### 
    
    ###############################
    # Between frame EIS quantity
    frame_EIS_quantity = LabelFrame(top1, text="Quantity of files", padx=5, pady=5)#padx and pady inside of the frame
    # in frame text="..." is optional
    frame_EIS_quantity.grid(row=0, column=0, padx=10, pady=5, sticky="nsew")#padx and pady outside of the frame
    
    var_one = BooleanVar()
    var_one.set(True)
    check_one_file = Checkbutton(frame_EIS_quantity, text="Only one file", width=20, 
                                      variable = var_one, command = nothing)
    
    check_one_file.grid(row=1, column=1, pady=5, columnspan=1)

    var_several = BooleanVar()
    check_several_files = Checkbutton(frame_EIS_quantity, text="Several files", 
                                      variable = var_several)
    var_several.set(False)
    check_several_files.grid(row=1, column=2, pady=5, columnspan=2)
    ###############################


    ###############################
    # Between frame frame_ISData
    frame_ISData = LabelFrame(top1, text="Data to Export", padx=5, pady=5)#padx and pady inside of the frame
    # in frame text="..." is optional

    frame_ISData.grid(row=2, column=0, padx=10, pady=5, sticky="nsew")#padx and pady outside of the frame

    ## From Solartron ##
    varOr_Sol = BooleanVar()
    varOr_Sol.set(True)
    check_IS_original_Sol = Checkbutton(frame_ISData, text="Original Data_ Solartron", width=20, 
                                    variable = varOr_Sol, command = nothing2)
    check_IS_original_Sol.grid(row=0, column=1, pady=5, columnspan=3)
    #############

    varSL = BooleanVar()
    check_IS_Normalized = Checkbutton(frame_ISData, text="Normalized Data by S/L", width=20, 
                                      variable = varSL, command=activate_NormData_SL)
    varSL.set(False)
    check_IS_Normalized.grid(row=1, column=1, pady=5, columnspan=1)
        
    Label_02 = Label(frame_ISData, text="S/L (mm)")
    Label_02.grid(row=2, column=1, columnspan=1, padx=5, sticky="nsew")

    S_L_box = Entry(frame_ISData, state=DISABLED)
    S_L_box.grid(row=3, column=1, pady=5, padx=5, ipady=3, sticky="nsew")

    varAt = BooleanVar()
    check_IS_Normalized2 = Checkbutton(frame_ISData, text="Normalized Data by diameter and thickness", 
                                      variable = varAt, command=activate_NormData_At)
    varAt.set(False)
    check_IS_Normalized2.grid(row=1, column=2, pady=5, columnspan=2)
     
    Label_03 = Label(frame_ISData, text="diameter (mm)")
    Label_03.grid(row=2, column=2, columnspan=1, padx=5, sticky="nsew")

    diametro_box = Entry(frame_ISData, state=DISABLED)
    diametro_box.grid(row=3, column=2, pady=5, padx=5, ipady=3, sticky="nsew")

    Label_04 = Label(frame_ISData, text="thickness (mm)")
    Label_04.grid(row=2, column=3, columnspan=1, padx=5, sticky="nsew")

    thickness_box = Entry(frame_ISData, state=DISABLED)
    thickness_box.grid(row=3, column=3, pady=5, padx=5, ipady=3, sticky="nsew")

    # save resistivity (real, imaginary) in Ohm*cm unit
    save_ISData_button = Button(frame_ISData, text="Save Data",
                      font=("", 12), background="#E8E8E8", width=13, 
                      command=lambda: save_IS_Data())
    save_ISData_button.grid(row=0, rowspan=4, column=0, columnspan=1, sticky="nsew", pady=5, padx=5)
    ###############################

    ###############################
    # Between frame options

    view_file = LabelFrame(top1, text="View Measurement Without Saving", padx=5, pady=5)#padx and pady inside of the frame

    view_file.grid(row=3, column=0, padx=10, pady=5, sticky="nsew")#padx and pady outside of the frame

    conv_button = Button(view_file, text="View Measurement",
                          font=("", 12), background="#E8E8E8", width=20, 
                          command=lambda: view_Data())
    conv_button.grid(row=0, column=1, sticky="nsew", pady=5, padx=5)

    ###############################
