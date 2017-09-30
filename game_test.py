from bs4 import BeautifulSoup
#import urllib.request
import requests


url = 'https://energyplus.net/weather-region/asia_wmo_region_2/RUS%20%20'

page = requests.get(url)
#page

soup = BeautifulSoup(page.content, 'html.parser')

# Gets links from a given region
data = soup.findAll("div", { "class" : "btn-group-vertical" })
for div in data:
    links = div.findAll('a')
    for a in links:
        print(a['href'])


# scrape the files


url2 = 'https://energyplus.net' + '/weather-location/asia_wmo_region_2/RUS//RUS_Yakutsk.249590_IWEC'

page2 = requests.get(url2)
#page

soup2 = BeautifulSoup(page2.content, 'html.parser')

# Gets links from a given region
data2 = soup2.findAll("div", { "class" : "btn-group-vertical" })
for div in data2:
    links = div.findAll('a')
    for a in links:
        if '.epw' in a['href'] :
            print(a['href'])
            
# Download file
test_file = requests.get('https://energyplus.net/weather-download/asia_wmo_region_2/RUS//RUS_Yakutsk.249590_IWEC/RUS_Yakutsk.249590_IWEC.epw')



    