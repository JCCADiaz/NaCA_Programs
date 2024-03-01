# -*- coding: utf-8 -*-
"""
Created on Thu Jan 25 10:45:07 2024

@author: jccad
"""

from tkinter import (Tk, LabelFrame, Entry, Button, Checkbutton, IntVar, Toplevel, Label, 
                    DISABLED, NORMAL, BooleanVar, Text, END, Menu, PhotoImage)
# StringVar,
from tkinter.filedialog import askopenfilename
import pandas as pd
import matplotlib.pyplot as plt

###############################
import Reagent_calculation_func as Rcf
import CG_Quantification_Table_func as CGQTf
import EIS_Data_Convert_func as EISDCf
import PEC_conversion_func as PECcf
import UV_Vis_conversion_func as UVViscf
import arduino_Temp_func as arduinoTf
###############################

root = Tk()
root.title("NaCA_Tools")
root.geometry("300x300+15+60")

background_image = PhotoImage(file = 'naca_logo.png')
background_image = background_image.zoom (3)
background_image = background_image.subsample(2)
image_label = Label(root, image=background_image)
image_label.pack()

# def teste():
#     print('XXX')

###############################

###############################
# Create menu
menu_bar = Menu(root)
root.config(menu=menu_bar)

# Add items to the menu
file_menu = Menu(menu_bar, tearoff=False)
menu_bar.add_cascade(label = "File", menu = file_menu)

# create data processing menu
processing_menu = Menu(menu_bar, tearoff=False)
menu_bar.add_cascade(label = "Data processing", menu = processing_menu)

# create Reagent Calculation menu
Reagent_Calculation_menu = Menu(menu_bar, tearoff=False)
menu_bar.add_cascade(label = "Reagent Calculation", menu = Reagent_Calculation_menu)
# add menu items to the Reagent Calculation menu
Reagent_Calculation_menu.add_command(label='Reagent Calculation', command = Rcf.top_Reagent_Calculation)
Reagent_Calculation_menu.add_separator()

# add menu items to the processing_menu
processing_menu.add_command(label='CG', command = CGQTf.top_CG_Qantification)
processing_menu.add_command(label='EIS', command = EISDCf.top_EIS_Data_Convert)
#processing_menu.add_command(label='PEC', command = PECcf.top_PEC_conv)
#processing_menu.add_command(label='UV-Vis', command=teste)

# Create Submenu PEC
PEC_submenu = Menu(processing_menu, tearoff=0)
processing_menu.add_cascade(label = "PEC", menu = PEC_submenu)

# Add items to PEC Submenu
PEC_submenu.add_command(label="Linear Sweep Voltammetry", command = PECcf.top_PEC_conv)
PEC_submenu.add_command(label="Chronoamperometry", command = PECcf.top_chronoA_conv)

# Create Submenu UV-Vis
UVVis_submenu = Menu(processing_menu, tearoff=0)
processing_menu.add_cascade(label = "UV-Vis", menu = UVVis_submenu)
processing_menu.add_separator()

# Add items to UV-Vis Submenu
UVVis_submenu.add_command(label="Absorbance", command = UVViscf.top_Abs_conv)
UVVis_submenu.add_command(label="Reflectance", command = UVViscf.top_Ref_conv)
UVVis_submenu.add_command(label="transmittance", command = UVViscf.top_Tra_conv)

# # create Help menu
# help_menu = Menu(menu_bar, tearoff=False)
# menu_bar.add_cascade(label = "Help", menu = help_menu)

# add Exit menu item
file_menu.add_command(label='Temperature measurement', command=arduinoTf.top_arduino_measure)

file_menu.add_separator()
file_menu.add_command(label='Exit', command=root.destroy)
###############################

###############################

root.mainloop()