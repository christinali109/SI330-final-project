import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

#function that grabs height and weight data on swimmers from wikipedia page
def swimmers_data(url,name):
    list_names = ["Louis Croenen","Velimir Stjepanovic","Chen Yin","Wu Peng"] #special cases 
    if name in list_names:
        df=pd.read_html(url)[0]

        df=df[["Personal information","Personal information.1"]]
        df=df.T
        df.rename(columns=df.loc["Personal information"], inplace=True)
        df=df.drop(["Personal information"])

        df=df[['Height', 'Weight']]
        df["Name"]=name
        df=df.reset_index()

        cols = df.columns.tolist()
        cols = cols[-1:] + cols[:-1]
        df = df[cols]
        df=df[['Name', 'Height', 'Weight']]
    else:
        df=pd.read_html(url)[0]

        df=df[[0, 1]]
        df=df.T
        df.rename(columns=df.loc[0], inplace=True)
        df=df.drop([0])

        df=df[['Height', 'Weight']]
        df["Name"]=name

        cols = df.columns.tolist()
        cols = cols[-1:] + cols[:-1]
        df = df[cols]
    return df

def readhtml(url,num,x,n1,n2,n3):
    df = pd.read_html(url)[num]
    if x == 2:
        df.at[5,'Name'] = "Velimir Stjepanovic"
    df=df.set_index('Name')

    df.at[n1,'Rank'] = 1
    df.at[n2,'Rank'] = 2
    df.at[n3,'Rank'] = 3

    df = df[["Rank","Nationality","Time"]]
    return df