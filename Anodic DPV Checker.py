# -*- coding: utf-8 -*-
"""
Created on Tue Dec 26 17:07:21 2023

@author: Adam Maitland
"""

import os
import pandas as pd
import matplotlib.pyplot as plt

def extract_number(file_name):
    # Assuming the number is separated by '_' and before '.txt'
    parts = file_name.split('_')
    if len(parts) >= 2:
        number_str = parts[-1].split('.txt')[0]
        try:
            return float(number_str)
        except ValueError:
            return None
    return None


def process_files(folder_path):
    data = []
    files = os.listdir(folder_path)
    
    peak_1_currents = []
    peak_2_currents = []
    peak_1_voltages = []
    peak_2_voltages = []
    file_names = []
    file_numbers = []
    
    for file_name in files:
        if file_name.endswith('.txt'):
            file_path = os.path.join(folder_path, file_name)
            with open(file_path, 'r') as file:
                # Skip first 22 lines
                for _ in range(33):
                    next(file)
                    
                lines = file.readlines()
                voltages = []
                currents = []
                for line in lines:
                    voltage, current = map(float, line.strip().split(','))
                    voltages.append(voltage)
                    currents.append(current)

                df = pd.DataFrame({'Voltage': voltages, 'Current': currents})

                peak_1_data = df[(df['Voltage'] >= -0.1) & (df['Voltage'] <= 0.3 )]
                peak_2_data = df[(df['Voltage'] >= -0.6) & (df['Voltage'] <= -0.3)]

                peak_1_voltage = peak_1_data.loc[peak_1_data['Current'].idxmax(), 'Voltage']
                peak_2_voltage = peak_2_data.loc[peak_2_data['Current'].idxmax(), 'Voltage']

                peak_1_current = peak_1_data['Current'].max()
                peak_2_current = peak_2_data['Current'].max()
                
                file_number = extract_number(file_name)

                data.append({'File': file_name,
                             'Peak_1_Current': peak_1_current, 'Peak_1_Voltage': peak_1_voltage,
                             'Peak_2_Current': peak_2_current, 'Peak_2_Voltage': peak_2_voltage,
                             'FRU Conc mM': file_number})
                
                # Storing data for plotting
                peak_1_currents.append(peak_1_current)
                peak_2_currents.append(peak_2_current)
                peak_1_voltages.append(peak_1_voltage)
                peak_2_voltages.append(peak_2_voltage)
                file_names.append(file_name)
                file_numbers.append(file_number)

    result_table = pd.DataFrame(data)
    
    result_table.to_csv('DA_FRU_20230209.csv', index=False)
    
    
    plt.figure(figsize=(10, 6))
    plt.scatter(file_numbers, peak_1_currents, marker='o', linestyle='-', label='Peak 1 Current')
    plt.scatter(file_numbers, peak_2_currents, marker='o', linestyle='-', label='Peak 2 Current')
    plt.xlabel('File Number')
    plt.ylabel('Current')
    plt.title('Anodic Peak Currents vs Fru Conc in mM')
    plt.legend()
    plt.tight_layout()
    plt.savefig('DA_FRU_Graph_an_20240309.pdf')
    plt.show()
    
    
    return result_table

# Save the result to a CSV file
folder_path = 'D:\\Experimental Files\\20240209\\Da + FRU\\Anodic files'
result = process_files(folder_path)
