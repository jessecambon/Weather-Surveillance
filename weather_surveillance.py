# -*- coding: utf-8 -*-
"""
Created on Sat Sep 30 09:36:29 2017

@author: cambonator
"""


import pandas as pd

# https://mpld3.github.io/_downloads/interactive_legend.html

# This function takes a hourly weather dataset and turns it into a daily dataset
# dataset is the pandas dataframe name
# variable is the value we want to calculate daily values for
# key needs to give us a unique day

def ImportFile(filename):
   
    imported_file = pd.read_csv(filename,skiprows=8,header=None)
    
    imported_file.columns =['Year', 'Month', 'Day', 'Hour', 'Minute', 'Data Source and Uncertainty Flags',
     'Dry Bulb Temperature','Dew Point Temperature', 'Relative Humidity', 'Atmospheric Station Pressure',
     'Extraterrestrial Horizontal Radiation', 'Extraterrestrial Direct Normal Radiation',
     'Horizontal Infrared Radiation Intensity', 'Global Horizontal Radiation',
     'Direct Normal Radiation', 'Diffuse Horizontal Radiation',
     'Global Horizontal Illuminance', 'Direct Normal Illuminance',
     'Diffuse Horizontal Illuminance', 'Zenith Luminance', 'Wind Direction',
     'Wind Speed', 'Total Sky Cover', 'Opaque Sky Cover (used if Horizontal IR Intensity missing)',
     'Visibility', 'Ceiling Height', 'Present Weather Observation',
     'Present Weather Codes', 'Precipitable Water', 'Aerosol Optical Depth',
     'Snow Depth', 'Days Since Last Snowfall', 'Albedo', 'Liquid Precipitation Depth',
     'Liquid Precipitation Rate']
    
    # Convert Temp to Fahrenheit
    imported_file['Dry Bulb Temperature (F)'] = (9/5 * imported_file['Dry Bulb Temperature']) + 32
    
    # Create daily date key (does not include year) for easy graphing
    imported_file['Date'] = pd.to_datetime((imported_file['Month'].apply(str) + '/' + imported_file['Day'].apply(str)),format='%m/%d').dt.strftime('%m/%d')
    
    return imported_file



def HourlyToDaily(dataset,variable,key):
      
    dataset_daily = dataset[key].drop_duplicates().to_frame().reset_index()
    
    # need the .values part because indexes do not match
    dataset_daily['Max ' + variable] = dataset.groupby(key)[variable].max().values
    dataset_daily['Min ' + variable] = dataset.groupby(key)[variable].max().values
    dataset_daily['Mean ' + variable] = dataset.groupby(key)[variable].mean().values
    return dataset_daily


def CompareWeather(input1,input2,variable,key):
    compare = input1.merge(input2,on=key)
    compare.plot(x=key,y=[variable + '_x',variable + '_y'],kind='line')


# Import CSV
nairobi = ImportFile('KEN_Nairobi-Wilson.637420_SWERA.epw')
inchon = ImportFile('KOR_Inchon.471120_IWEC.epw')

# Convert to Daily Data
nairobi_daily = HourlyToDaily(nairobi,'Dry Bulb Temperature (F)','Date')
inchon_daily = HourlyToDaily(inchon,'Dry Bulb Temperature (F)','Date')

# Compare
CompareWeather(inchon_daily,nairobi_daily,'Max Dry Bulb Temperature (F)','Date')
