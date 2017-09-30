# -*- coding: utf-8 -*-
"""
Created on Sat Sep 30 17:03:29 2017

@author: cambonator
"""
import os 

# Extract locations from files to build index

subfolder = 'Weather Files'

def ExtractCityInfo(filename,subfolder):
    with open('./' + subfolder + '/' + filename, 'r') as f:
        first_line = f.readline().split(',')
        city = first_line[1]
        country_code = first_line[3]
        lat = first_line[6]
        long = first_line[7] 
        print('Filename:' + filename)
        print('city: ' + city)
        print('country_code: ' + country_code)
        print('lat: ' + lat)
        print('long: ' + long)
        print('-------------------')
    
        return pd.DataFrame([[city,country_code,filename,lat,long]],
            columns=['City','Country Code','Filename','Lat','Long'])
        
 # initialize empty dataframe
 # Not very computationally efficient but whatever
 Index = pd.DataFrame(columns=['City','Country Code','Filename','Lat','Long']) # Create empty dataframe
 for filename in os.listdir('./' + subfolder):
    a = ExtractCityInfo(filename,subfolder)
    Index = Index.append(a)
    #print(filename)
    
Index.to_csv('Index.csv')

filename='KEN_Meru.636950_SWERA.epw'

a = ExtractCityInfo('BGD_Rangpur.418590_SWERA.epw','Weather Files')
b = ExtractCityInfo('CHN_Anhui.Bengbu.582210_CSWD.epw','Weather Files')

    