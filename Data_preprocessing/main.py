import pandas as pd
import json
df1=pd.read_csv('Generaldata.csv')
df2=pd.read_csv('general and  schizophrenia.csv')
df3=pd.read_csv('stress.csv')
df4=pd.read_csv('depression.csv')
df_combine_data=pd.concat([df1,df2,df3,df4],ignore_index=True)
df_combine_data.to_csv("combine_data.csv",index=False)

df_combine_data=df_combine_data.drop(['Unnamed: 2'], axis=1)

df_combine_data.isnull().sum()
df_combine_data = df_combine_data.dropna()
print(df_combine_data.isnull().sum())

duplicate = df_combine_data[df_combine_data.duplicated()]
print("Duplicate Rows :")
print(duplicate)
df_combine_data=df_combine_data.drop_duplicates(keep="first")

df_combine_data['content']=df_combine_data['content'].str.strip()

df_combine_data['content'] = df_combine_data['content'].str.replace(r'[!"#$%&()*+,-./:;<=>?@[\]^_`{|}~]+', '')

#Verifying that the data
duplicate = df_combine_data[df_combine_data.duplicated()]
if len(duplicate) > 0:
    print("There are {len(duplicate)} duplicate records in the data")
else:
    print("There are no duplicate records in the data")

Null_number=df_combine_data.isna().sum().sum()
if Null_number > 0:
    print("There are {Null_number} null records in the data")
else:
    print("There are no null records in the data")

# Check any incorrect data
if ( df_combine_data['content'].dtype.kind in 'iufc') == False :
    print("There are no incorrect data in the data")
else:
    print("There are incorrect data in the data")

# convert data to json format
data_json=[{
    'Content': text,
}for text in df_combine_data['content'].values]
with open('data.json', 'w') as f:
    json.dump(data_json, f, ensure_ascii=False, indent=4)
