import pandas as pd
import numpy as np
import os
from os import path
import shutil
import psycopg2
import sys
from config import  param_dic 


def connect(params_dic):
    """ Connect to the PostgreSQL database server """
    conn = None
    try:
        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params_dic)
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        sys.exit(1) 
    print("Connection successful")
    return conn

def postgresql_to_dataframe(conn, select_query, column_names):
    """
    Tranform a SELECT query into a pandas dataframe
    """
    cursor = conn.cursor()
    try:
        cursor.execute(select_query)
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error: %s" % error)
        cursor.close()
        return 1
    
    # Naturally we get a list of tupples
    tupples = cursor.fetchall()
    cursor.close()
    
    # We just need to turn it into a pandas dataframe
    df = pd.DataFrame(tupples, columns=column_names)
    return df


def fix_11c(df, df_sqlite_full):
    df_11c = df[df['difficulty']== '6c+']
    df_11c2 = df_11c[(df_11c['zlagGradeIndex'] >20) &  (df_11c['zlagGradeIndex'] <24)]
    df_11c2_dropped = df_11c2.drop_duplicates(keep = 'last')
    names = df_11c2_dropped.zlaggableName.unique()
    for item, frame in df_sqlite_full['name'].iteritems():
        if frame in names:
            # print(f'{frame}:{item}:')
            df_sqlite_full.at[item, 'grade_id'] =47
    return df_sqlite_full








if __name__ =="__main__":
    df = pd.read_csv('/Users/cp/Documents/dsi/8a_kaggle/routes_full.csv')
    # param_dic = param_dic = {
    #         "host"      : "*****",
  
    #         # "database"  : '*********',
    #         "database"  : '**',
    
    #         "user"      : '*******',
    
    
    #         "password"  : "*****"
        
    # }

    conn = connect(param_dic)
    column_names = ['id', 'user_id', 'grade_id', 'notes', 'raw_notes', 'method_id',
       'climb_type', 'total_score', 'date', 'year', 'last_year', 'rec_date',
       'project_ascent_date', 'name', 'crag_id', 'crag', 'sector_id', 'sector',
       'country', 'comment', 'rating', 'description', 'yellow_id', 'climb_try',
       'repeat', 'exclude_from_ranking', 'user_recommended', 'chipped', 'shoe', 'video', 'screename']
    df_sqlite_full = postgresql_to_dataframe(conn, "select * from ascents", column_names)

    df2 = fix_11c(df, df_sqlite_full)
    print(df2.grade_id.value_counts())