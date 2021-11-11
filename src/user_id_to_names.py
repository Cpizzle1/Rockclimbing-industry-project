import numpy as np
import pandas as pd
import os
import sqlite3
import glob
import datetime
from tqdm import tqdm

def get_ids(path):

    os.chdir(path)
    result1 = glob.glob('*.{}'.format('csv'))

    empty_csvs = []
    for file1 in result1:
        filesize = os.path.getsize(file1)
        if filesize == 0:
            # print(f"{file1} The file is empty: " + str(filesize))
            empty_csvs.append(file1)

    print(len(empty_csvs))
#     files = [i for i in os.listdir(path) if i.startswith("climber-info")]
    files = result1
    full_csvs = [i for i in files if i not in empty_csvs]
    print(len(full_csvs))



    df_lst = []
    errors_list = []
    col_list = ['userAvatar', 'userName', 'userSlug', 'date', 'difficulty', 'isHard', 
       'isSoft', 'type', 'comment', 'traditional', 'project', 'rating', 
       'userPrivate', 'zlagGradeIndex', 'zlaggableName', 'zlaggableSlug', 
       'cragSlug', 'cragName', 'countrySlug', 'countryName', 'areaSlug', 
       'areaName', 'sectorSlug', 'sectorName', 'category', 'recommended', 
       'firstAscent', 'secondGo', 'isBoltedByMe', 'isOverhang', 'isVertical', 
       'isSlab', 'isRoof', 'isAthletic', 'isEndurance', 'isCrimpy', 'isCruxy', 
       'isSloper', 'isTechnical', 'isDanger', 'chipped', 'withKneepad', 
       'badAnchor', 'badBolts', 'highFirstBolt', 'looseRock', 
       'badClippingPosition'] 
    for file_name1 in tqdm(full_csvs[24000:40000]):
        try:
            file_name1 = file_name1.replace('\n',"")
            scraped_df = pd.read_csv(f'/Volumes/Backup Plus/boulder_csv/routes/{file_name1}', names = col_list)
            # scraped_df = scraped_df.loc[:, ~scraped_df.columns.str.contains('^Unnamed')]
            scraped_df['date'] = pd.to_datetime(scraped_df['date']).dt.tz_localize(None)
            scraped_df.date = scraped_df.date.dt.round('1d')

            file_name = scraped_df.zlaggableName.value_counts().index.tolist()[0]

            query1 = f'SELECT * FROM ascent where name = "{file_name}" and climb_type = 0'
            data = sqlite3.connect('/Users/cp/Documents/dsi/8a_kaggle/database.sqlite')
            ascents_df = pd.read_sql_query(query1, data)
            ascents_df['date'] = pd.to_datetime(ascents_df['date'], unit = 's')
            ascents_df['rec_date'] = pd.to_datetime(ascents_df['date'], unit = 's')
            ascents_df.date = ascents_df.date.dt.round('1d')

            # ascents_df = ascents_df.loc[:, ~ascents_df.columns.str.contains('^Unnamed')]

            ascents_df = ascents_df.drop_duplicates(subset="date", keep = False)
            scraped_df = scraped_df.drop_duplicates(subset="date", keep = False)

            new_df = pd.merge(ascents_df, scraped_df, how = 'inner', left_on = 'date', right_on = 'date')

            df_lst.append(new_df)

            compare_df = new_df[['user_id', 'userAvatar', 'userName']]
        except Exception as error:  
             
             
           
            errors_list.append(error) 
    results_df = pd.concat(df_lst)
    # return compare_df
    
    test_df = results_df[['user_id', 'userAvatar', 'userName']]
    test_df = test_df.drop_duplicates()
    return test_df, errors_list

if __name__ == '__main__':
    df, errors_list = get_ids('/Volumes/Backup Plus/boulder_csv/routes/')
    print(df)
    print(df.nunique)
    df.to_csv('/Users/cp/Documents/dsi/github_wikiclimber_public/rock_climbing_project/src/userid_name_avatar9.csv', index = False)