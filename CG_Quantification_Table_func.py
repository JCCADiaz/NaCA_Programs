# -*- coding: utf-8 -*-
"""
Created on Thu Jan 25 11:52:46 2024

@author: jccad
"""

import math
import numpy as np
import pandas as pd
from datetime import datetime

from tkinter import (Tk, LabelFrame, Entry, Button, Checkbutton, IntVar, Toplevel, Label, Scrollbar,
                    DISABLED, NORMAL, BooleanVar, Text, END)
import matplotlib.pyplot as plt

def top_CG_Qantification():
    top = Toplevel()
    top.title("Quantification table for Photocatalysis experiments")
    top.geometry("635x550+330+60")
    ###############################
    # System parameters

    def Vt_value(line):
        D = 0.118 # external D=1/8", internal D = 1.18 mm  :: value in cm
        h = length_of_lines[line]
        vol = math.pi*h*(D/2)**2
        return vol

    length_of_lines = {'2':73, '4':272, '6':121, '8':314, '8H':298}
    dic_lineas = {'2':Vt_value('2'), '4':Vt_value('4'), '6':Vt_value('6'), '8':Vt_value('8'), '8H':Vt_value('8H')}

    gases = ['CO', 'CH4', 'C2H6', 'O2', 'H2', 'CO2']
    parametros_ab = [[0,59292],[0,55129],[0,13290],[4.8,254],[0,3198],[0,232.973]]
    dic_parametros_ab = dict(map(lambda i,j : (i,j) , gases,parametros_ab))

    ###############################

    def get_parameters(df_col, df_val, t):
        #tau = int(tau_box.get())
        line = line_box.get()
        gas = df_col
        A = df_val
        return line, gas, A, t

    def calculo_Evolution_gas(line, gas, A, t): # A:Area bajo la curva :: tau: tempo entre coletas, min :: 
        a, b = dic_parametros_ab[gas]    
        Vt = dic_lineas[line] #Vt: volume de tubulação, ml
        
        Vr = 100 # Volume do reator, ml 
        Vl = 1 # Volume do loop, ml
        f = 1.0 # fluxo, ml/min
        Vs = 30 # Volume da solução, ml
        # if t==0:
        #     Evolution_gas = 3*((A-a)/b)*(Vr+Vt+Vl+(t*f)-Vs)
        # else:
        Evolution_gas = 3*((A-a)/b)*(Vr+Vt+Vl+(t*f)-Vs)
        
        return Evolution_gas

    def create_df_evolution():
        df_in = data_list(size)
        df_out = pd.DataFrame(columns=['time(min)', *gases], index=range(Ty))
        df_out['time(min)']=df_in['time(min)']
        for gas in gases: 
            for i in range(len(df_in[gas])):
                df_col = gas
                df_val = df_in[gas][i]
                if i==0:
                    t = 0
                else: 
                    t=int(tau_box.get())
                
                Vt, gas, A, t = get_parameters(df_col, df_val, t)
                df_out[gas][i]= round(calculo_Evolution_gas(Vt, gas, A, t),5)
        return df_out

    def print_text():
        top_output_Tool()
            
    def plot_results():
        df0 = create_df_evolution()
        df = df0.cumsum()
        df['time(min)'] = df0['time(min)']
        df.plot(x='time(min)'); 
        plt.legend(loc='best')
        plt.show()

    ###############################
    # Between frame tau, line
    in_tau = 60
    in_Total_time = 300

    frame_tau_line = LabelFrame(top, text="tau value = interval time between injections", padx=5, pady=5)#padx and pady inside of the frame
    frame_tau_line.grid(row=0, column=0, padx=10, pady=5, sticky="nsew")#padx and pady outside of the frame
     
    Label_tau_box = Label(frame_tau_line, text="tau value (min)")
    Label_tau_box.grid(row=0, column=0, columnspan=1, padx=5, sticky="nsew")
    tau_box = Entry(frame_tau_line)
    tau_box.insert(0, str(in_tau))
    tau_box.config(state=DISABLED)
    tau_box.grid(row=1, column=0, pady=5, padx=5, ipady=3, sticky="nsew")

    Label_Tt_box = Label(frame_tau_line, text="Total time (min)")
    Label_Tt_box.grid(row=0, column=1, columnspan=1, padx=5, sticky="nsew")
    Tt_box = Entry(frame_tau_line)
    Tt_box.insert(0, str(in_Total_time))
    Tt_box.config(state=DISABLED)
    Tt_box.grid(row=1, column=1, pady=5, padx=5, ipady=3, sticky="nsew")

    Label_line_box = Label(frame_tau_line, text="Line Number")
    Label_line_box.grid(row=0, column=2, columnspan=1, padx=5, sticky="nsew")
    line_box = Entry(frame_tau_line)
    line_box.insert(0, "2")
    line_box.grid(row=1, column=2, pady=5, padx=5, ipady=3, sticky="nsew")
    ###############################

    ###############################
    # Between frame matrix
    frame_matrix = LabelFrame(top, text="Insert the values of the areas calculated for each gas retrieved from the cromatrogram", padx=5, pady=5)#padx and pady inside of the frame
    frame_matrix.grid(row=1, column=0, padx=10, pady=5, sticky="nsew")#padx and pady outside of the frame

    times = [n*int(tau_box.get()) for n in range((int(Tt_box.get())//int(tau_box.get()))+1)]
    Tx=len(gases)+1
    Ty=len(times)
    size = Tx*Ty
    my_entries = []

    def data_list(size):
        data_list = [my_entries[i].get() for i in range(size)]
        updated_data_list = []
        
        for val in data_list:
            if val=='':
                updated_data_list.append(None)
            else:
                updated_data_list.append(val.replace(',', '.'))
        
        list_of_lists = []
        for i in range(Ty):
            lista_i = updated_data_list[i*Tx:(i+1)*Tx]
            list_of_lists.append(lista_i)
            
        df_data_list = pd.DataFrame(list_of_lists, columns =['time(min)', *gases], dtype = float) 
        return df_data_list

    #row loop
    for y in range(Ty+1):
        if y==0:
            for x in range(Tx):
                if x==0:
                    label_cols = Label(frame_matrix, text='time (min)')
                    label_cols.grid(row=0, column=x, pady=10) 
                else:    
                    label_cols = Label(frame_matrix, text=gases[x-1])
                    label_cols.grid(row=0, column=x, pady=10)      
               
        else:
            #column loop
            for x in range(Tx):
                my_entry = Entry(frame_matrix, width=12)
                if x==0:
                    my_entry.insert(0, str(times[y-1]))
                my_entry.grid(row=y, column=x, pady=5, padx=5)
                my_entries.append(my_entry)
                
    ###############################   

    ###############################
    # Between frame output
    frame_output = LabelFrame(top, text="", padx=5, pady=5)#padx and pady inside of the frame
    frame_output.grid(row=3, column=0, padx=10, pady=5, sticky="nsew")#padx and pady outside of the frame

    results_button = Button(frame_output, width=34, text="Click to See Results",
                      font=("", 10), background="#E8E8E8",
                      command=lambda: print_text())
    results_button.grid(row=0, column=0, padx=10, pady=5,  sticky="nsew")

    plot_button = Button(frame_output, width=34, text="Click to plot the Results",
                      font=("", 10), background="#E8E8E8",
                      command=lambda: plot_results())
    plot_button.grid(row=0, column=2, padx=10, pady=5, sticky="nsew")
    ###############################  

    ###############################
    def top_output_Tool():
        top2 = Toplevel()
        top2.title("Report of results")
        top2.geometry("635x615+665+60")
        ###############################
        
        def print_data_output():
            message_box.delete('1.0', END)
            data_in = data_list(size)
            data_out = create_df_evolution()
            data_out_acc = data_out.cumsum()
            data_out_acc['time(min)'] = data_out['time(min)']
            
            text_in = (str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                        +'\n Quantification data for line Number '+ line_box.get() +'\n'
                        +'1) The original values of area for each gas.\n\n')
            text_out = '\n\n2) The quantity of each gas for the corresponding interval of time.\ndata unit = umol\n\n'
            text_out_acc = '\n\n3) The accumulated quantity of each gas in the corresponding time.\ndata unit = umol\n\n'
            
            message_box.insert('1.0', text_in)
            message_box.insert('end', data_in)
            
            message_box.insert('end', text_out)
            message_box.insert('end', data_out)
            
            message_box.insert('end', text_out_acc)
            message_box.insert('end', data_out_acc)
        ###############################
        # Between frame top_ouotput
        frame_top_ouotput = LabelFrame(top2, text="Calculated amount of gases", padx=5, pady=5)#padx and pady inside of the frame
        frame_top_ouotput.grid(row=3, column=0, padx=10, pady=5, sticky="nsew")#padx and pady outside of the frame
            
        message_box = Text(frame_top_ouotput, height=34, width=72)
        message_box.grid(row=1, column=0, columnspan=4, padx=10, pady=10, sticky="nsew")
        
        print_data_output()
        
    ###############################