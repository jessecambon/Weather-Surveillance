# Weather-Surveillance

Author: Jesse Cambon, jesse cambon a-t  gmail  <.> com

9/30/2017

DESCRIPTION

    This program can compare typical weather for a variety of locations around the 
    world using standard .EPW format weather files that can be downloaded
    from https://energyplus.net/weather.
    Currently using matplotlib and pandas dataframes for plotting

![Screenshot1](max_temp_inchon_nairobi.png?raw=true)


INSTRUCTIONS

    Run web_scrape.py file first to scrape all the data files to 
    the subfolder if you don't have the data yet
    
    The UI Index File builds an index that can be used for 
    a frontend once that is built
    
    The Weather Surveillance file has the backend to generate and plot
    data using the weather files

TODO

    - Label and organize files by region when I import them
    - Rank cities by max wind chill, heat index, etc. ****
    - Incorporate current and historic weather data (not just typical year)
    - Improve file download speed
    - Create UI for selecting which cities you want to compare
        - just in time delivery of files? (create index without downloading files)
    - Beautify plots
    - Display summary stats and tables
    