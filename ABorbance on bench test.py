# -*- coding: utf-8 -*-
"""
Created on Thu Dec 21 16:07:19 2023

@author: amaitland
"""

# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import os
import pandas as pd
import glob
import matplotlib.pyplot as plt

def extract_numbers(file):
    filename = os.path.splitext(os.path.basename(file))[0]  # Extract filename without extension
    last_numbers = filename[-5:]  # Get the last 5 characters from the filename
    return last_numbers
# Function to process each file
def process_file(file):
    # Read the file skipping first 13 rows and extracting two columns
    data = pd.read_csv(file, skiprows=13, delimiter='\s+', header=None, usecols=[0, 1])
    
    # Assign column names
    data.columns = ['Wavelength', 'Absorbance']
    
    # Define wavelength ranges
    ranges = {
        'Peak 1': (300, 400)
    }
    
    # Calculate maximum absorbance values within specified ranges
    max_values = {}
    for peak, (start, end) in ranges.items():
        peak_range = data[(data['Wavelength'] >= start) & (data['Wavelength'] <= end)]
        max_value = peak_range['Absorbance'].max()
        max_values[peak] = max_value
    
    return max_values

# Folder containing text files
folder_path = 'C:\\Users\\Athira\\Desktop\\2024- Spectroelectro\\300124\\Spectroelectro\\Ba growth- 1st cycle (0.1-0.4V)/*.txt'  # Update with your folder path

# Get a list of text files in the folder
files = glob.glob(folder_path)

# Prepare the CSV file to store results
csv_data = {'LastNumbers': [], 'Filename': []}
for peak in ['Peak 1']:
    csv_data[peak] = []

# Process each file and store results in CSV
for file in files:
    last_numbers = extract_numbers(file)  # Extract last 5 numbers from file name
    max_values = process_file(file)
    
    # Store max values in csv_data
    csv_data['LastNumbers'].append(last_numbers)
    csv_data['Filename'].append(file)
    for peak, value in max_values.items():
        csv_data[peak].append(value)

# Convert the dictionary to a DataFrame
result_df = pd.DataFrame(csv_data)

# Save the results to a CSV file
result_df.to_csv('1stcycle20240213.csv', index=False)

data = pd.read_csv('1stcycle20240213.csv')

# Prepare the data for plotting
x = data['LastNumbers']  # X-axis data from 'LastNumbers' column
y1 = data['Peak 1']  # Y-axis data for Peak 1
#y2 = data['Peak 2']  # Y-axis data for Peak 2
#y3 = data['Peak 3']  # Y-axis data for Peak 3

# Plotting the data
plt.figure(figsize=(10, 6))  # Set the size of the figure

# Scatter plots for each series with different colors
plt.scatter(x, y1, label='Range 300 to 400 nm', color='red', marker='o')
#plt.scatter(x, y2, label='Range 600 to 650 nm', color='blue', marker='x')
#plt.scatter(x, y3, label='Range 650 to 700 nm', color='green', marker='^')

# Set plot title and labels
plt.title( 'Peak Absorbances for 1st cycle')
plt.xlabel('Run cycle number')
plt.ylabel('Absorbance')

# Show legend
plt.legend()

#plt.savefig('UVVIS_0.1V_5min.pdf', format='pdf')

# Show the plot
plt.grid(True)
plt.show()