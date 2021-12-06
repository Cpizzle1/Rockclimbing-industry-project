import pandas as pd
import os
import glob
import re
import sqlalchemy
import re

def clean_climber_details_from_user_deets(path, pattern):
    """[takes csvs from folder (path) and combines them into single large dataframe
    with colnames as columns.  Meant for scraped data]

    Args:
        path ([string]): [path to folder of csv files]
        pattern ([string]): [file path of each csv minus the unique name (in case 
        there is a prefix to filename ie 'climber-info-')]

    Returns:
        [pandas Dataframe]: [combined csv files into single large dataframe]
    """
    all_files = glob.glob(path + "/*.csv")
    li = []
    colnames=['location', 'age', 'website', 'sponsors', 'started_climbing', 'occupation', 'other_interests', 'best_climbing_area', 'known_areas', 'height', 'dob'] 
    for filename in all_files:
        # pattern = "/Volumes/Backup Plus/climber_deets/climber-info-(.*?).csv"
        substring = re.search(pattern, filename).group(1)
        df = pd.read_csv(filename, names=colnames, header=None)
        df['name'] = substring
        li.append(df)
        if len(li)%500 ==0:
            print (len(li))
        # for index in range(len(li)):
        #     if len(li)%500 ==0:
        #         print(li[index])
    frame = pd.concat(li)
    return frame

def combine_ascent_csvs(path):
    """[combines all scraped data to a single large dataframe with duplicates dropped]

    Args:
        path ([string]): [path to folder with csvs]

    Returns:
        [dataframe]: [combined dataframe from all csvs with duplicates dropped]
    """
    # path = '/Users/cp/Documents/dsi/8a2/8a_scraper/'
    # extension = 'csv'
    os.chdir(path)
    result1 = glob.glob('*.{}'.format('csv'))

    empty_csvs = []
    for file1 in result1:
        filesize = os.path.getsize(file1)
        if filesize == 0:
            # print(f"{file1} The file is empty: " + str(filesize))
            empty_csvs.append(file1)

    print(len(empty_csvs))
    files = [i for i in os.listdir(path) if i.startswith("climber-info")]
    full_csvs = [i for i in files if i not in empty_csvs]
    
    list_df = []
    count = 0
    for file in full_csvs:
        df = pd.read_csv(f'{path}/{file}',header=None,  error_bad_lines=False)
        list_df.append(df)
        count +=1
        if count%500 ==0:
            print(count)
    df2 = pd.concat(list_df)
    df2 = df2.drop_duplicates(keep='last')
    df2.rename(columns = {0:'ascentId'
    ,1: 'areaName'
    ,2: 'areaSlug'
    ,3: 'cragName'
    ,4: 'cragSlug'
    ,5: 'sectorSlug'
    ,6: 'zlaggableName'
    ,7: 'zlaggableSlug'
    ,8: 'countrySlug'
    ,9: 'userAvatar'
    ,10: 'userName'
    ,11: 'userSlug'
    ,12: 'date'
    ,13: 'difficulty'
    ,14: 'gradeIndex'
    ,15: 'comment'
    ,16: 'isPrivateComment'
    ,17:'traditional'
    ,18:'project'
    ,19:'isHard'
    ,20:'isSoft'
                            
    ,21: 'firstAscent'
    ,22: 'secondGo'
    ,23: 'type'
    ,24: 'notes'
    ,25: 'rating'}, inplace = True)

    return df2

# def get_user_ids(csv_file):
#     df = pd.read_csv(csv_file)
#     avatar_str_lst = df.userAvatar.unique()
#     # avatar_str_lst_full = [x for x in avatar_str_lst if x != 'nan']
#     non_float_lst_avatar_str_lst= []
#     for i in avatar_str_lst:
#         if type(i) ==str:
#             non_float_lst_avatar_str_lst.append(i)
#     potential_user_nums= []
    
#     pattern2 = "gallery/(.*?)\."
#     for string in non_float_lst_avatar_str_lst:
#         string= string.lower()
#         print(string)
#     #     if "jpg" in string:
#         substring = re.search(pattern2, string).group(1)
#         print(substring)
#         potential_user_nums.append(substring)

#     for i in potential_user_nums:
#         if i.isnumeric() == True:
#             print(i)


def get_user_ids2(csv_file):
    """[gets user names from useravatar data]

    Args:
        csv_file ([csv]): [csv with all data combined]

    Returns:
        [dataframe]: [extracted names of users]
    """
    df = pd.read_csv(csv_file)
    df = df.drop_duplicates()
    df.userAvatar.fillna(value = 'disregard', inplace = True)
    df['b'] = df['userAvatar'].apply(lambda s:s.split('/')[0].split('.'))
    df['c'] = df['b'][1].apply(lambda s:s.split('/'))
    df['num_val'] = df.userAvatar.str.extract('gallery/(\d+).', expand = False)
    return df
            

if __name__ == '__main__':
    # x = clean_climber_details('/Volumes/Backup Plus/climber_deets', "/Volumes/Backup Plus/climber_deets/climber-info-(.*?).csv")
    # print(x)

    # x = climber_ids('/Volumes/Backup Plus/climber_deets')
    # print(x)
    
    # x = combine_ascent_csvs('', index = False)
    # print(x.head)
    # print(x.shape)
    # x.to_csv('/Users/cp/Documents/dsi/github_wikiclimber_public/rock_climbing_project/src/boulders_full.csv')
