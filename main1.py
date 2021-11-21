import pandas as pd
import glob
import os
from pandasgui import show #pip install pypiwin32
import numpy as np


#link do poleceń https://jug.dpieczynski.pl/lab-ead/Lab%2004%20-%20Projekt%20blok1_2021.html

def load_data():
    path = os.getcwd()+'\Data'
    test_path = os.getcwd()+'\Data_test'
    all_files = glob.glob(test_path + "/*.txt")
    print(all_files)

    df0 = pd.DataFrame()

    for filename in all_files:
        df = pd.read_csv(filename, header=None)
        year=filename.replace(test_path+"\yob", '')
        year=year.replace(".txt", '')
        df['Year']=year
        #print(type(filename))
        df0=df0.append(df)

    df0=df0.rename(columns={0:'Name', 1:'Sex', 2:'Number'})

    return df0


def zad1(df0):
    print(df0.nunique())  # TODO ZAD2 3265 dla 80-87
    visited = []
    cnt = 0
    # print(df0['Name'])
    # for i in range(0, len(df0['Name'])):
    #     if df0.loc[df0['Name']][i].isin(visited):
    #         visited.append(df0['Name'][i])
    #
    #         cnt += 1
    #
    # print("No.of.unique values :", cnt)
    #
    # print("unique values :", visited)
    #
    # print(df0.nunique(axis='index'))
    # df0.query('Name'==)
    gui = show(df0)

    # TODO ZAD4
    # df0['frequency_male'] = ""
    # df0['frequency_female'] = ""

def zad5(df0):
    #gui=show(df0)
    #df0['Year']

    df_p=pd.pivot_table(df0, index=['Name'], columns=['Year', 'Sex'])
    #print(df_p.columns.get_level_values(level=1))
    #df_p=df_p.loc[:,(df_p.columns.get_level_values(0)==1880)]
    #a=pd.DataFrame()
    list = ['1880', '1881', '1882']
    # for year in list:
    #     a = df_p.loc[:, (df_p.columns.get_level_values(1) == year)].sum()
    #     print(a)
    #     t = pd.DataFrame(a)
    #     t = t.rename(columns={0: 'Val'})
    #     print(t)
    #     gui = show(t)

    a = df_p.loc[:,(df_p.columns.get_level_values(1)=='1881')].sum()
    print(a)
    t=pd.DataFrame(a)
    t = t.rename(columns={0: 'Val'})
    print(t)
    gui=show(t)
    print(t.sum())
    t2=t.groupby(level='Sex').sum() #df sex f/m | val
    gui=show(t2)

    vals_f=[]
    vals_m=[]

    df_p2=pd.pivot(df0, columns='Year')
    #gui=show(df_p2)
    test=[]
    a=df_p.sum(min_count=1,skipna=True)
    test.append(a)
   # print(test[0])
def main(df0):
    # path = os.getcwd()+'\Data'
    # test_path = os.getcwd()+'\Data_test'
    # all_files = glob.glob(test_path + "/*.txt")
    # print(all_files)
    #
    # df0 = pd.DataFrame()

    # for filename in all_files:
    #     df = pd.read_csv(filename, header=None)
    #     year=filename.replace(test_path+"\yob", '')
    #     year=year.replace(".txt", '')
    #     df['Year']=year
    #     #print(type(filename))
    #     df0=df0.append(df)
    #
    # df0=df0.rename(columns={0:'Name', 1:'Sex', 2:'Number'})
    #df0=df0.set_index(['Name', 'Sex'])

    #print(df0.count(axis='index'))
    print(df0.nunique()) #TODO ZAD2 3265 dla 80-87
    visited=[]
    cnt=0
    #print(df0['Name'])
    for i in range(0, len(df0['Name'])):
        if df0.loc[df0['Name']][i].isin(visited):
            visited.append(df0['Name'][i])

            cnt += 1

    print("No.of.unique values :", cnt)

    print("unique values :", visited)

    print(df0.nunique(axis='index'))
    #df0.query('Name'==)
    gui=show(df0)

    #TODO ZAD4
    df0['frequency_male']=""
    df0['frequency_female']=""

if __name__ == '__main__':
    df=load_data()
    zad5(df)