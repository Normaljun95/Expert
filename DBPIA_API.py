
import requests, re
from bs4 import BeautifulSoup

def cleanText(readData):
    text = re.sub('[-=+,#/\?:^$.@*\"※~&%ㆍ!』\\‘|\(\)\[\]\<\>`\'…》]', '', readData)
    text = re.sub('lt;', '', text)
    text = re.sub('HSgt;', '', text)
    text = re.sub('HEgt;', '', text)
    return text

input_name = "유재수"
apiKeyword = "차세대 모바일 콘텐츠 서비스를 위한 멀티미디어 인사말 시스템의 설계 및 구현"

url = "http://api.dbpia.co.kr/v2/search/search.xml"
queryParams = "?" + "key=" + "785daf59cf68133cc5df9a87a8d8f6c9" + "&target="+ "se" + "&searchall=" + apiKeyword +"&pagecount="+"1"

url = url + queryParams

res = requests.get(url, timeout=60)

soup = BeautifulSoup(res.content, "lxml-xml")
items = soup.find_all('item')
# print(items)

result_list = []

for item in items:
    # print('item :')
    # print(item)
    
    title = item.find('title')
    title = re.sub('<.+?>', '', str(title), 0).strip()
    title = cleanText(title)
    # print(title)
    
    authors = item.find_all('author')
    for author in authors:
        for name in author.find('name'):
            if input_name == name:
                # print(name)
                for url in author.find('url'):
                    print(url[50:])
