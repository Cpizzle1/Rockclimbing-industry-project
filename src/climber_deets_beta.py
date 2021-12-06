import pandas as pd
import numpy as np
import json, requests
from slugify import slugify
from bs4 import BeautifulSoup
import csv
from _8a_scraper.users import get_user_info, get_user_ascents, get_recommended_ascents
from _8a_scraper.ascents import *
from _8a_scraper.users  import *
from  _8a_scraper.utils import *
from _8a_scraper.users import get_user_info, get_user_ascents
import sqlite3import selenium 
from selenium.common.exceptions import TimeoutException
from _8a_scraper.ascents import get_ascents
from _8a_scraper.ascents import *
from _8a_scraper.users  import *
from  _8a_scraper.utils import *
import time
import os
import glob

from _8a_scraper.user_beta_scrap import get_user_info2

def pull_data():
    """[Pulls data from website on users details]
    """

    df = pd.read_csv("/Volumes/data/8a_scraper/climbers_unique_no_anons.csv")
    df_names = df.userName.unique()
    short_names = df_names[:]
    print(len(short_names))


    login()
    count = 0
    for name in short_names:
        
        print(type(name))
        print(name)
        # print(short_names)
        count+=1
        print(count)


        if name != "":
            try:
                climber_info = get_user_info2(name)
                # climbers = get_ascents(name , 'bouldering')
                print(climber_info)
                print(f'{name} climber is done!')
            
            except TimeoutException:
                print(f'cannot obtain {name} data... skipping')
                continue

            
            # print(climbers)

            # This code block shows how to export the data into a csv file
            try:
                if climber_info != []:
                    print(name)
                    print(type(climber_info))

                    name = name.replace("/", "-")
                    with open(f'/Volumes/data/climber_deets/climber-info-{name}.csv', 'w', newline='') as csvfile:
                        # print(ascents)
                        fieldnames = climber_info.keys()
                        print(f' fieldnames: {fieldnames}')

                        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                        writer.writerow(climber_info)
        
                else:
                    print('field out of range')
                    print(f'Could not save {name} file!!!')
                    f = open('/Volumes/data/unmade_climber_info.txt', "a")
                    f.write(f"{name} wasnt made \n" )
                    f.close()
                    continue




            except TimeoutException:
                # driver.back()
                # continue so we can return to beginning of loop
                continue
   if __name__ == "__main__":
       pull_data()
