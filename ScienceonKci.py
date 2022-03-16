from http import client
from pymongo import MongoClient

input_name = "유재수"
apiKeyword = "빅데이터 환경에서 연속 질의 처리를 위한 리버스 k-최근접 질의 처리 기법"

client = MongoClient('mongodb://203.255.92.141:27017', authSource='admin')

domesticAPI = client['ID']['Domestic_API']

API_dict = {}
site = ['SCIENCEON', 'KCI']

sci_raw = client['SCIENCEON']['Rawdata']
kci_raw = client['KCI']['Rawdata']

result_sci = sci_raw.find_one({'$and':[{'author':{'$regex':input_name}},{'title':{'$regex':apiKeyword}}]})
result_kci = kci_raw.find_one({'$and':[{'author':{'$regex':input_name}},{'title':{'$regex':apiKeyword}}]})

sci_Alst = result_sci['author'].split(';')
kci_Alst = result_sci['author'].split(';')

sci_Aid = result_sci['author_id'].split(';')[sci_Alst.index(input_name)]
kci_Aid = result_kci['author_id'].split(';')[kci_Alst.index(input_name)]

API_dict = {'name' : input_name}

for s in range(len(site)):
    if site[s] == 'SCIENCEON':
        API_dict[site[s]] = {'A_id' : sci_Aid}
    else:
        API_dict[site[s]] = {'A_id' : kci_Aid}
    
print(API_dict)