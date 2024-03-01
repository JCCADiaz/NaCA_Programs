# -*- coding: utf-8 -*-
"""
Created on Thu Jan 25 12:30:38 2024

@author: jccad
"""

from tkinter import (LabelFrame, Entry, Button, Checkbutton, Toplevel, Label, 
                    DISABLED, NORMAL, BooleanVar, END)
# StringVar,
from tkinter.filedialog import askopenfilename
import pandas as pd
import matplotlib.pyplot as plt


def top_EIS_Data_Convert():
    top1 = Toplevel()
    top1.title("EIS_Tool")
    top1.geometry("605x320+330+60")

    ###############################
    def open_file():
        open_file_name = askopenfilename()
        select_box.delete(0,"end")
        select_box.insert(0, open_file_name)
    ###############################

    ###############################

    def from_Imp_Spect_Or_Sol(): # From Solartron
        path = select_box.get()
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

    def from_Imp_Spect_Norm(geometricFactor):
        new_df = from_Imp_Spect_Or_Sol()
        new_df["Z'"] = geometricFactor * new_df["Z'"]
        new_df["-Z''"] = geometricFactor * new_df["-Z''"]
        return new_df

    def view_Data():
        path = select_box.get()
        label = path.split('/')[-1]
        data = from_Imp_Spect_Or_Sol()
        
        # Placing the plots in the plane
        plot1 = plt.subplot2grid((2,2), (0, 0), colspan=2)
        plot2 = plt.subplot2grid((2,2), (1, 0))
        plot3 = plt.subplot2grid((2,2), (1, 1))
          
        # Plot Nyquist plot 
        plot1.plot(data["Z'"], data["-Z''"], 'ro', label = label)
        plot1.axis('scaled')
        plot1.legend()
        plot1.set_xlabel("Z' (Ohm)")
        plot1.set_ylabel("-Z'' (Ohm)")
        
        # Plot Z' vs. freq
        plot2.semilogx(data["Frequency (Hz)"], data["Z'"], 'bo')
        plot2.set_xlabel("frequency (Hz)")
        plot2.set_ylabel("Z' (Ohm)")
        
        # Plot -Z'' vs. freq
        plot3.semilogx(data["Frequency (Hz)"], data["-Z''"], 'go')
        plot3.set_xlabel("frequency (Hz)")
        plot3.set_ylabel("-Z'' (Ohm)")
          
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
        if area_box['state'] == DISABLED or thickness_box['state'] == DISABLED:
            area_box['state'] = NORMAL
            thickness_box['state'] = NORMAL
        else:
            area_box['state'] = DISABLED
            thickness_box['state'] = DISABLED
        
    ###############################
    def save_IS_Data():
        sub_path = subPath()
        if varSL.get()==True and varAt.get()==True:
            varSL.set(False)
            varAt.set(False)
            activate_NormData_SL()
            activate_NormData_At()
        else:       
            if varOr_Sol.get() == True:
                path = sub_path + "_Or.txt"
                print(path)
                new_df = from_Imp_Spect_Or_Sol()
                new_df.columns=[str(new_df.shape[0]), '', '']
                print('Saving data...')
                new_df.to_csv(path, index=False, sep='\t')
                print(':::  ended successfully!  :::')
                
            if varSL.get()==True or varAt.get()==True:
                if varSL.get()==True:
                    geometricFactor = float(S_L_box.get())/10
                if varAt.get()==True:
                    geometricFactor = float(area_box.get())/(float(thickness_box.get())*10)
                path = sub_path + "_Norm.txt"
                new_df = from_Imp_Spect_Norm(geometricFactor)
                new_df.columns=[str(new_df.shape[0]), '', '']
                print('Saving data...')
                new_df.to_csv(path, index=False, sep='\t')
                print(':::  ended successfully!  :::')
        
    ###############################

    ##############################
    # Between frame select file
    frame_select_file = LabelFrame(top1, padx=5, pady=5)#padx and pady inside of the frame
    # in frame text="..." is optional

    frame_select_file.grid(row=0, column=0, padx=10, pady=5, sticky="nsew")#padx and pady outside of the frame

    #select file: box and button 
    select_box = Entry(frame_select_file, width=47, font=("", 12))
    select_box.insert(0, "Type or select the file")
    select_box.grid(row=0, column=1, pady=5, padx=5, ipady=3)

    select_button = Button(frame_select_file, text="Select File",
                          font=("", 12), background="#E8E8E8", width=13, 
                          command=lambda: open_file())
    select_button.grid(row=0, column=0, pady=5, padx=5)
    ###############################


    ###############################
    # Between frame frame_ISData
    frame_ISData = LabelFrame(top1, text="Data to Export", padx=5, pady=5)#padx and pady inside of the frame
    # in frame text="..." is optional

    frame_ISData.grid(row=1, column=0, padx=10, pady=5, sticky="nsew")#padx and pady outside of the frame

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
    check_IS_Normalized2 = Checkbutton(frame_ISData, text="Normalized Data by Area and thickness", 
                                      variable = varAt, command=activate_NormData_At)
    varAt.set(False)
    check_IS_Normalized2.grid(row=1, column=2, pady=5, columnspan=2)
     
    Label_03 = Label(frame_ISData, text="Area (mm^2)")
    Label_03.grid(row=2, column=2, columnspan=1, padx=5, sticky="nsew")

    area_box = Entry(frame_ISData, state=DISABLED)
    area_box.grid(row=3, column=2, pady=5, padx=5, ipady=3, sticky="nsew")

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

    view_file.grid(row=2, column=0, padx=10, pady=5, sticky="nsew")#padx and pady outside of the frame

    conv_button = Button(view_file, text="View Measurement",
                          font=("", 12), background="#E8E8E8", width=20, 
                          command=lambda: view_Data())
    conv_button.grid(row=0, column=1, sticky="nsew", pady=5, padx=5)

    ###############################
