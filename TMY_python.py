# -*- coding: utf-8 -*-
"""
Created on Thu Sep 28 22:21:48 2017

@author: cambonator
"""
import pandas as pd

# https://mpld3.github.io/_downloads/interactive_legend.html

seattle = pd.read_csv('727930TYA_seattle.csv',skiprows=1)
louisville = pd.read_csv('724235TYA_Bowman_Field_Louisville.CSV',skiprows=1)

#seattle.plot('Date (MM/DD/YYYY)','Dry-bulb (C)',kind='line',title='sdfs')

seattle['Temp (F)'] = (9/5 * seattle['Dry-bulb (C)']) + 32
seattle['Day'] = pd.to_datetime(seattle['Date (MM/DD/YYYY)'], format='%m/%d/%Y',infer_datetime_format=True).dt.strftime('%m/%d')

seattle_daily = seattle['Day'].drop_duplicates().to_frame().reset_index()

# need the .values part because indexes do not match
seattle_daily['Max Daily Temp (F)'] = seattle.groupby('Day')['Temp (F)'].max().values
seattle_daily['Min Daily Temp (F)'] = seattle.groupby('Day')['Temp (F)'].max().values
seattle_daily['Mean Daily Temp (F)'] = seattle.groupby('Day')['Temp (F)'].mean().values


seattle_daily = [seattle['Day'].drop_duplicates(), seattle['Max Daily Temp (F)'].drop_duplicates()
    ,seattle['Min Daily Temp (F)'].drop_duplicates(), seattle['Avg Daily Temp (F)'].drop_duplicates()]




# This function takes the TMY3 hourly dataset and turns it into an hourly dataset
def HourlyToDaily(dataset):
    dataset['Temp (F)'] = (9/5 * dataset['Dry-bulb (C)']) + 32
    dataset['Day'] = pd.to_datetime(dataset['Date (MM/DD/YYYY)'], format='%m/%d/%Y').dt.strftime('%m/%d')
    
    dataset_daily = dataset['Day'].drop_duplicates().to_frame().reset_index()
    
    # need the .values part because indexes do not match
    dataset_daily['Max Daily Temp (F)'] = dataset.groupby('Day')['Temp (F)'].max().values
    dataset_daily['Min Daily Temp (F)'] = dataset.groupby('Day')['Temp (F)'].max().values
    dataset_daily['Mean Daily Temp (F)'] = dataset.groupby('Day')['Temp (F)'].mean().values
    return dataset_daily


# Function to compare weather
def CompareWeather(input1,input2,variable):
    compare = input1.merge(input2,on='Day')
    compare.plot(x='Day',y=[variable + '_x',variable + '_y'],kind='line')


CompareWeather(seattle_fun,louisville_fun,'Max Daily Temp (F)')

seattle_fun = HourlyToDaily(seattle)
louisville_fun = HourlyToDaily(louisville)

seattle_fun.set_index(['Day'])
louisville_fun.set_index('Day')


compare = seattle_fun.merge(louisville_fun,on='Day')
compare.set_index(['Day'])
compare.plot(x='Day',y=['Max Daily Temp (F)_x','Max Daily Temp (F)_y'],kind='line')


import matplotlib.pyplot as plt

plt.figure(); compare[['Max Daily Temp (F)_x','Max Daily Temp (F)_y']].plot();