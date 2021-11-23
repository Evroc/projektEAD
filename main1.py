import pandas as pd
import glob
import os
from pandasgui import show #pip install pypiwin32
import numpy as np
import matplotlib.pyplot as plt
import sqlite3
#link do poleceń https://jug.dpieczynski.pl/lab-ead/Lab%2004%20-%20Projekt%20blok1_2021.html

def load_data():
    path = os.getcwd()+'\Data'
    #path = os.getcwd()+'\Data_test' #_test
    all_files = glob.glob(path + "/*.txt")
    #print(all_files) sprawdzenie co wczytuje

    df0 = pd.DataFrame()
    years=[]

    for filename in all_files:
        df = pd.read_csv(filename, header=None)
        year = filename.replace(path+"\yob", '')
        year = year.replace(".txt", '')
        years.append(year)
        df['Year'] = year
        df0 = df0.append(df)

    df0=df0.rename(columns={0: 'Name', 1: 'Sex', 2: 'Number'})

    return df0, years

def task2_3(df0):
    print("Zad2: ")
    print(f'Ilosc nadanych unikalnych imion bez rozrozniania na meskie i zenskie: {df0.nunique()[0]} ')
    print("===================")
    df_m = df0[df0['Sex'] == 'M']
    df_f = df0[df0['Sex'] == 'F']
    print("Zad3: ")
    print(f'Ilosc nadanych unikalnych imion meskich: {df_m.nunique()[0]} ')
    print(f'Ilosc nadanych unikalnych imion zenskich: {df_f.nunique()[0]} ')
    print("===================")

def task4_f(df):
    df.groupby(['Year', 'Sex']).sum().unstack('Sex')

    fem_births = df[df['Sex'] == 'F'].Number
    df['freq fem']=fem_births/fem_births.sum()

    mal_births=df[df['Sex'] == 'M'].Number
    df['freq m'] = mal_births/mal_births.sum()

    return df

def task4(df0, ifprint):
    #TODO Rozwiazanie bazuje na: https://pandasguide.readthedocs.io/en/latest/Pandas/babyname.html
    results = df0.groupby(['Year', 'Sex']).apply(task4_f)
    if ifprint==True:
        print("Zad 4:")
        print(results)
        print("===================")

    return results

def task5(df0, years):
    df_p=pd.pivot_table(df0, index=['Name'], columns=['Year', 'Sex'])
    df_p=df_p['Number']
    n_births=[]

    for i in years:
        n_births.append(df_p[i].sum())

    total_n_births=[]
    births_ratio_f_to_m=[]

    for i in range(0, len(n_births)):
        #[x][y] x - nr probki(rok), y - plec(0=f 1=m)
        births_ratio_f_to_m.append((n_births[i][0]/n_births[i][1]-1)*100)
        total_n_births.append((n_births[i][0]+n_births[i][1]))

    fixed_years = list(map(int, years))
    f, axes = plt.subplots(2)
    axes[0].bar(fixed_years,total_n_births)
    axes[0].set_title("Zad 5_1 urodzenia(lata)")
    axes[1].bar(fixed_years,births_ratio_f_to_m)
    axes[1].set_ylabel("% (wiecej/mniej) zenskich imion wzgledem meskich") #0% = tyle samo zenskich imion i meskich, 100% = 100% wiecej zenskich, -30% = o 30% mniej zenskich imion niz meskich
    axes[1].set_title("Zad 5_2 f/m ratio")
    plt.xticks(np.arange(min(fixed_years), max(fixed_years) + 1, 20.0))
    plt.show()

def task6(df, years, ifprint):

    many_F_dfs = []
    many_M_dfs = []

    fem_df = pd.DataFrame()
    mal_df = pd.DataFrame()

    for year in years:
        df1 = df[df['Year'] == year]

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

    if ifprint == True:
        print("Zad6: ")
        #TODO 1000 most popular male names
        print(mal_df)
        #-----------------------
        #TODO 1000 most popular female names
        print(fem_df)
        #-----------------------
        print("===================")

    #Do nastepnego zadania potrzebuje najpopularniejsze imie zenskie, wiec znajde je juz tutaj i przekaze
    max_Fem_Name = fem_df.idxmax()
    #print(max_Fem_Name[0])

    return max_Fem_Name[0], mal_df, fem_df

def task7(df, years, most_popular_fem_name, df_with_freq):
   # gui=show(df_with_freq)
    to_note = ['1930', '1970', '2015'] #tu podać jakie lata sprawdzać
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

    #TODO rysowanie wykresów wzialem z https://matplotlib.org/stable/gallery/subplots_axes_and_figures/two_scales.html


    fixed_years = list(map(int, years))
    fig, ax1 = plt.subplots()

    color = 'tab:red'
    ax1.set_xlabel('Years')
    ax1.set_ylabel('Johns', color=color)
    ax1.plot(fixed_years, johns_list, color=color)
    ax1.tick_params(axis='y', labelcolor=color)
    ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
    color = 'tab:blue'
    ax2.set_ylabel('name freq', color=color)
    ax2.plot(fixed_years, Johns_freq_list, color=color)
    ax2.tick_params(axis='y', labelcolor=color)
    fig.tight_layout()
    plt.xticks(np.arange(min(fixed_years), max(fixed_years) + 1, 20.0))
    plt.title("Zad7_1")
    plt.show()


    fig, ax1 = plt.subplots()

    color = 'tab:red'
    ax1.set_xlabel('Years')
    ax1.set_ylabel(most_popular_fem_name, color=color)
    ax1.plot(fixed_years, mostF_List, color=color)
    ax1.tick_params(axis='y', labelcolor=color)
    ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
    color = 'tab:blue'
    ax2.set_ylabel('name freq', color=color)
    ax2.plot(fixed_years, mostF_freq_list, color=color)
    ax2.tick_params(axis='y', labelcolor=color)
    plt.xticks(np.arange(min(fixed_years), max(fixed_years) + 1, 20.0))
    fig.tight_layout()
    plt.title("Zad7_2")
    plt.show()
    print("Zad7: ")
    for i in range(0, len(notedJ)):
        print(f'W roku {notedJ[i][0]} urodzilo sie {notedJ[i][1][1]} mezczyzn o imieniu John i {notedF[i][1][1]} kobiet o imieniu {most_popular_fem_name}')
    print("===================")
    # f, axes = plt.subplots(2)
    # axes[0].bar(years, johns_list)
    # axes[0].set_title("Imiona John(m) w czasie")
    # plt.show()

