from bs4 import BeautifulSoup
#import urllib.request
import requests
import pandas as pd
import re

# This program downloads all our Weather File Data to A Subfolder


root = 'https://energyplus.net'


import shutil
 

# WARNING - This function gives me messed up garbled files right now
def download_file(url,subfolder_name):
    local_filename = url.split('/')[-1]
    r = requests.get(url, stream=True)
    with open('./' + subfolder_name + '/' + local_filename, 'wb') as f:
        #r.raw.decode_content = True 
        shutil.copyfileobj(r.text, f)
 
    return local_filename


        
# Deprecated --- very slow
# Downloads a file from a given URL to a specified subfolder            
def download_file_old(url,subfolder_name):
    local_filename = url.split('/')[-1]
    # NOTE the stream=True parameter
    r = requests.get(url, stream=True)
    with open('./' + subfolder_name + '/' + local_filename, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024*1024): 
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)
                #f.flush() commented by recommendation from J.F.Sebastian
    return local_filename            


# Scrape the index of a given page
# Return a list of the links
def scrape_links(url):
    print('Scraping ' + url)
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    
    # Select the given div
    data = soup.findAll("div", { "class" : "btn-group-vertical" })
    
    list_links = [] #initialize
    for div in data:
        links = div.findAll('a')
        for a in links:
            list_links.append(a['href'])
       # print(list_links)
    return list_links

# test
#download_file('https://energyplus.net/weather-location/africa_wmo_region_1/EGY//EGY_Asyut.623930_ETMY/weather-download/africa_wmo_region_1/EGY//EGY_Asyut.623930_ETMY/EGY_Asyut.623930_ETMY.epw','Test Files')


scrape_links('https://energyplus.net/weather-region/north_and_central_america_wmo_region_4')


scrape_links(root + '/weather-region/north_and_central_america_wmo_region_4/USA%20%20')

# Initialize index
Index = pd.DataFrame(columns=['Region','Country','City','Filename']) # Create empty dataframe
    

# Grabs an epw file from a list of file urls which may
# or may not include other file types
def get_file(file,Index):
    if '.epw' in file:
                    
        ### Uncomment download_file line to actually download the files
       # a = pd.DataFrame([[region.split('/')[-1],file.split('/')[-1].split('_')[0],re.split('\\.\d|_',file.split('/')[-1])[1],file.split('/')[-1]]],
       #    columns=['Region','Country','City','Filename'])
        
          # if '_' in file.split('/')[-1].split('_')[0]:
         #      country_cd = file.split('/')[-1].split('_')[0]
          # else:
           #    country_cd = file.split('/')[-1].split('_')[0]
        
           
       # NEED TO FIX THIS line
        a = pd.DataFrame([[region.split('/')[-1],country.split('/')[-1],city.split('/')[-1],file.split('/')[-1]]],
           columns=['Region','Country','City','Filename'])
        
        Index = Index.append(a)
        #print ('Region: ' + region.split('/')[-1])
        
        
        #### Comment this line out if you don't want to download
        download_file_old(root + file,'Weather Files')
        
        #print(file.split('/')[-1])
        #print("Country: " + file.split('/')[-1].split('_')[0])
        
        # Delimit by . followed by digit an or _ char
        #print("City: " + re.split('\\.\d|_',file.split('/')[-1])[1])
    return(Index)



for region in scrape_links(root + '/weather'): # Regions
    for country in scrape_links(root + region): 

        # Need to add code to scrape US and Canadian states and provinces (extra layer)
        if country in ['/weather-region/north_and_central_america_wmo_region_4/CAN%20%20',
 '/weather-region/north_and_central_america_wmo_region_4/USA%20%20' ]:
            for state in scrape_links(root + country):
                for city in scrape_links(root + state):
                    for file in scrape_links(root + city):
                        Index = get_file(file,Index)
        # All countries besides US and Canada
        else:
            for city in scrape_links(root + country):
           # print(city)
                for file in scrape_links(root + city):
                    Index = get_file(file,Index)
               
Index.to_csv('Index_scrape.csv')
