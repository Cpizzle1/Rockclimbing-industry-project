from _8a_scraper.users import get_user_info, get_user_ascents
import sqlite3
import pandas as pd
import numpy as np
import selenium 
from _8a_scraper.ascents import *
from _8a_scraper.users  import *
from  _8a_scraper.utils import *
import csv
import time
import os
import glob
from datetime import datetime
import re



def get_products():
    """
    get data from website... It is kept anonymous to prevent people from abusing this webscraping tool, 
    but code can be provided to demonstrate performance
    
    """
    path = '/Volumes/data/routes/'
    extension = 'csv'
    os.chdir(path)
    result1 = glob.glob('*.{}'.format(extension))
    sub_string_lst = []
    for file_name in result1:
        # print(file_name)
        stringed_name = str(file_name)
        substring = re.search("data-(.*?).csv", stringed_name)
        sub_string_lst.append(substring)
    
    db_conn = sqlite3.connect('/Volumes/data/database.sqlite')
    theCursor = db_conn.cursor()
    theCursor.execute('select name, count(name) from ascent where climb_type = 0 group by name order by count(name) DESC')
    names = (theCursor.fetchall())
    print(len(names))
    names_2 = []
    for person in names:
    if person in sub_string_lst:
        names.remove(person)

    for i in names:
        if (f'data-{i[0]}.csv') not in result1:
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
    short_names = names_2[119236:125000]
    print(len(short_names))
    ogin()
    count = 119236
    for name in short_names:
        
        print(type(name))
        print(name)
        count+=1
        print(count)
        if name != "":
            try:
                climbers = get_ascents(name , 'sportclimbing')
                dateTimeObj = datetime.now()
                print(dateTimeObj)

                print(f'{name} route is done!')
            
            except TimeoutException:
                print(f'cannot obtain {name} data... skipping')
                dateTimeObj = datetime.now()
                print(dateTimeObj)
                continue

            try:
                name = name.replace("/", "-")
                with open(f'/Volumes/data/routes/{name}.csv', 'w', newline='') as csvfile:
                    try:
                        fieldnames = climbers[0].keys()
                        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                        for climber in climbers:
                            writer.writerow(climber)
                    except:
                        print('field out of range')
                        print(f'Could not save {name} file!!!')
                        f = open('/Volumes/data/unmade_routes.txt', "a")
                        f.write(f"{name} wasnt made \n" )
                        f.close()
                        
                        dateTimeObj = datetime.now()
                        print(dateTimeObj)
                        continue

            except TimeoutException:
                dateTimeObj = datetime.now()
                print(dateTimeObj)
                continue
if __name__ =='__main__':
    get_products()