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


def clean_data(x1,x2,x3,x4,x5,x6,x7,x8,name,merge_type,df):
    all_s = pd.concat([x1, x2, x3, x4, x5, x6, x7, x8])
    all_s = all_s.reset_index()
    all_s = all_s[["Name", "Height", "Weight"]]
    
    all_s[['Height_m']] = all_s['Height'].str.extract('(?P<Height_m>\d.?\d\d)')
    all_s=all_s.set_index('Name')
    
    if name == 'Daiya Seto':
        all_s.at['Daiya Seto', 'Height_m'] = float(all_s.at['Daiya Seto', 'Height_m'])/100
        
    elif name == 'Takeshi Matsuda':
        all_s.at['Takeshi Matsuda', 'Height_m'] = float(all_s.at['Takeshi Matsuda', 'Height_m'])/100
    
    all_s[['Weight_kg_temp']] = all_s['Weight'].str.extract('(?P<Weight_kg>\d\d\s?kg)')
    all_s[['Weight_kg']] = all_s['Weight_kg_temp'].str.extract('(?P<Weight_kg>\d\d)')
    all_s = all_s[["Height_m","Weight_kg"]]
    all_s["Height_m"] = all_s["Height_m"].astype(float)
    all_s["Weight_kg"] = all_s["Weight_kg"].astype(float)
    
    all_s["BMI"] = all_s["Weight_kg"]/(all_s["Height_m"])**2
    
    if merge_type == 'outer':
        merged_df = df.merge(all_s, on='Name',how='outer')
    
    return merged_df


def clean_data3(x1,x2,x3,x4,x5,x6,df):
    all_s3 = pd.concat([x2, x2, x3, x4, x5, x6])
    all_s3 = all_s3.reset_index()
    all_s3 = all_s3[["Name", "Height", "Weight"]]

    all_s3[['Height_m']] = all_s3['Height'].str.extract('(?P<Height_m>\d.?\d\d)')
    all_s3=all_s3.set_index('Name')
    all_s3.at['Takeshi Matsuda', 'Height_m'] = float(all_s3.at['Takeshi Matsuda', 'Height_m'])/100 

    all_s3[['Weight_kg_temp']] = all_s3['Weight'].str.extract('(?P<Weight_kg>\d\d\s?kg)') 
    all_s3[['Weight_kg']] = all_s3['Weight_kg_temp'].str.extract('(?P<Weight_kg>\d\d)')
    all_s3 = all_s3[["Height_m","Weight_kg"]]
    all_s3["Height_m"] = all_s3["Height_m"].astype(float)
    all_s3["Weight_kg"] = all_s3["Weight_kg"].astype(float)

    all_s3["BMI"] = all_s3["Weight_kg"]/(all_s3["Height_m"])**2

    merged_df3 = df.merge(all_s3, on='Name',how='inner')
    
    return merged_df3


def list_medals(soup):
    table = soup.find_all('table')[1]
    body = table.find_all('tbody')[0]
    list_medals = body.find_all('td')

    medals_num = []
    for m in list_medals:
        medals_num.append(int(m.text))

    n = 5 

    final = [medals_num[i * n:(i + 1) * n] for i in range((len(medals_num) + n - 1) // n )]  
    top25_data = final[:25]

    table = soup.find_all('table')[1]
    body = table.find_all('tbody')[0]

    countries = []
    for x in body.find_all('span'):
        countries.append(x.text[1:-1])
    top25_countries = countries[:25]

    list_tuples_country = []
    for i in range(0,25):
        list_tuples_country.append((top25_countries[i],top25_data[i][0],top25_data[i][4]))

    list_tuples_medals = []
    for i in range(0,25):
        list_tuples_medals.append((top25_countries[i],top25_data[i][1],top25_data[i][2],top25_data[i][3]))

    return list_tuples_country, list_tuples_medals