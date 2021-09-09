import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
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
import pandas as pd
import numpy as np
import selenium 
from selenium.common.exceptions import TimeoutException

from _8a_scraper.ascents import get_ascents
from _8a_scraper.ascents import *
from _8a_scraper.users  import *
from  _8a_scraper.utils import *

import csv
import time
from datetime import datetime


import os
import glob


df = pd.read_csv("/Volumes/64gig data_sets/combine_test.csv")

df_names = df.userName.unique()



# for name in df_names[:2]:
#     ascents  = get_user_ascents(name, 'bouldering')
#     print(ascents)
#     print(type(ascents))
#     # climbers = get_ascents('Midnight Lightning', 'bouldering')
    
#     # print(climbers)

#     # This code block shows how to export the data into a csv file
    
#     with open('data.csv', 'w', newline='') as csvfile:
#         fieldnames = climbers[0].keys()
#         writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
#         for climber in climbers:
#             writer.writerow(climber)


#-------------------------------------------------------------------------------------------------------------------------
# len(names)
short_names = df_names[13890:]
print(len(short_names))


login()
count = 13890
for name in short_names:
    
    print(type(name))
    print(name)
    # print(short_names)
    count+=1
    print(count)

    # time.sleep(1)

    # info = get_user_info(name)
    # # print(info)

    # ascents = get_user_ascents(name, 'bouldering')
    # print(ascents)

    if name != "":
        try:
            # ascents  = get_user_ascents(name, 'bouldering')
            ascents  = get_user_ascents(name, 'sportclimbing')
            # climbers = get_ascents(name , 'bouldering')
            print(f'{name} climber is done!')
            dateTimeObj = datetime.now()
            print(dateTimeObj)
        
        except TimeoutException:
            print(f'cannot obtain {name} data... skipping')
            dateTimeObj = datetime.now()
            print(dateTimeObj)
            
            # driver.back()
            # continue so we can return to beginning of loop
            continue

        
        # print(climbers)

        # This code block shows how to export the data into a csv file
        try:
            if ascents != []:

                name = name.replace("/", "-")
                # with open(f'climber-info-{name}.csv', 'w', newline='') as csvfile:
                with open(f'/Volumes/64gig data_sets/sport_climbing_logbooks/climber-sport_climbing-{name}.csv', 'w', newline='') as csvfile:
                    try:
                        # print(ascents)
                        fieldnames = ascents[0].keys()
                        # print(fieldnames)

                        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                        for ascent in ascents:
                            writer.writerow(ascent)
                    except:
                        print('field out of range')
                        print(f'Could not save {name} file!!!')
                        dateTimeObj = datetime.now()
                        print(dateTimeObj)
                        # 
                        
                        # f = open('/Users/cp/Documents/dsi/8a2/8a_scraper/users_unmade.txt', "a")
                        f = open('/Users/cp/Documents/dsi/8a2/8a_scraper/users_unmade.txt', "a")
                        f.write(f"{user} wasnt made \n" )
                        f.close()
                        continue
                    # else:
                    #     writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                    #     for ascent in ascents:
                    #         writer.writerow(ascent)
            else:
                print('field out of range')
                print(f'Could not save {name} file!!!')
                # f = open('/Users/cp/Documents/dsi/8a2/8a_scraper/users_unmade.txt', "a")
              
                f = open('/Volumes/64gig data_sets/users_sport_climbing_unmade.txt', "a")
                f.write(f"{name} wasnt made \n" )
                f.close()
                continue



                   
        # except:
        #     pass
        #     # print('something went wrong')

        except TimeoutException:
            # driver.back()
            # continue so we can return to beginning of loop
            continue
   