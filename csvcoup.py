from pymongo import MongoClient
import pandas as pd
import json

client = MongoClient('mongodb://203.255.92.141:27017', authSource='admin')

db = client['ID']
col = db['coopList']

xlsData = pd.read_excel("C:/workSpace(expert)/협업 전문가 리스트 (220418).xlsx")
payload = json.loads(xlsData.to_json(orient='records'))

for num in range(len(payload)):
    
    keys_list = list(payload[num].keys())
    
    values_list = list(payload[num].values())
    values_list[0] = str(values_list[0])
    values_list[1] = str(values_list[1])
    values_list[2] = str(values_list[2])
    values_list[3] = int(values_list[3])
    
    result = dict(zip(keys_list, values_list))
    col.insert(result)