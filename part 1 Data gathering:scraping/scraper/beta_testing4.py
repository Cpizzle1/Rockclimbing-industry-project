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

from datetime import datetime
import re

path = '/Users/cp/Documents/dsi/8a_project/8a_scraper'
extension = 'csv'
os.chdir(path)
result1 = glob.glob('*.{}'.format(extension))
# print(result1)

sub_string_lst = []
for file_name in result1:
    # print(file_name)
    stringed_name = str(file_name)
    # print(stringed_name)
    substring = re.search("data-(.*?).csv", stringed_name)
    sub_string_lst.append(substring)



    


db_conn = sqlite3.connect('database.sqlite')
theCursor = db_conn.cursor()
theCursor.execute('select name, count(name) from ascent where climb_type = 1 group by name order by count(name) DESC')
# theCursor.execute('select distinct(name) from ascent where climb_type = 1;')

names = (theCursor.fetchall())
print(len(names))
names_2 = []

# res = [ ele for ele in test_list1 ]
for person in names:
  if person in sub_string_lst:
    names.remove(person)

for i in names:
    

    if (f'data-{i[0]}.csv') not in result1:
        # print(f'{i} is the climb name in progress')
    # joined_string = "".join(i)
    # joined_string.append(names_2)
        first  = i[0]
        result = str(first)
        names_2.append(result)
    else:
        # print(f'data-{i[0]}.csv is already made!!')
        continue



print(f'length of all distinct routes: {len(names)}')
print(f'length of routes already made:{len(result1)}')
print(f'not made yet total ascents:{len(names_2)}')

len(names)
# short_names = names_2[14190:25000]
# short_names = names_2[17746:25000]
# short_names = names_2[19341:25000]
# short_names = names_2[2256:25000]
short_names = names_2[85000:95000]
print(len(short_names))


login()
count = 75000
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
            climbers = get_ascents(name , 'bouldering')
            dateTimeObj = datetime.now()
            print(dateTimeObj)

            print(f'{name} route is done!')
        
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
            name = name.replace("/", "-")
            with open(f'data-{name}.csv', 'w', newline='') as csvfile:
                try:
                    fieldnames = climbers[0].keys()
                    # print(fieldnames)
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                    for climber in climbers:
                        writer.writerow(climber)
                except:
                    print('field out of range')
                    print(f'Could not save {name} file!!!')
                    #

                    
                    #
                    f = open('/Users/cp/Documents/dsi/8a_project/8a_scraper/ascents_unmade.txt', "a")
                    f.write(f"{name} wasnt made \n" )
                    f.close()
                    
                    dateTimeObj = datetime.now()
                    print(dateTimeObj)
                    continue
        # except:
        #     pass
        #     # print('something went wrong')

        except TimeoutException:
            # driver.back()
            # continue so we can return to beginning of loop
            dateTimeObj = datetime.now()
            print(dateTimeObj)
            continue