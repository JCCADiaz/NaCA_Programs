# -*- coding: utf-8 -*-
"""
Created on Thu Jan 25 11:40:38 2024

@author: jccad
"""

from tkinter import (LabelFrame, Entry, Button, Toplevel, Label, Text, END)

import math
import numpy as np
import periodictable as PTab


def top_Reagent_Calculation():
    top = Toplevel()
    top.title("Reagent Calculation")
    top.geometry("498x750+330+60")
    
    def atomic_weight(symbol):
        el_mass = [el.mass for el in PTab.elements if el.symbol==symbol][0]
        return el_mass
    
    def m_Molar(list1, list2): # list1 = elements ; list2 = coefficients
        list1 = [atomic_weight(i) for i in list1]
        m_Molar = sum(list(map(lambda x,y:x*y,list1,list2)))
        return m_Molar
    
    def Number_mol(list1, list2, mass): # number of mol in the required mass ::  list1 = elements ; list2 = coefficients
        m_mol = m_Molar(list1, list2)
        Number_mol = mass/m_mol
        return Number_mol
    
    def include_reagents(material, reagents):
        if material not in material_reagents:
            material_reagents[material] = reagents
            
    def material_To_lists(material):
        material = material.split(' ')
        material_elements = []
        material_coeffs = []
        for mat in material:
            if '.' in mat:
                element = mat[:mat.find('.')-1]
                coeff = float(mat[mat.find('.')-1:])
            elif not '.' in mat and mat[-1].isdigit() and len(mat)>=2 and not mat[-2:].isdigit():
                element = mat[:-1]
                coeff = int(mat[-1])
            elif not '.' in mat and len(mat)>2 and mat[-2].isdigit():
                element = mat[:-2]
                coeff = int(mat[-2:])              
            else:
                element = mat
                coeff = 1
            
            material_elements.append(element)
            material_coeffs.append(coeff)
        return material_elements, material_coeffs
    
    def proportion_values(material, reagents=[]):
        reagents = material_reagents[material]
        material_elements, material_coeffs = material_To_lists(material)
        
        material = material.split(' ')
        proportion_values = {}
        
        for el in material_elements[:-1]:
            for reag in reagents:
                reag_elements, reag_coeffs = material_To_lists(reag)
                if el in reag_elements:
                    proportion = material_coeffs[material_elements.index(el)]/reag_coeffs[reag_elements.index(el)]
                    proportion_values[reag] = proportion
        return proportion_values
        
        
    def reagents_masses(material, reagents=[], required_mass=1): # material = chemical formula with spaces ::: ex: 'Sr Ti O3'
                                                                # leave the oxygen at the end of the formula
        material_elements, material_coeffs = material_To_lists(material)
        material_num_mol = Number_mol(material_elements, material_coeffs, required_mass)
        
        include_reagents(material, reagents)
        reagents = material_reagents[material]
        
        #calculates the stoichiometric proportions between material and reagents
        prop_val = proportion_values(material) 
        
        reagents_masses = {}
    
        for reag in reagents:
            reag_elements, reag_coeffs = material_To_lists(reag)
            massa_molar = m_Molar(reag_elements, reag_coeffs)       
            reagents_masses[reag] = prop_val[reag]*massa_molar*material_num_mol
        return reagents_masses
    
    def output(material, reagents=[], required_mass=1):
        message_box.delete('1.0', END)
        
        dic_masses = reagents_masses(material, reagents, required_mass)
        
        # print(f' :::  preparation of {material}  ::: \n')
        # print(f'- Quantity of {material} to be prepared: {required_mass} g\n')
        
        message_box.insert('1.0', f' :::  preparation of {material}  ::: \n')
        message_box.insert('end', f'\nQuantity of {material} to be prepared: {required_mass} g\n')
        
        material_elem, material_elemcoeff= material_To_lists(material)
        material_elem1 = [atomic_weight(i) for i in material_elem]
        # Print the names of the columns.
        # print("|{:<10} |{:<10}|".format('Element', 'atomic_weight (g/mol)'))
        message_box.insert('end', "\n|{:<10} {:<10}|".format('Element', 'atomic_weight (g/mol)'))
        
        # print each data item.
        for i in range(len(material_elem)):
            # print('-----------------------------------')
            # print("|{:<10} |{:<21}|".format(material_elem[i], round(material_elem1[i], 5)))
            message_box.insert('end','\n-----------------------------------')
            message_box.insert('end',"\n|{:<10} {:<21}|".format(material_elem[i], round(material_elem1[i], 5)))
        
        # Print the names of the columns.
        # print("\n\n|{:<10} |{:<10}|".format('Reagent', 'mass (g)'))
        message_box.insert('end',"\n\n|{:<10} {:<10}|".format('Reagent', 'mass (g)'))
        # print each data item.
        for key, value in dic_masses.items():
            # print('------------------------')
            # print("|{:<10} |{:<10}|".format(key, round(value, 5)))
            message_box.insert('end', '\n------------------------')
            message_box.insert('end', "\n|{:<10} {:<10}|".format(key, round(value, 5)))
    
    # material = 'Bi0.5 Na0.5 Ti O3' # material to be prepared, separed by spaces ::: ex: 'Sr Ti O3'
    # reagents = ['Bi2 O3', 'Na2 C O3', 'Ti O2'] #reagents to prepara the material, separed by spaces ::: ex: 'Ti O2', If it exists on the list, leave it empty
    # Bi2 O3,Na2 C O3,Ti O2
    # required_mass = 10 # desired quantity of material, in g
    
    ###############################
    material_reagents = {'Sr Ti O3': ['Sr C O3', 'Ti O2']} # dictionary to be completed as needed
    
    def get_boxes():
        mat_box = material_box.get()
        reag_box = reagents_box.get()
        
        if reag_box!='':
            reag_box = reag_box.split(',')
            
            for i in range(len(reag_box)):
                while True:
                    if reag_box[i][0]==' ':
                        reag_box[i] = reag_box[i][1:]
                    else: break
                while True:
                    if reag_box[i][-1]==' ':
                        reag_box[i] = reag_box[i][:-1]
                    else: break
        return mat_box, reag_box
    
    def Print_resultados():
        mat_box, reag_box = get_boxes()
        required_mass = float(mass_box.get())
        output(mat_box, reag_box, required_mass)
    
    ###############################
    # Between frame frame_material
    frame_material = LabelFrame(top, text="Write chemical formulas with spaces, ex: Sr Ti O3", padx=5, pady=5)#padx and pady inside of the frame
    frame_material.grid(row=0, column=0, padx=10, pady=5, sticky="nsew")#padx and pady outside of the frame
    
    Label_material_box = Label(frame_material, text="Material to be prepared:")
    Label_material_box.grid(row=1, column=1, columnspan=1, padx=5, sticky="nsew")
    material_box = Entry(frame_material, width=41)
    material_box.grid(row=1, column=2, pady=5, padx=5, ipady=3, sticky="nsew")
    
    
    Label_reagents_box = Label(frame_material, text="Necessary reagents:\n(Write chemical formulas separated\nby comma, ex: Sr C O3, Ti O2)")
    Label_reagents_box.grid(row=2, column=1, columnspan=1, padx=5, sticky="nsew")
    reagents_box = Entry(frame_material)
    reagents_box.grid(row=2, column=2, pady=5, padx=5, ipady=3, sticky="nsew")
    
    Label_mass_box = Label(frame_material, text="Desired quantity of Material (in g):")
    Label_mass_box.grid(row=3, column=1, columnspan=1, padx=5, sticky="nsew")
    mass_box = Entry(frame_material)
    mass_box.grid(row=3, column=2, pady=5, padx=5, ipady=3, sticky="nsew")
    ###############################
    
    ###############################
    # Between frame frame_amount_Reagentes
    frame_amount_Reagentes = LabelFrame(top, text="Run this cell to calculate the amount of reagents", padx=5, pady=5)#padx and pady inside of the frame
    frame_amount_Reagentes.grid(row=1, column=0, padx=10, pady=5, sticky="nsew")#padx and pady outside of the frame
    
    message_box = Text(frame_amount_Reagentes, height=30, width=55)
    message_box.grid(row=1, column=0, columnspan=1, padx=10, pady=10, sticky="nsew")
    
    results_button = Button(frame_amount_Reagentes, text="Click to See Results",
                      font=("", 10), background="#E8E8E8",
                      command=lambda: Print_resultados())
    results_button.grid(row=0, column=0, pady=5, columnspan=1, sticky="nsew")
    ###############################