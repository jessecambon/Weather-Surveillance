# -*- coding: utf-8 -*-
"""
Created on Sat Sep 30 09:36:29 2017

@author: cambonator
"""

import pylab as plot
import pandas as pd


# Change plot parameters
params = { 'legend.fontsize': 25,
          'font.size': 15,
          'axes.titlesize' : 25,
          'axes.labelsize' : 25
          }
plot.rcParams.update(params)

# To see plot parameters
#plot.rcParams.keys()

# https://mpld3.github.io/_downloads/interactive_legend.html
# https://pandas.pydata.org/pandas-docs/stable/visualization.html
# http://mpld3.github.io/
# https://scrapy.org/

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
    
    imported_file['Heat Index (F)'] = -42.379 + 2.04901523*imported_file['Dry Bulb Temperature (F)']
    + 10.14333127*imported_file['Relative Humidity'] - .22475541*imported_file['Dry Bulb Temperature (F)']*imported_file['Relative Humidity'] 
    - .00683783*imported_file['Dry Bulb Temperature (F)']**2 - .05481717*imported_file['Relative Humidity'] **2 
    + .00122874*imported_file['Dry Bulb Temperature (F)']**2*imported_file['Relative Humidity'] 
    + .00085282*imported_file['Dry Bulb Temperature (F)']*imported_file['Relative Humidity'] **2 
    - .00000199*imported_file['Dry Bulb Temperature (F)']**2*imported_file['Relative Humidity']**2
    # Source: http://www.wpc.ncep.noaa.gov/html/heatindex_equation.shtml
    
    # Convert Wind speed to mph
    imported_file['Wind Speed (mph)'] = 2.23694 * imported_file['Wind Speed']
    
    imported_file['Wind Chill'] = 35.74 + (0.6215 * imported_file['Dry Bulb Temperature (F)'])
    - (35.75 * imported_file['Wind Speed (mph)']**0.16)  \
    + (0.4275 * imported_file['Dry Bulb Temperature (F)'] * imported_file['Wind Speed (mph)']**0.16 )
    # Source: https://www.weather.gov/media/epz/wxcalc/windChill.pdf
    
    #### COMMENTED THIS OOUT FOR NOW BECAUSE OF ERROR:
    # ValueError: day is out of range for month
    # when iterating through all cities and finding max temp
    
    # Create daily date key (does not include year) for easy graphing
    #imported_file['Date'] = pd.to_datetime((imported_file['Month'].apply(str) + '/' + imported_file['Day'].apply(str)),format='%m/%d',dayfirst=True).dt.strftime('%m/%d')
    
    return imported_file


def HourlyToDaily(dataset,variable_list,key):
      
    dataset_daily = dataset[key].drop_duplicates().to_frame().reset_index()
    
    for variable in variable_list:
    # need the .values part because indexes do not match
        dataset_daily['Max ' + variable] = dataset.groupby(key)[variable].max().values
        dataset_daily['Min ' + variable] = dataset.groupby(key)[variable].max().values
        dataset_daily['Mean ' + variable] = dataset.groupby(key)[variable].mean().values
        dataset_daily['Total ' + variable] = dataset.groupby(key)[variable].sum().values
        
    return dataset_daily


# Plots metrics from two different weather files against each other
def CompareWeather(input1,input2,name1,name2,variable,key):
   # I renamed the variable to force the label on the plot for now
    compare = input1.merge(input2,on=key).rename(columns={variable + '_x': name1,
                            variable + '_y': name2                       
            })
   # print(compare.dtypes)
    compare.plot(x=key,y=[name1,name2],kind='line',figsize=(16,9),title=variable)


# Import CSV
nairobi = ImportFile('KEN_Nairobi-Wilson.637420_SWERA.epw')
inchon = ImportFile('KOR_Inchon.471120_IWEC.epw')

# These are quantities I am interested in
Analysis_Var_List = ['Dry Bulb Temperature (F)', 'Heat Index (F)', 'Wind Speed (mph)',
        'Relative Humidity','Wind Chill','Liquid Precipitation Depth',
     'Liquid Precipitation Rate']

# Convert to Daily Data
nairobi_daily = HourlyToDaily(nairobi,
   Analysis_Var_List,'Date')

inchon_daily = HourlyToDaily(inchon,
    Analysis_Var_List,'Date')

# Exports
#nairobi_daily.to_csv('nairobi_daily.csv') # Export Data to CSV
#inchon_daily.to_csv('inchon_daily.csv') # Export Data to CSV


# Compare
CompareWeather(inchon_daily,nairobi_daily,'Inchon','Nairobi','Max Dry Bulb Temperature (F)','Date')
CompareWeather(inchon_daily,nairobi_daily,'Inchon','Nairobi','Min Dry Bulb Temperature (F)','Date')
CompareWeather(inchon_daily,nairobi_daily,'Inchon','Nairobi','Mean Dry Bulb Temperature (F)','Date')
CompareWeather(inchon_daily,nairobi_daily,'Inchon','Nairobi','Max Wind Speed (mph)','Date')
CompareWeather(inchon_daily,nairobi_daily,'Inchon','Nairobi','Max Wind Chill','Date')
CompareWeather(inchon_daily,nairobi_daily,'Inchon','Nairobi','Max Heat Index (F)','Date')
CompareWeather(inchon_daily,nairobi_daily,'Inchon','Nairobi','Mean Relative Humidity','Date')





# Loop through files to calculate max temp etc..


subfolder = 'Weather Files'
# Loop through files
dataframe_collection = {}
# Initialize
City_List = pd.DataFrame(columns=['City','Max Temp']) # Create empty dataframe

#City_List.append(['blah',123])

### Iterate through all cities and find max temperature

import os
for filename in os.listdir('./' + subfolder):
    #print('./' + subfolder + '/' + filename)
    
    dataframe_collection[filename] = ImportFile('./' + subfolder + '/' + filename)
    
    print(filename)
    
    a = pd.DataFrame([[filename,dataframe_collection[filename]['Dry Bulb Temperature (F)'].max()]],columns=['City','Max Temp'])
    City_List = City_List.append(a)
  
    
    #if i == 5:
    #    break
    
# Top 10 cities by temperature
City_List.set_index('City')['Max Temp'].sort_values(ascending=False).head(20)

 
dataframe_collection['USA_IA_Carroll.Muni.AP.725468_TMY3.epw'].to_csv('USA_IA_Carroll_muy_caliente.csv')


#for i in (1,2,3):
#    dataframe_collection[i] = ImportFile('./' + subfolder + '/' + filename)



# There variables are missing
#CompareWeather(inchon_daily,nairobi_daily,'Total Liquid Precipitation Depth','Date')
#CompareWeather(inchon_daily,nairobi_daily,'Total Liquid Precipitation Rate','Date')
#CompareWeather(inchon_daily,nairobi_daily,'Total Snow Depth','Date')
