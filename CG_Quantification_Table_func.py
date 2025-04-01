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
                    OptionMenu, DISABLED, NORMAL, BooleanVar, StringVar, Text, END)
import matplotlib.pyplot as plt

def top_CG_Liquid_Qantification():
    top = Toplevel()
    top.title("Quantification table for Photocatalysis experiments -> Liquid")
    top.geometry("640x570+330+60")
    ###############################
    def injected_Volume():
        #return i_vol.get()
        pass

    liquids = ['C2H6O', 'CH3-OH']
    param_liquid_ab = [[0,2.725, 0, 0.01224], [0, 1.694, 0, 0.007]] 
    # A = a + b*Concentration  ::: EtOH-> a=1.7262 ± 0.53297 (area), b=2.72515 ± 0.01224 (area/ppm)
    # A = a + b*Concentration  ::: MeOH-> a=1.40425 ± 0.29079 (area), b=1.69376 ± 0.007 (area/ppm)

    dic_param_liquid_ab = dict(map(lambda i,j : (i,j) , liquids,param_liquid_ab))
    
    def calculo_Concentration_Liquid(liquid, A): # A:Area bajo la curva 
        split = int(split_val_box.get())
        a, b, Da, Db = dic_param_liquid_ab[liquid]  #calibration parameters  a=intercept ::: b=angular coef.
        Concentration_liquid = split*(A-a)/b
        return Concentration_liquid
    
    def calculo_Concentration_Liquid_Error(liquid, A):
        split = int(split_val_box.get())
        a, b, Da, Db = dic_param_liquid_ab[liquid]  #calibration parameters  a=intercept ::: b=angular coef.
        Ds = 0
        DA = 0
        CL = split*(A-a)/b #Concentration_liquid 
        
        DCL = math.sqrt(((A-a)/b)**2*Ds**2 + (split/b)**2*DA**2 + (split/b)**2*Da**2 + ((A-a)*split/b**2)**2*Db**2)
        return DCL
    
    def nothing():pass
        #print(split_val_box.get())
        
    def create_df_concentration_L():
        df_in, x = data_list_L(size)
        df_out = pd.DataFrame(columns=['Measure N°', *liquids], index=range(Ty))
        df_out['Measure N°']=df_in['Measure N°']
        for liquid in liquids:
            for i in range(len(df_in[liquid])):
                df_col_liquid = liquid
                df_val_A = df_in.loc[i, liquid]
                df_out.loc[i,liquid] = calculo_Concentration_Liquid(df_col_liquid, df_val_A)
                #print(calculo_Concentration_Liquid_Error(df_col_liquid, df_val_A))
        return df_out
    
    def print_text_L():
        top_output_L_Tool()
            
    def plot_results_L():
        df = create_df_concentration_L()
        #df = df0.cumsum()
        df.plot(x='Measure N°'); 
        plt.legend(loc='best')
        plt.show()
    
    ###############################
    # Between frame liguid
    inj_param = LabelFrame(top, text="Injection parameters", padx=5, pady=5)#padx and pady inside of the frame
    inj_param.grid(row=0, column=0, padx=10, pady=5, sticky="nsew")#padx and pady outside of the frame

    Label_split_val_box = Label(inj_param, text="Split Value")
    Label_split_val_box.grid(row=0, column=0, columnspan=1, padx=5, sticky="nsew")
    split_val_box = Entry(inj_param)
    split_val_box.insert(0, "10")
    split_val_box.grid(row=1, column=0, pady=5, padx=5, ipady=3, sticky="nsew")
    
    Label_var = Label(inj_param, text="Bool Var free")
    Label_var.grid(row=0, column=1, columnspan=1, padx=5, sticky="nsew")
    var_free = BooleanVar()
    check_carrier_gas = Checkbutton(inj_param, text="", width=5, variable = var_free, command = nothing())
    check_carrier_gas.grid(row=1, column=1, pady=5, columnspan=1)
    ###############################
     
    ###############################
    # Between frame matrix
    frame_matrix_Liquid = LabelFrame(top, text="Insert the values of the areas calculated for each liquid retrieved from the cromatrogram", padx=5, pady=5)#padx and pady inside of the frame
    frame_matrix_Liquid.grid(row=1, column=0, padx=10, pady=5, sticky="nsew")#padx and pady outside of the frame

    lines = [i+1 for i in range(10)]
    Tx=len(liquids)+1
    Ty=len(lines)
    size = Tx*Ty
    my_entries_L = []

    def data_list_L(size):
        data_list = [my_entries_L[i].get() for i in range(size)]
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
            
        df_data_list = pd.DataFrame(list_of_lists, columns =['Measure N°', *liquids], dtype = float) 
        bool_dic_liquids0 = {liquids[i]:bool_liquids[i].get() for i in range(len(liquids))} 
        bool_dic_liquids = {'Measure N°':True}
        bool_dic_liquids.update(bool_dic_liquids0)
        return df_data_list, bool_dic_liquids

    #row loop
    for y in range(Ty+1):
        if y==0:
            for x in range(Tx):
                if x==0:
                    label_cols_L = Label(frame_matrix_Liquid, text='Measure N°')
                    label_cols_L.grid(row=1, column=x, pady=10) 
                else:    
                    label_cols_L = Label(frame_matrix_Liquid, text=liquids[x-1])
                    label_cols_L.grid(row=1, column=x, pady=10)      
        else:
            #column loop
            for x in range(Tx):
                my_entry_L = Entry(frame_matrix_Liquid, width=12)
                if x==0:
                    my_entry_L.insert(0, str(lines[y-1]))
                my_entry_L.grid(row=y+1, column=x, pady=5, padx=5)
                my_entries_L.append(my_entry_L)

    bool_liquids = []
    for x in range(Tx-1):
        var = BooleanVar()
        var.set(True)
        check_liquid = Checkbutton(frame_matrix_Liquid, text="", width=5, 
                                        variable = var, command = nothing())
        check_liquid.grid(row=0, column=x+1, pady=5, columnspan=1)
        bool_liquids.append(var)
    ###############################   

    ###############################
    # Between frame output
    frame_output_L = LabelFrame(top, text="", padx=5, pady=5)#padx and pady inside of the frame
    frame_output_L.grid(row=3, column=0, padx=10, pady=5, sticky="nsew")#padx and pady outside of the frame

    results_L_button = Button(frame_output_L, width=34, text="Click to See Results",
                      font=("", 10), background="#E8E8E8",
                      command=lambda: print_text_L())
    results_L_button.grid(row=0, column=0, padx=10, pady=5,  sticky="nsew")

    plot_L_button = Button(frame_output_L, width=34, text="Click to plot the Results",
                      font=("", 10), background="#E8E8E8",
                      command=lambda: plot_results_L())
    plot_L_button.grid(row=0, column=2, padx=10, pady=5, sticky="nsew")
    ###############################  

    ###############################
    def top_output_L_Tool():
        top2 = Toplevel()
        top2.title("Report of results")
        top2.geometry("635x615+665+60")
        ###############################
        def print_data_output():
            message_box_L.delete('1.0', END)
            #####################################
            data_in, bool_liquids_toPrint = data_list_L(size)
            lista_True_liquids = []
            for key in bool_liquids_toPrint:
                if bool_liquids_toPrint[key]==True:
                    lista_True_liquids.append(key)
            #####################################
            data_out = create_df_concentration_L()
            data_in = data_in[lista_True_liquids]
            data_out = data_out[lista_True_liquids]
            #####################################
            
            text_in = (str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                        +'\n Quantification data for liquid concentration \n'
                        +'\nUsed split = ' + split_val_box.get()+'\n'
                        +'1) The original values of area for each liquid.\n\n')
            text_out = '\n\n2) The concentration of each liquid.\ndata unit = ppm\n\n'
            
            message_box_L.insert('1.0', text_in)
            message_box_L.insert('end', data_in)
            
            message_box_L.insert('end', text_out)
            message_box_L.insert('end', data_out)
            
        ###############################
        # Between frame top_ouotput
        frame_top_ouotput = LabelFrame(top2, text="Calculated concentration of liquids", padx=5, pady=5)#padx and pady inside of the frame
        frame_top_ouotput.grid(row=3, column=0, padx=10, pady=5, sticky="nsew")#padx and pady outside of the frame
            
        message_box_L = Text(frame_top_ouotput, height=34, width=72)
        message_box_L.grid(row=1, column=0, columnspan=4, padx=10, pady=10, sticky="nsew")
        
        print_data_output()
        
    ###############################



