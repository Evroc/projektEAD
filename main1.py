import pandas as pd
import glob
import os
from pandasgui import show #pip install pypiwin32
import numpy as np
import matplotlib.pyplot as plt

#link do poleceń https://jug.dpieczynski.pl/lab-ead/Lab%2004%20-%20Projekt%20blok1_2021.html

def load_data():
    path = os.getcwd()+'\Data'
    test_path = os.getcwd()+'\Data_test'
    all_files = glob.glob(test_path + "/*.txt")
    print(all_files)

    df0 = pd.DataFrame()
    years=[]

    for filename in all_files:
        df = pd.read_csv(filename, header=None)
        year=filename.replace(test_path+"\yob", '')
        year=year.replace(".txt", '')
        years.append(year)
        df['Year']=year
        #print(type(filename))
        df0=df0.append(df)

    df0=df0.rename(columns={0:'Name', 1:'Sex', 2:'Number'})

    return df0, years


def task1_2(df0):
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

def task4_f(df):
    df.groupby(['Year', 'Sex']).sum().unstack('Sex')

    fem_births = df[df['Sex']=='F'].Number
    df['freq fem']=fem_births/fem_births.sum()

    mal_births=df[df['Sex']=='M'].Number
    df['freq m']=mal_births/mal_births.sum()

    return df


def task4(df0, years, show):

    #https://pandasguide.readthedocs.io/en/latest/Pandas/babyname.html
    total_n_births=df0.pivot_table('Number', index='Year', columns='Sex', aggfunc=sum)
    results = df0.groupby(['Year', 'Sex']).apply(task4_f)
    if show==True:
        gui=show(results)

    return results
def task6(df, years, show):

    many_F_dfs = []
    many_M_dfs = []

    fem_df = pd.DataFrame()
    mal_df = pd.DataFrame()

    for year in years:
        df1 = df[df['Year']==year]

        df_fem = df1[df1['Sex'] == 'F']
        df_mal = df1[df1['Sex'] == 'M']

        # freq jest proporcjonalne do number, a dzialam w obrebie 1 roku = nie ma znaczenia
        df_fem = df_fem.sort_values('Number', ascending=False).head(1000)
        df_fem = df_fem[['Name','Number']]

        df_mal = df_mal.sort_values('Number', ascending=False).head(1000)
        df_mal = df_mal[['Name','Number']]

        many_F_dfs.append(df_fem)
        many_M_dfs.append(df_mal)

    j = 0
    k = 0

    for i in range(0, len(many_F_dfs)):
        if j == 0:
            fem_df = (many_F_dfs[i])
            j += 1
        else:
            fem_df = fem_df.groupby('Name').sum().add((many_F_dfs[i]).groupby('Name').sum(), fill_value=0)

    fem_df = fem_df.sort_values('Number', ascending=False).head(1000)



    for i in range(0, len(many_M_dfs)):
        if k == 0:
            mal_df = (many_M_dfs[i])
            k += 1
        else:
            mal_df = mal_df.groupby('Name').sum().add((many_M_dfs[i]).groupby('Name').sum(), fill_value=0)

    mal_df = mal_df.sort_values('Number', ascending=False).head(1000)

    if show == True:
        #TODO 1000 most popular male names
        gui=show(mal_df)
        #-----------------------
        #TODO 1000 most popular female names
        gui = show(fem_df)
        #-----------------------

    #For the next task I have to find most popular female name:
    max_Fem_Name = fem_df.idxmax()
    #print(max_Fem_Name[0])
    #-----------------------

    return max_Fem_Name[0]

