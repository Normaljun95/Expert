import datetime, requests, xmltodict
import re, math

def DBPIA(self):

    a = " "
    keywords = {'and' : [], 'or' : [], 'not' : []}

    dt = datetime.datetime.now()
    #Field 변경 / API Key 변경 시 수정 필요 (Porting)
    url = "http://api.dbpia.co.kr/v2/search/search.xml"
    queryParams = '?' + 'key=' + '785daf59cf68133cc5df9a87a8d8f6c9' + '&target='+'se_adv' + '&searchall=' + self.apiKeyword  +'&pagecount='+'100' + '&pyear='+'3'+ '&pyear_start=' +self.year +'&pyear_end='+ str(dt.year)  +'&sorttpye=' +'1'
    url = url + queryParams

    rescode = 0
    try :
        resq = requests.get(url, timeout = self.timeout)
        rescode = resq.status_code
    except Exception as e :
        print(e)
        rescode = 500

    isPartial = False

    print(url)
    if rescode ==200:
        conn = resq.content
        xmldict = xmltodict.parse(conn)
        nothing = {}
        if 'error' in xmldict :
            nothing['progress'] = 1.0
            nothing['keyId'] = self.keyId
            nothing['isPartial'] = False
            self.producer.send(self.site, value=nothing)
            self.flush()
        else:
            total_count=int(xmldict['root']['paramdata']['totalcount'])
            print(total_count)
            pagenum = int(math.ceil((int(total_count)/100)))

            hundred = 100                
            temp_total_count =int(total_count)
            temp_count = 0
            temp_rawData = {}
            success_count = 0
            fail_count = 0

            """ #5-1. 검색 결과 없을 떄 행위 """
            if int(pagenum)==0:
                nothing['progress'] = 1.0
                nothing['keyId'] = self.keyId
                nothing['isPartial'] = False
                self.producer.send(self.site, value=nothing)
                self.flush()
                print(nothing)
                print("검색결과가 없습니다.")
            else:
                cnt = 0
                pagenum = int(math.ceil((int(total_count)/hundred)))                    
                START =  datetime.datetime.now()
                for i in range(1,pagenum+1):
                    try:

                        """ #5-2. 10만건 이상 시 stop """
                        if cnt > self.stopCount :
                            isPartial = True
                            break
                        add_queryparam = '&pagenumber=' +'{}'.format(i)
                        final_url = url + add_queryparam


                        """ #5-3. API 응답 정상이 아닐 때 n번 재요청 """
                        retryCount = 5
                        isOK = False
                        while not isOK :
                            try :
                                if i != 1:
                                    restemp = requests.get(final_url, timeout = self.timeout)
                                    conn = restemp.content

                                final_xmldict = xmltodict.parse(conn)
                                page_count = min(temp_total_count,hundred)

                                isOK = True
                                print(i, "isOk")
                            except Exception as e :
                                print(e)
                                print("retry count = ", retryCount)
                                retryCount -= 1
                            if retryCount == 0 :
                                break

                        if retryCount == 0 :
                            isPartial = True
                            print("page error")
                            continue

                        numPerror = 0

                        """ #5-4. Field 파싱 """
                        for j in range(0, page_count):
                            cnt = cnt + 1
                            
                            rawData = {}
                            rawData ['qryKeyword'] = self.keyword
                            rawData ['qryTime'] = "{}{}{}{}{}".format(dt.year, dt.month, dt.day, dt.hour, dt.minute)
                            rawData ['keyId'] = self.keyId
                            rawData['citation'] = 0
                            try :
                                if page_count == 1:
                                    item = final_xmldict['root']['result']['items']['item']
                                else:
                                    item = final_xmldict['root']['result']['items']['item'][j]
                                
                                if isinstance(item['authors']['author'], list):                                        
                                    name_list = []
                                    id_list = []
                                    name_list = [0]*len(item['authors']['author'])
                                    id_list = [0]*len(item['authors']['author'])

                                    for z in range (0, len(item['authors']['author'])):
                                        name_list[z]=item['authors']['author'][z]['name']
                                        id_list[z]=','.join(re.findall('\d+',item['authors']['author'][z]['url']))

                                    rawData['author']=";".join(name_list)
                                    rawData['author_id']=';'.join(id_list)
                                    
                                else:                                       
                                    rawData['author'] = item['authors']['author']['name']
                                    rawData['author_id'] =",".join(re.findall('\d+',item['authors']['author']['url']))                                    
                                
                                rawData['title'] = re.sub('<.+?>','',item['title'])
                                
                                if "name" in  item['publication']:
                                    rawData['journal'] = item['publication']['name']
                                else:
                                    rawData['journal'] = item['publisher']['name']

                                rawData['issue_inst'] = item['publisher']['name']

                                if "pages" in item:
                                    page_search = re.findall('\d+',item['pages'])
                                    rawData['start_page'] = page_search[0]
                                    rawData['end_page'] = page_search[1]
                                else:
                                    rawData['start_page'] = 0
                                    rawData['end_page'] = 0


                                rawData['keyId'] = self.keyId
                                rawData['id'] = 'NODE' + item['link_url'].split('NODE')[1]

                                if item['dreg_name'] is None:
                                    rawData['dreg_name']=None
                                elif 'KCI' in item['dreg_name']:
                                    rawData['dreg_name']='KCI'
                                else:
                                    rawData['dreg_name']=item['dreg_name']
                                rawData['issue_year'] = item['issue']['yymm']
                                rawData['english_title'] = None
                                rawData['issue_lang'] = None
                                rawData['paper_keyword'] = None
                                rawData['abstract'] = None
                                rawData['english_abstract'] = None
                                rawData['author_inst'] = None
                                tPro = (cnt)/int(total_count)
                                if tPro >= 1.0 :
                                    tPro = 0.99
                                rawData['progress'] = tPro

                                title = re.sub('<.+?>','',item['title'])
                                
                                title_sub = re.sub(r'[^가-힣]+','',title)
                                if len(title_sub) == 0:
                                    rawData['issue_lang'] = 'eng'
                                else:
                                    rawData['issue_lang'] = 'kor'

                                """ #5-5. kafka msg send => NTIS외에는 temp를 send (첫 결과 집합과 검색 도중 검색 결과 집합 개수가 다름)  """
                                if temp_rawData is not None:
                                    self.producer.send(self.site , value=temp_rawData)
                                
                                temp_rawData = rawData.copy()
                            except Exception as e:
                                
                                numPerror += 1
                        print(i,"번쩨 페이지 수집완료, ", (pagenum-i), ' remained', ' Num Parsing Error : ', numPerror)
                        temp_total_count = temp_total_count - 100

                    except Exception as e:
                        print(e)
                        print(i,'page error')

                END =  datetime.datetime.now()
                print("Elapsed Time : ", (END-START), pagenum)
                """ #5-5. kafka msg send => NTIS외에는 temp를 send (첫 결과 집합과 검색 도중 검색 결과 집합 개수가 다름)  """
                if temp_rawData is not None:
                    temp_rawData['progress'] = 1.0
                    temp_rawData['qryKeyword'] = self.keyword
                    temp_rawData ['qryTime'] = "{}{}{}{}{}".format(dt.year, dt.month, dt.day, dt.hour, dt.minute)
                    temp_rawData ['keyId'] = self.keyId
                    temp_rawData['isPartial'] = isPartial

                    self.producer.send(self.site, value=temp_rawData)
                else:
                    nothing['progress'] = 1.0
                    nothing['keyId'] = self.keyId
                    nothing['isPartial'] = False
                    self.producer.send(self.site, value=nothing)
                self.flush()

    else:
        """ #5-6. 검색 실패시 """
        nothing={}
        nothing['progress'] = 1.0
        nothing['keyId'] = self.keyId
        nothing['isPartial'] = False
        self.producer.send(self.site, value=nothing)
        self.flush()
        print("Error Code" + rescode)
        
    myDict = {'DBPIA': DBPIA}