#############################################################################################

def top_CG_Gas_Qantification_parameters():
    top = Toplevel()
    top.title("Parameters for analisis of Photocatalysis experiments -> Gas")
    top.geometry("685x115+330+60")
    ###############################

    ###############################
    # Between frame tau, line
    in_tau = 60
    in_Total_time = 300

    frame_tau_line = LabelFrame(top, text="Interval time = interval time between injections", padx=5, pady=5)#padx and pady inside of the frame
    frame_tau_line.grid(row=0, column=0, padx=10, pady=5, sticky="nsew")#padx and pady outside of the frame
     
    Label_tau_box = Label(frame_tau_line, text="Interval time (min)")
    Label_tau_box.grid(row=0, column=0, columnspan=1, padx=5, sticky="nsew")
    tau_box = Entry(frame_tau_line, font=("", 12), width=13)
    tau_box.insert(0, str(in_tau))
    tau_box.grid(row=1, column=0, pady=5, padx=5, ipady=3, sticky="nsew")

    Label_Tt_box = Label(frame_tau_line, text="Total time (min)")
    Label_Tt_box.grid(row=0, column=1, columnspan=1, padx=5, sticky="nsew")
    Tt_box = Entry(frame_tau_line, font=("", 12), width=13)
    Tt_box.insert(0, str(in_Total_time))
    Tt_box.grid(row=1, column=1, pady=5, padx=5, ipady=3, sticky="nsew")
    
    Label_flux_box = Label(frame_tau_line, text="flux (ml/min)")
    Label_flux_box.grid(row=0, column=2, columnspan=1, padx=5, sticky="nsew")
    flux_box = Entry(frame_tau_line, font=("", 12), width=13)
    flux_box.insert(0, str(1))
    flux_box.grid(row=1, column=2, pady=5, padx=5, ipady=3, sticky="nsew")

    # Label_line_box = Label(frame_tau_line, text="Line Number")
    # Label_line_box.grid(row=0, column=2, columnspan=1, padx=5, sticky="nsew")
    # line_box = Entry(frame_tau_line)
    # line_box.insert(0, "2")
    # line_box.grid(row=1, column=2, pady=5, padx=5, ipady=3, sticky="nsew")
    
    lines_names = ['2', '4', '6', '8L', '8S', '8P', '8D', '12']
    select_line = StringVar()
    select_line.set(lines_names[0])
    
    Label_drop_lines = Label(frame_tau_line, text="Line Number")
    Label_drop_lines.grid(row=0, column=3, columnspan=1, padx=5, sticky="nsew")
    
    drop_lines = OptionMenu(frame_tau_line, select_line, *lines_names)
    drop_lines.grid(row=1, column=3, pady=5, padx=5, ipady=3, sticky="nsew")
    
    # Label_carrier_gas = Label(frame_tau_line, text="Is the carrier gas CO2?")
    # Label_carrier_gas.grid(row=0, column=3, columnspan=1, padx=5, sticky="nsew")
    var_carrier_gas = BooleanVar()
    #var_carrier_gas.set(False)
    # check_carrier_gas = Checkbutton(frame_tau_line, text="", width=5, variable = var_carrier_gas, command = nothing())
    # check_carrier_gas.grid(row=1, column=3, pady=5, columnspan=1)
    
    test_button = Button(frame_tau_line, width=18, text="Click to Create Table ",
                      font=("", 10), background="#E8E8E8",
                      command=lambda: top_CG_Gas_Qantification_table())
    test_button.grid(row=0, rowspan=2, column=4, padx=10, pady=5, sticky="nsew")

    ###############################
    
    
    ###############################
    def top_CG_Gas_Qantification_table():
        top = Toplevel()
        top.title("Quantification table for Photocatalysis experiments -> Gas")
        top.geometry("720x550+330+150")
        ###############################
        
        ###############################
        # System parameters
    
        def Vt_value(line):
            D = 0.118 # external D=1/8", internal D = 1.18 mm  :: value in cm
            h = length_of_lines[line]
            vol = math.pi*h*(D/2)**2
            return vol
    
        # Volumes adicionais para o experimento Linha 8D: Vcopo, Vtubo1, Vtubo2  ::: ref Linha 8L
        Vcopo = math.pi*(0.203)*(2.750/2)**2 + math.pi*(0.07)*(2.905/2)**2 - math.pi*(0.203)*(0.2/2)**2 # volume do reator solido
        Vtubo1 = math.pi*(103+97)*(0.14/2)**2 # volume do tubo de cobre
        Vtubo2 = math.pi*(104)*(0.128/2)**2 # volume do tubo de aço entre os dois reatores
        #print(Vcopo , '  :::  ', Vtubo1, '  :::  ', Vtubo2)
        
        length_of_lines = {'2':73, '4':272, '6':121, '8L':298, '8S': 298+90.5, '8P':298+162.5, '12':724+260} # 8H change to 8L
        
        dic_lineas = {'2':Vt_value('2'), '4':Vt_value('4'), '6':Vt_value('6'), '8L':Vt_value('8L'), '8S':Vt_value('8S'), '8P':Vt_value('8P'), '8D':Vt_value('8L')+Vcopo+Vtubo1+Vtubo2, '12':Vt_value('12')}
        
        dic_Vol_reactor = {'2':100.9, '4':100.9, '6':100.9, '8L':100.9, '8S':4, '8P':1, '8D':100.9, '12':75}# Volume do reator, ml 
    
        dic_Vol_sol = {'2':30, '4':30, '6':30, '8L':30, '8S':0, '8P':0, '8D':30, '12':40}# Volume da solução , ml 
    
        gases = ['CO', 'CH4', 'C2H6', 'O2', 'H2', 'CO2', 'N2']
        
        #parametros do H2 atualizados em 26-03-2025: de [0,3198] para [0,1127.055]
        #parametros do O2 atualizados em 01-04-2025: de [0,254] para [0,153.2743]
        #parametros do N2 atualizados em 01-04-2025: de [1,1] para [0,117.5914]
            
        parametros_ab = [[0,59292],[0,55129],[0,132900],[0,153.2743],[0,1127.055],[0,232.973], [0,117.5914]]#For N2 a and b parameters does not have any meaning
        # for O2 [4.8,254] --- [0,254] because negative values
        dic_parametros_ab = dict(map(lambda i,j : (i,j) , gases,parametros_ab))
    
        ###############################
    
        def get_parameters(df_col, df_val, t):
            #tau = int(tau_box.get())
            line = select_line.get()
            gas = df_col
            A = df_val
            flux = int(flux_box.get())
            #print(flux)
            return line, gas, A, t, flux
        
        def factor_O2_N2():
            A0O, slope_O = dic_parametros_ab['O2']
            A0N, slope_N = dic_parametros_ab['N2']
            #print((slope_O/slope_N)*0.25)
            return (slope_O/slope_N)*(0.21/0.78)
            
        def calculo_Evolution_gas(line, gas, A, t, flux, A_N2=0): # A:Area bajo la curva :: tau: tempo entre coletas, min :: 
            A0, b = dic_parametros_ab[gas]  #calibration parameters  a=intercept -- area ::: b=angular coef -- area/(umol/ml).
    
            Vr = dic_Vol_reactor[line] # Volume do reator, ml  ::: padrão para liquido 100.9 ml 
            
            Vs = dic_Vol_sol[line] # Volume da solução , ml 
            
            Vt = dic_lineas[line] #Vt: line volume, ml  ::: volume de tubulação, ml
            
            Vl = 1 # Volume do loop, ml
            
            #f = 1.0 # fluxo, ml/min
            
            Area = A-(factor_O2_N2()*A_N2)# in calibration Volume of O2 20% and volume of N2 80% of the injected
    
            Evolution_gas = ((Area-A0)/b)*(Vr-Vs+Vt+Vl+(t*flux))
            
            return Evolution_gas
    
        def create_df_evolution():
            df_in, x = data_list(size)
            df_out = pd.DataFrame(columns=['time(min)', *gases], index=range(Ty))
            df_out['time(min)']=df_in['time(min)']
            for gas in gases[:-1]: # disregards N2
                for i in range(len(df_in[gas])):
                    df_col = gas
                    df_val = df_in.loc[i,gas]
                    if i==0:
                        t = 0
                    else: 
                        t=int(tau_box.get())
                    Vt, gas, A, t, flux = get_parameters(df_col, df_val, t) 
                    if gas=='O2':
                        A_N2 = df_in.loc[i,'N2']
                        df_out.loc[i,gas] = calculo_Evolution_gas(Vt, gas, A, t, flux, A_N2)
                    else:
                        df_out.loc[i,gas] = calculo_Evolution_gas(Vt, gas, A, t, flux)
            return df_out
        
        def create_df_evolution_CO2_carrier():
            df_in, x = data_list(size)
            df_out = pd.DataFrame(columns=['time(min)', *gases], index=range(Ty))
            df_out['time(min)']=df_in['time(min)']
            for gas in gases[:-1]: # disregards N2
                if gas=='CO' or gas=='CH4': #or ...
                    for i in range(len(df_in[gas])):
                        df_col = gas
                        df_val = df_in.loc[i,gas]
                        if i==0:
                            t = 0
                            Vt, gas, A, t, flux = get_parameters(df_col, df_val, t) 
                            gas0 = calculo_Evolution_gas(Vt, gas, A, t, flux)
                        else: 
                            t=int(tau_box.get())
                        Vt, gas, A, t, flux = get_parameters(df_col, df_val, t) 
                        df_out.loc[i,gas] = calculo_Evolution_gas(Vt, gas, A, t, flux)-gas0
                else:
                    for i in range(len(df_in[gas])):
                        df_col = gas
                        df_val = df_in.loc[i,gas]
                        if i==0:
                            t = 0
                        else: 
                            t=int(tau_box.get())
                        Vt, gas, A, t, flux = get_parameters(df_col, df_val, t) 
                        if gas=='O2':
                            A_N2 = df_in.loc[i,'N2']
                            df_out.loc[i,gas] = calculo_Evolution_gas(Vt, gas, A, t, flux, A_N2)
                        else:
                            df_out.loc[i,gas] = calculo_Evolution_gas(Vt, gas, A, t, flux)
            return df_out
    
        def print_text():
            top_output_Tool()
            #print('check_carrier_gas = ', var_carrier_gas.get())
                
        def plot_results():
            df0 = create_df_evolution()
            df = df0.cumsum()
            df['time(min)'] = df0['time(min)']
            df.plot(x='time(min)'); 
            plt.legend(loc='best')
            plt.show()
            
        
        def nothing():
            pass
    
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
            bool_dic_gases0 = {gases[i]:bool_gases[i].get() for i in range(len(gases))} 
            bool_dic_gases = {'time(min)':True}
            bool_dic_gases.update(bool_dic_gases0)
            return df_data_list, bool_dic_gases
    
        #row loop
        for y in range(Ty+1):
            if y==0:
                for x in range(Tx):
                    if x==0:
                        label_cols = Label(frame_matrix, text='time (min)')
                        label_cols.grid(row=1, column=x, pady=10) 
                    else:    
                        label_cols = Label(frame_matrix, text=gases[x-1])
                        label_cols.grid(row=1, column=x, pady=10)      
            else:
                #column loop
                for x in range(Tx):
                    my_entry = Entry(frame_matrix, width=12)
                    if x==0:
                        my_entry.insert(0, str(times[y-1]))
                    my_entry.grid(row=y+1, column=x, pady=5, padx=5)
                    my_entries.append(my_entry)
                    
        
        bool_gases = []
        for x in range(Tx-1):
            var = BooleanVar()
            var.set(True)
            check_gas = Checkbutton(frame_matrix, text="", width=5, 
                                            variable = var, command = nothing())
            check_gas.grid(row=0, column=x+1, pady=5, columnspan=1)
            bool_gases.append(var)
        ###############################   
    
        ###############################
        # Between frame output
        frame_output = LabelFrame(top, text="", padx=5, pady=5)#padx and pady inside of the frame
        frame_output.grid(row=3, column=0, padx=10, pady=5, sticky="nsew")#padx and pady outside of the frame
    
        results_button = Button(frame_output, width=39, text="Click to See Results",
                          font=("", 10), background="#E8E8E8",
                          command=lambda: print_text())
        results_button.grid(row=0, column=0, padx=10, pady=5,  sticky="nsew")
    
        plot_button = Button(frame_output, width=39, text="Click to plot the Results",
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
                #####################################
                data_in, bool_gases_toPrint = data_list(size)
                lista_True_gas = []
                for key in bool_gases_toPrint:
                    if bool_gases_toPrint[key]==True:
                        lista_True_gas.append(key)
                #####################################
                if var_carrier_gas.get()==True:
                    data_out = create_df_evolution_CO2_carrier()
                else:
                    data_out = create_df_evolution()
                data_in = data_in[lista_True_gas]
                data_out = data_out[lista_True_gas]

                data_out_acc = data_out.cumsum()
                data_out_acc['time(min)'] = data_out['time(min)']
                #####################################
                
                text_in = (str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                            +'\n Quantification data for line Number '+ select_line.get() +'\n'
                            +'1) The original values of area for each gas.\n\n')
                text_out = '\n\n2) The quantity of each gas for the corresponding interval of time.\ndata unit = umol\n\n'
                text_out_acc = '\n\n3) The accumulated quantity of each gas in the corresponding time.\ndata unit = umol\n\n'
                
                message_box.insert('1.0', text_in)
                message_box.insert('end', data_in.to_string(index=False))
                
                
                message_box.insert('end', text_out)
                message_box.insert('end', data_out.to_string(index=False))
                
                message_box.insert('end', text_out_acc)
                message_box.insert('end', data_out_acc.to_string(index=False))
            ###############################
            # Between frame top_ouotput
            frame_top_ouotput = LabelFrame(top2, text="Calculated amount of gases", padx=5, pady=5)#padx and pady inside of the frame
            frame_top_ouotput.grid(row=3, column=0, padx=10, pady=5, sticky="nsew")#padx and pady outside of the frame
                
            message_box = Text(frame_top_ouotput, height=34, width=72)
            message_box.grid(row=1, column=0, columnspan=4, padx=10, pady=10, sticky="nsew")
            
            print_data_output()
            