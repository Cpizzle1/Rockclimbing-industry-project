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
import sqlite3
import selenium 
from selenium.common.exceptions import TimeoutException
from _8a_scraper.ascents import get_ascents
import csv
import time
import os
import glob
from _8a_scraper.user_beta_scrap import get_user_info2, get_recommended_ascents2

    
def get_recommended(): 
    # df = pd.read_csv("/Volumes/data/8a_scraper/combine_test.csv")
    df = pd.read_csv("/Volumes/data/8a_scraper/climbers_unique_no_anons3.csv")
    df_names = df.userName.unique()
    print(df_names)
    short_names = df_names[14809:]
    print(len(short_names))
    login()
    count = 14809
    for name in short_names:
        
        print(type(name))
        print(name)
        # print(short_names)
        count+=1
        print(count)
        if name != "":
            try:
                climber_recs =  get_recommended_ascents2(name)
                print(f'{name} climber is done!')
            
            except TimeoutException:
                print(f'cannot obtain {name} data... skipping')
                continue
            try:
                if climber_recs != []:
                    print(name)
                    print(type(climber_recs))

                    name = name.replace("/", "-")
                    with open(f'/Volumes/data/climber_recs/climber-info-{name}.csv', 'w', newline='') as csvfile:
                        fieldnames = climber_recs[0].keys()
                        print(f' fieldnames: {fieldnames}')

                        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                        for rec in climber_recs:
                            writer.writerow(rec)

                    print('field out of range')
                    print(f'Could not save {name} file!!!')
                    # 
                    
                    f = open('/Volumes/data/unmade_climber_recs.txt', "a")
                    f.write(f"{name} wasnt made \n" )
                    f.close()
                    continue

            except TimeoutException:
                # driver.back()

                continue
if __name__ == "__main__":
    get_recommended()