def task8(df, years, top1000_mal, top1000_fem): #nie bylem do konca pewny polecenia do tego zadania - top1000 jest ze wszystkich dostepnych lat i co roku porownuje imiona do tego zbioru
    top1000names_m = top1000_mal.index.values.tolist()
    top1000names_f = top1000_fem.index.values.tolist()
    df_fem=df[df['Sex']=='F']
    df_mal = df[df['Sex']=='M']
    ratio_f=[]
    ratio_m=[]
    diff_list=[]

    for year in years:
        times_in_1000_this_year_male=0
        times_in_1000_this_year_female = 0
        df_year_fem = df_fem[df_fem['Year'] == year]
        df_year_mal = df_mal[df_mal['Year'] == year]
        m_list = list(df_year_mal['Name'])
        f_list = list(df_year_fem['Name'])

        for i in range (0, len(m_list)):
            if m_list[i] in top1000names_m:
                times_in_1000_this_year_male+=1
        for i in range (0, len(f_list)):
            if f_list[i] in top1000names_f:
                times_in_1000_this_year_female+=1

        ratio_m.append(times_in_1000_this_year_male*100/len(top1000names_m)) #wiem ze top 1000 ma 1000 imion, ale jakbym kiedys zmienil z top1000 na np top 100 to bedzie latwiej
        ratio_f.append(times_in_1000_this_year_female*100 / len(top1000names_f))
        diff_list.append([(abs(times_in_1000_this_year_male-times_in_1000_this_year_female))*100/len(top1000names_m), year])
        #gui = show(df_year_fem)
        # sum_f_thisyear = df_year_fem.Number.sum()
        # sum_m_thisyear = df_year_mal.Number.sum()
        # ratio_f_thisyear = sum_f_thisyear/sum_f_overall
        # ratio_f.append(ratio_f_thisyear)
        #
        # ratio_m_thisyear = sum_m_thisyear/sum_m_overall
        # ratio_m.append(ratio_m_thisyear)

    print("Zad8: ")
    print(f'Maksymalna roznica w roznorodnosci wyniosla {max(diff_list)[0]} punkty procentowe i pojawila sie w {max(diff_list)[1]} roku')
    print("===================")
    fixed_years=list(map(int, years))

    fig, ax = plt.subplots()
    ax.plot(fixed_years, ratio_m, label='ratio m')
    ax.plot(fixed_years, ratio_f, label='ratio f')
    ax.set_ylabel('% imion danego roku należących do zbioru top1000(zbior ze wszystkich lat)')
    plt.title("Zad8")
    plt.xticks(np.arange(min(fixed_years), max(fixed_years) + 1, 20.0))
    ax.legend()
    plt.show()

def task12_13_14(df0):
    conn = sqlite3.connect('USA_ltper_1x1.sqlite')
    df_f = pd.read_sql('SELECT Year, Age, lx, dx, LLx FROM USA_fltper_1x1', conn)
    df_m = pd.read_sql('SELECT Year, Age, lx, dx, LLx FROM USA_mltper_1x1', conn)
    df = pd.concat([df_m, df_f], ignore_index=True)
    #gui = show(df)
    df0=df0[df0['Year'].astype(int)>1958]

    df_age0=df[df['Age']==0]
    #gui = show(df_age0)

    births=[]
    b_years=[]
    deaths=[]
    births_minus_deaths=[]
    survival_ratio=[]

    for year in range(1959,2018):
        df1 = df0[df0['Year'].astype(int) == year] #stad urodzenia w danym roku
        df2 = df[df['Year'].astype(int) == year] #stad zgony w danym roku
        df_a = df_age0[df_age0['Year'].astype(int) == year]
        survival_ratio.append((df1.Number.sum() - df_a.dx.sum()) / df1.Number.sum())

        deaths.append(df2.dx.sum())
        births.append(df1.Number.sum())
        births_minus_deaths.append(df1.Number.sum()-df2.dx.sum())
        b_years.append(year)
        #gui=show(df1)

    # print('--------------')
    # print(survival_ratio)
    # print('--------------')

    plt.plot(b_years, births_minus_deaths)
    plt.title("Zad13 Przyrost naturalny")
    plt.xticks(np.arange(min(b_years), max(b_years) + 1, 5.0))
    plt.show()

    plt.plot(b_years, survival_ratio)
    plt.title("Zad14 Survival ratio")
    plt.xticks(np.arange(min(b_years), max(b_years) + 1, 5.0))
    plt.show()

    # print(births)
    # print(deaths)
    # print(b_years)

if __name__ == '__main__':
    df, years=load_data()
    data_from4 = task4(df, False)
    data_from6, mal_df, fem_df = task6(data_from4, years, False)

    #wywolywanie kolejnych zadan
    task2_3(df)
    task4(df, True)
    task5(df, years)
    task6(data_from4, years, True)
    task7(df, years, data_from6, data_from4)
    task8(df, years, mal_df, fem_df)
    task12_13_14(df)