def task7(df, years, most_popular_fem_name, df_with_freq):
   # gui=show(df_with_freq)
    to_note = ['1881', '1883'] #tu podać jakie lata sprawdzać
    notedJ = []
    notedF = []

    df_Johns = pd.DataFrame()
    df_MostF = pd.DataFrame()

    df_Johns_freq = pd.DataFrame()
    df_MostF_freq = pd.DataFrame()

    for year in years:
        df1 = df[df['Year'] == year]
        df_with_freq1 = df_with_freq[df_with_freq['Year'] == year]

        df_withJohn = df1[df1['Name']=='John']
        df_withJohn = df_withJohn[df_withJohn['Sex'] == 'M']
        df_withJohn = df_withJohn[['Name', 'Number']]

        df_withJohn_freq = df_with_freq1[df_with_freq1['Name']=='John']
        df_withJohn_freq = df_withJohn_freq[df_withJohn_freq['Sex'] == 'M']
        df_withJohn_freq = df_withJohn_freq[['Name', 'freq m']]

        df_withMostF = df1[df1['Name'] == most_popular_fem_name]
        df_withMostF = df_withMostF[df_withMostF['Sex'] == 'F']
        df_withMostF = df_withMostF[['Name', 'Number']]

        df_withMostF_freq = df_with_freq1[df_with_freq1['Name']==most_popular_fem_name]
        df_withMostF_freq = df_withMostF_freq[df_withMostF_freq['Sex'] == 'F']
        df_withMostF_freq = df_withMostF_freq[['Name', 'freq fem']]

        if year in to_note:
            notedJ.append([year, df_withJohn.sum()])
            notedF.append([year, df_withMostF.sum()])

        df_Johns=df_Johns.append(df_withJohn)
        df_MostF=df_MostF.append(df_withMostF)

        df_Johns_freq=df_Johns_freq.append(df_withJohn_freq)
        df_MostF_freq = df_MostF_freq.append(df_withMostF_freq)

    johns_list=df_Johns['Number'].to_list()
    mostF_List=df_MostF['Number'].to_list()
    Johns_freq_list=df_Johns_freq['freq m'].to_list()
    mostF_freq_list=df_MostF_freq['freq fem'].to_list()

    #https://matplotlib.org/stable/gallery/subplots_axes_and_figures/two_scales.html
    fig, ax1 = plt.subplots()

    color = 'tab:red'
    ax1.set_xlabel('Years')
    ax1.set_ylabel('Johns', color=color)
    ax1.plot(years, johns_list, color=color)
    ax1.tick_params(axis='y', labelcolor=color)
    ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
    color = 'tab:blue'
    ax2.set_ylabel('JohnsFreq', color=color)
    ax2.plot(years, Johns_freq_list, color=color)
    ax2.tick_params(axis='y', labelcolor=color)
    fig.tight_layout()

    plt.show()


    fig, ax1 = plt.subplots()

    color = 'tab:red'
    ax1.set_xlabel('Years')
    ax1.set_ylabel(most_popular_fem_name, color=color)
    ax1.plot(years, mostF_List, color=color)
    ax1.tick_params(axis='y', labelcolor=color)
    ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
    color = 'tab:blue'
    ax2.set_ylabel('Most popular female name freq', color=color)
    ax2.plot(years, mostF_freq_list, color=color)
    ax2.tick_params(axis='y', labelcolor=color)
    fig.tight_layout()

    plt.show()


    # print(johns_list)
    # print(noted[0][0]) #rok
    # print(noted[0][1][1]) #liczba

    for i in range(0, len(notedJ)):
        print(f'W roku {notedJ[i][0]} urodzilo sie {notedJ[i][1][1]} mezczyzn o imieniu John i {notedF[i][1][1]} kobiet o imieniu {most_popular_fem_name}')

    # f, axes = plt.subplots(2)
    # axes[0].bar(years, johns_list)
    # axes[0].set_title("Imiona John(m) w czasie")
    # plt.show()

def task5(df0, years):
    df_p=pd.pivot_table(df0, index=['Name'], columns=['Year', 'Sex'])
    df_p=df_p['Number']
    gui=show(df_p)
    n_births=[]

    for i in years:
        n_births.append(df_p[i].sum())

    total_n_births=[]
    births_ratio_f_to_m=[]

    for i in range(0, len(n_births)):
        #[x][y] x - nr probki(rok), y - plec(0=f 1=m)
        births_ratio_f_to_m.append((n_births[i][0]/n_births[i][1]-1)*100)
        total_n_births.append((n_births[i][0]+n_births[i][1]))

    # print("F")
    # print(n_births_f)
    # print("M")
    # print(n_births_m)
    # print("T")
    # print(total_n_births)
    # print("R")
    # print(births_ratio_f_to_m)
    f, axes = plt.subplots(2)
    axes[0].bar(years,total_n_births)
    axes[0].set_title("births(years)")
    axes[1].bar(years,births_ratio_f_to_m)
    axes[1].set_ylabel("% more f than m")
    axes[1].set_title("f/m ratio")
    plt.show()


if __name__ == '__main__':
    df, years=load_data()
    #task4(df, years, True)

    data_from4=task4(df, years, False)
    #task6(data_from4, years, True)

    data_from6=task6(data_from4, years, False)
    task7(df, years, data_from6, data_from4)