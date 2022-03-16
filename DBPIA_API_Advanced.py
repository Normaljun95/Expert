import requests, re
from bs4 import BeautifulSoup
import xmltodict
import json

input_name = "유재수"
apiKeyword = "차세대 모바일 콘텐츠 서비스를 위한 멀티미디어 인사말 시스템의 설계 및 구현"

url = "http://api.dbpia.co.kr/v2/search/search.xml"
queryParams = "?" + "key=" + "785daf59cf68133cc5df9a87a8d8f6c9" + "&target="+ "se" + "&searchall=" + apiKeyword +"&pagecount="+"1"

url = url + queryParams

try :
    resq = requests.get(url, timeout = 60)
    rescode = resq.status_code
    # print(rescode)
except Exception as e:
    print(e)
    rescode = 500

# print(url)
if rescode == 200:
    conn = resq.content
    xmldict = xmltodict.parse(conn)
    
    rawData = {}
    
    item = xmldict['root']['result']['items']['item']
    
    if isinstance(item['authors']['author'], list):
        name_list = []
        id_list = []
        name_list = [0]*len(item['authors']['author'])
        id_list = [0]*len(item['authors']['author'])
        
        for z in range(0, len(item['authors']['author'])):
            name_list[z]=item['authors']['author'][z]['name']
            id_list[z]=','.join(re.findall('\d+',item['authors']['author'][z]['url']))
            
            if input_name in name_list[z]:
                rawData['author'] = name_list[z]
                rawData['author_id'] = id_list[z]
            
    else:
        rawData['author'] = item['authors']['author']['name']
        rawData['author_id'] =",".join(re.findall('\d+',item['authors']['author']['url']))
        
    rawData['title'] = re.sub('<.+?>','',item['title'])
    rawData['issn'] = item['publication']['issn']
    print(rawData)

else:
    nothing = {}
    nothing['progress'] = 1.0
    nothing['title'] = apiKeyword
    nothing['isPartial'] = False
    print("Error Code" + rescode)