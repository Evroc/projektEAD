import pandas as pd
import glob
import os
from pandasgui import show #pip install pypiwin32





def main():
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
    main()