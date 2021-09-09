import pandas as pd
import numpy as np
# import matplotlib.pyplot as plt
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


import os
import glob

from _8a_scraper.user_beta_scrap import get_user_info2

# df = pd.read_csv("/Volumes/data/8a_scraper/combine_test.csv")
df = pd.read_csv("/Volumes/data/8a_scraper/climbers_unique_no_anons3.csv")
df_names = df.userName.unique()
print(df_names)



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

    # time.sleep(1)

    # info = get_user_info(name)
    # # print(info)

    # ascents = get_user_ascents(name, 'bouldering')
    # print(ascents)

    if name != "":
        try:
            # climber_info  = get_user_info(name)
            # climber_info = get_user_info2(name)
            climber_recs =  get_recommended_ascents2(name)
            # climbers = get_ascents(name , 'bouldering')
            
            # print(climber_recs)
            print(f'{name} climber is done!')
        
        except TimeoutException:
            print(f'cannot obtain {name} data... skipping')
            
            # driver.back()
            # continue so we can return to beginning of loop
            continue

        
        # print(climbers)

        # This code block shows how to export the data into a csv file
        try:
            if climber_recs != []:
                print(name)
                print(type(climber_recs))

                name = name.replace("/", "-")
                with open(f'/Volumes/data/climber_recs/climber-info-{name}.csv', 'w', newline='') as csvfile:
                    # try:
                    #_________________________________________________
                    # print(ascents)
                    fieldnames = climber_recs[0].keys()
                    print(f' fieldnames: {fieldnames}')

                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                    for rec in climber_recs:
                        writer.writerow(rec)
                        #__________________________________________________________________
                    # except:
                    #     print(f'climber info exeption route:{climber_info}')
                    #     # print(climber_info[0].keys())

                    #     print('field out of range')
                    #     print(f'Could not save {name} file!!!')
                    #     # 
                        
                    #     f = open('/Volumes/data/unmade_climber_info.txt', "a")
                    #     f.write(f"{name} wasnt made \n" )
                    #     f.close()
                    #     continue




                    # else:
                    #     writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                    #     for ascent in ascents:
                    #         writer.writerow(ascent)
            else:
                print('field out of range')
                print(f'Could not save {name} file!!!')
                # 
                
                f = open('/Volumes/data/unmade_climber_recs.txt', "a")
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