from bs4 import BeautifulSoup
#import urllib.request
import requests

# This program downloads all our Weather File Data to A Subfolder


root = 'https://energyplus.net'

        
# Downloads a file from a given URL to a specified subfolder            
def download_file(url,subfolder_name):
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
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    
    # Select the given div
    data = soup.findAll("div", { "class" : "btn-group-vertical" })
    
    for div in data:
        links = div.findAll('a')
        list_links = [a['href'] for a in links]
    
    return list_links


#download_file('https://energyplus.net/weather-location/africa_wmo_region_1/EGY//EGY_Asyut.623930_ETMY/weather-download/africa_wmo_region_1/EGY//EGY_Asyut.623930_ETMY/EGY_Asyut.623930_ETMY.epw','Weather Files')

import re

for region in scrape_links(root + '/weather'): # Regions
    for country in scrape_links(root + region):
        for city in scrape_links(root + country):
            for file in scrape_links(root + city):
                if '.epw' in file:
                    #print(root + file)
                    
                    ### Uncomment download_file line to actually download the files
                    
                    #download_file(root + file,'Weather Files')
                    #print(file.split('/')[-1])
                    print("Country: " + file.split('/')[-1].split('_')[0])
                    
                    # Delimit by . followed by digit an or _ char
                    print("City: " + re.split('\\.\d|_',file.split('/')[-1])[1])
               

