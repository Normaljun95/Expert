from pymongo import MongoClient
from selenium import webdriver # 1004 수정
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import os
from bs4 import BeautifulSoup
import re
import time
import pprint
import math
import json
from json import dumps
import sys
import xlrd
import xmltodict
import requests, re


def __main__():
    ntis_crawling().start_crwal()

class ntis_crawling:
    
    def __init__(self):
        
        # 여기는 정상준 설정
        self.chrome_options = webdriver.ChromeOptions()
        self.chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])
        self.driver = webdriver.Chrome("C:\chromedriver_win32\chromedriver.exe", chrome_options=self.chrome_options)
        # 여기까지 정상준 설정
        self.author = {}
        self.paper = []
        self.papers = []
        self.info = {}
        self.infolist = []
        self.cnt = 0
        self.name = "유재수"
        self.ntis_author_path = 'C:/Users/jongwoo/selenium_test/'
        self.Affiliated = '충북대학교1'
        self.send_name = ''
        self.send_ktitle = []

#--------------------한국논문판별함수 ------------------------------------

    def isEnglishOrKorean(self,input_s):
        k_count = 0
        e_count = 0
        for c in input_s:
            if ord('가') <= ord(c) <= ord('힣'):
                k_count+=1
            elif ord('a') <= ord(c.lower()) <= ord('z'):
                e_count+=1
        return "k" if k_count>1 else "e"


#--------------------저자정보 ------------------------------------

    def main_title(self, soup):
        try:
            # print('0223')
            authorInfo = {}
            infolist = []
            thumnails  = []
            try:
                thumnail   = soup.select_one('#viewForm > div > div.riAside > div.profilePhoto > div > img')
                thumnails.append(thumnail['src'])
            except Exception as e:
                print("이미지 소스 없습니다.")
            self.info["thumnails"] = thumnails
            

            try:
                name = soup.select_one('#viewForm > div > div.riBodyWrap > header > h2').text
                name = name.lstrip()
                name = ' '.join(name.split())
                name = re.sub('[^가-힣]', '', name)
                self.info["name"] = name
                self.send_name = name
                # print(self.send_name)
            except Exception as e:
                print("이름역영이 잘못됐습니다.")


            
            try:
                for tag in soup.select('#career > section.stuCareer > div'):
                    ed = tag.get_text(separator='|li|', strip=True).split('|li|')
                    # ed = tag.get_text(strip=True, separator=" ")
                    # edu.append(ed)
                    # print(ed)
                for i in range(len(ed)):
                    ed[i] = ed[i].replace("\n","").replace("\t","")
                # print(ed)
                self.info["Education"] = ed
                
            except Exception as e:
                print(e)
                print("학력 없습니다.")

            
            
            try:
                for tag in soup.select('#career > section.jbCareer > div'):
                    ca = tag.get_text(separator='|li|', strip=True).split('|li|')
                    # carear.append(ca)
                    # print(ca)
                for i in range(len(ca)):
                    ca[i] = ca[i].replace("\n","").replace("\t","")
                # print(ca)
                self.info["carear"] = ca
            except Exception as e:
                print("커리어 없습니다.")
            print(self.info)
            print("main title 크롤 종료")

           
        except Exception as e:
            print(e)
            
    #----------------------논문 크롤---------------------------------

    def crawl_paper(self):
        try:
            self.driver.find_element_by_xpath('//*[@id="mainContents"]/section[2]/header/div[2]/button').click() # 목록 다운로드 클릭
            time.sleep(1)
            self.driver.find_element_by_xpath('//*[@id="layerItemIndividual"]').click()              # 전체선택 해제
            time.sleep(1)
            self.driver.find_element_by_xpath('//*[@id="layerItemList"]/label[1]/input').click()     # 기준년도 클릭
            time.sleep(1)
            self.driver.find_element_by_xpath('//*[@id="layerItemList"]/label[2]/input').click()     # 학술지명 클릭
            time.sleep(1)
            self.driver.find_element_by_xpath('//*[@id="layerItemList"]/label[3]/input').click()     # 논문명 클릭
            time.sleep(1)
            self.driver.find_element_by_xpath('//*[@id="layerItemList"]/label[5]/input').click()     # 저자명 클릭  
            time.sleep(1)  
         
            self.driver.find_element_by_xpath('//*[@id="layerAgreeAll"]').click()                    # 전체동의 클릭
            time.sleep(1)
            self.driver.find_element_by_xpath('//*[@id="downChk"]/button').click()                   # 다운로드 클릭
            time.sleep(5)
            print("논문 다운완료")
                           
        except Exception as e:
            print(e)
            print("논문 다운로드 선택창 오류")

        try:
            workbook = xlrd.open_workbook(self.ntis_author_path+'논문목록.xls')
            worksheet = workbook.sheet_by_index(0)
            rows = worksheet.nrows
            data = []
            for i in range(1,rows):
                a = {}
                data.append(worksheet.row_values(i)) 
                a['year'] = data[i-1][1]                # 기준년도
                a['journal'] = data[i-1][2]             # 학술지
                a['title'] = data[i-1][3]               # 논문명
                if self.isEnglishOrKorean(data[i-1][3]) == 'k':        # 한국논문인지 판별해서 self.send_ktittle 에 추가
                    self.send_ktitle.append(data[i-1][3])
                else:
                    pass
                a['au'] = data[i-1][4]                  # 저자명
                self.paper.append(a)
            
            print(self.paper)
            print('논문 엑셀데이터가져오기 성공')
            time.sleep(1)
            os.remove(self.ntis_author_path+'논문목록.xls')
            time.sleep(3)
            print('다운로드파일 삭제')

            send_name = self.send_name
            send_ktitle = self.send_ktitle
            print(send_name)
            print(send_ktitle)
            self.DBPIA_API_Advanced(send_name,send_ktitle)              # DBpia로 이름,k제목 보내고 함수호출


        except Exception as e:
            # print('여기임당3')
            print(e)
            # print("논문 엑셀 데이터 가져오는곳에서 오류")


#------------------과제 크롤-------------------------------

    def rnd_crawl(self):
        try:    
           self.driver.find_element_by_xpath('//*[@id="mainContents"]/section[1]/header/div[2]/button').click() # 목록 다운로드 클릭
           time.sleep(1)
           self.driver.find_element_by_xpath('//*[@id="layerItemIndividual"]').click()              # 전체선택 해제
           time.sleep(1)
           self.driver.find_element_by_xpath('//*[@id="layerItemList"]/label[1]/input').click()     # 기준년도 클릭
           time.sleep(1)
           self.driver.find_element_by_xpath('//*[@id="layerItemList"]/label[2]/input').click()     # 사업명 클릭
           time.sleep(1)
           self.driver.find_element_by_xpath('//*[@id="layerItemList"]/label[4]/input').click()     # 부처명 클릭  
           time.sleep(1)  
           self.driver.find_element_by_xpath('//*[@id="layerItemList"]/label[6]/input').click()     # 과제고유번호 클릭
           time.sleep(1)
           self.driver.find_element_by_xpath('//*[@id="layerItemList"]/label[17]/input').click()    # 총 연구기간 클릭 클릭
           time.sleep(1)
           
           self.driver.find_element_by_xpath('//*[@id="layerAgreeAll"]').click()                    # 전체동의 클릭
           time.sleep(1)
           self.driver.find_element_by_xpath('//*[@id="downChk"]/button').click()                   # 다운로드 클릭
           time.sleep(5)
           print("RnD과제 다운완료")

        except Exception as e:
            print(e)
            print("rnd 과제다운로드 선택창 오류")
        

        try:
            workbook = xlrd.open_workbook(self.ntis_author_path+'과제목록.xls')
            worksheet = workbook.sheet_by_index(0)
            rows = worksheet.nrows
            data = []
            for i in range(1,rows):
                a = {}
                data.append(worksheet.row_values(i)) 
                a['RND_num'] = data[i-1][0]             # 순번
                a['RND_year'] = data[i-1][1]            # 기준년도
                a['RND_title'] = data[i-1][2]           # 사업명
                # self.test.append(data[i-1][2])          # kotitle과 비교를 위해 과제명을 self.test에 추가
                a['RND_bz_name'] = data[i-1][3]         # 부처명
                a['RND_ins'] = data[i-1][4]             # 과제고유번호
                a['RND_period'] = data[i-1][5]          # 총연구기간
                self.papers.append(a)
            # print(data)
            print(self.papers)
            print('rnd엑셀데이터가져오기 성공')
            time.sleep(1)
            os.remove(self.ntis_author_path+'과제목록.xls')
            time.sleep(3)
            print('다운로드파일 삭제')


        except Exception as e:
            print(e)
            print("rnd 엑셀 데이터 가져오는곳에서 오류")
            

    def start_crwal(self):
        try:
            rnd_error_cnt =0
            start = time.time()
            self.driver.get("https://www.ntis.go.kr/ThSearchHumanDetailView.do")

            self.driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[2]/button[1]').click()

            self.driver.switch_to_window(self.driver.window_handles[1])  # 로그인창으로 전환 이거는 빼면 작동 x
            self.driver.find_element_by_xpath('/html/body/div/form/label[2]/input').send_keys("jeonjongwoo30")
            self.driver.find_element_by_xpath('/html/body/div/form/label[4]/input').send_keys("jjw01430143!") #아이디와 비밀번호
            self.driver.find_element_by_xpath('/html/body/div/form/input').click()
            time.sleep(2)

            self.driver.switch_to_window(self.driver.window_handles[0]) #혹시 모를 화면 전환. 빼도 상관없음
            time.sleep(1)
            self.driver.find_element_by_xpath('/html/body/div[4]/div[1]/div[2]/div/input[2]').click()
            time.sleep(1)
            self.driver.find_element_by_xpath('/html/body/div[4]/div[4]/div/div[2]/fieldset/div/table/tbody/tr[1]/td[1]/input').send_keys(self.name)
        #     self.driver.find_element_by_xpath('/html/body/div[4]/div[4]/div/div[2]/fieldset/div/table/tbody/tr[3]/td[1]/input').send_keys(self.idAgency)
            self.driver.find_element_by_xpath('/html/body/div[4]/div[4]/div/div[3]/input[1]').click() # 상세 검색 클릭
            time.sleep(1)
            try:
                a = self.driver.find_element_by_xpath("/html/body/div[5]/div/div/div[3]/form/div[3]/div[2]/div[1]/div/a[1]/span")
                # print('검색결과가 있습니다.')
            except Exception as e:
                print("검색한 사람이 없습니다.")
                self.driver.close
            
            
            # self.driver.find_element_by_xpath('/html/body/div[5]/div/div/div[3]/form/div[3]/div[2]/div[1]/div/a[1]').click()
            
            if a.text == self.name:
                b = self.driver.find_element_by_xpath('//*[@id="humanSearchFormDetail"]/div[3]/div[2]/div[1]/div/span[1]')
                c = b.text
                affiliatedre = re.sub('[^가-힣]', '', c)
                if self.Affiliated == affiliatedre:
                    print('있으니까 넘어갑시다.')
                    pass
                else:
                    self.cnt = 1
                    time.sleep(3)
                    print("기존저자가 아닙니다. 논문크롤합니다.")     
            else: 
                b = self.driver.find_element_by_xpath('//*[@id="humanSearchFormDetail"]/div[3]/div[2]/div[2]/div/span[1]')
                c = b.text
                affiliated = re.sub('[^가-힣]', '', c)
                if self.Affiliated == affiliated:
                    print('있으니까 넘어갑시다.')
                    pass
                else:
                    self.cnt = 1
                    time.sleep(3)
                    print("기존저자가 아닙니다. 논문크롤합니다.")  
        
            
            # self.driver.switch_to_window(self.driver.window_handles[1])
            # print("여기인가?")
            
            # soup = BeautifulSoup(self.driver.page_source, 'html.parser')

            # time.sleep(2)
            # try:
            #     self.driver.find_element_by_xpath('//*[@id="rschDevPjtBtn"]').click()
            # except Exception as e:
            #     rnd_error_cnt = 1
            #     print("R&D참여과제 버튼이 없습니다.")
            # if rnd_error_cnt != 1:
            #     print("rnd함수로이동")
            #     self.rnd_crawl()
                
            # //*[@id="searchForm"]/div[3]/div[2]/div[1]/div/span[1]
            # //*[@id="searchForm"]/div[3]/div[2]/div[2]/div/span[1]
            # //*[@id="searchForm"]/div[3]/div[2]/div[3]/div/span[1]
            # //*[@id="searchForm"]/div[3]/div[2]/div[4]/div/span[1]
            # self.author["rnd"] = self.papers
            # print(self.test)
            ### 파라미터 값이 존재하는지 검사
            # if self.kotitle in self.test:
            #     self.author["rnd"] = self.papers
            # else:
            #     print("없으니까 다음으로 넘어갑니다.")  
            #     self.cnt = 1
            #     time.sleep(3)  

              #---------------------처음에 들어간 저자가 다른 사람일 경우------------------        
            if self.cnt == 1:
                retry_paper_error_cnt = 0
                print("다시 시작")
                self.driver.switch_to_window(self.driver.window_handles[0]) #혹시 모를 화면 전환. 빼도 상관없음
                self.driver.find_element_by_xpath('/html/body/div[4]/div[1]/div[2]/div/input[2]').click()
                time.sleep(1)
                self.driver.find_element_by_xpath('/html/body/div[4]/div[4]/div/div[2]/fieldset/div/table/tbody/tr[1]/td[1]/input').clear()
                self.driver.find_element_by_xpath('/html/body/div[4]/div[4]/div/div[2]/fieldset/div/table/tbody/tr[1]/td[1]/input').send_keys(self.name)
                # self.driver.find_element_by_xpath('/html/body/div[4]/div[4]/div/div[2]/fieldset/div/table/tbody/tr[3]/td[1]/input').clear()
                # self.driver.find_element_by_xpath('/html/body/div[4]/div[4]/div/div[2]/fieldset/div/table/tbody/tr[3]/td[1]/input').send_keys(self.idAgency)
                self.driver.find_element_by_xpath('/html/body/div[4]/div[4]/div/div[3]/input[1]').click()
                time.sleep(1)    
                self.driver.find_element_by_xpath('/html/body/div[5]/div/div/div[3]/form/div[3]/div[2]/div[1]/div/a[1]').click()
                self.driver.switch_to_window(self.driver.window_handles[1])
                # soup = BeautifulSoup(self.driver.page_source, 'html.parser')
                
                time.sleep(2)
                self.driver.find_element_by_xpath('//*[@id="rschDevPjtBtn"]').click()       #rnd 파트
                print("rnd함수로이동")
                self.rnd_crawl()
                # self.author["rnd"] = self.papers
                # print(self.test)
                self.author["rnd"] = self.papers

                self.driver.find_element_by_xpath('//*[@id="edubgCareerBtn"]').click()       # main_title
                html = self.driver.page_source
                soup = BeautifulSoup(html, 'html.parser')
                self.main_title(soup)
                # print("title" , self.author)
                
                
                try:
                    self.driver.find_element_by_xpath('//*[@id="paperBtn"]').click()
                except Exception as e:
                    retry_paper_error_cnt =1
                    print("논문 버튼이 없습니다.")

                if retry_paper_error_cnt != 1:                  #여기서부터는 논문파트 
                    self.crawl_paper()
                try:
                    self.author["reference"] = self.paper
                    # print(self.author)
                    # print(self.send_name)
                    # print(self.send_ktitle)
                except Exception as e:
                    print(e)

                    
          #---------------------정상실행일때------------------        
            else:
                paper_error_cnt = 0
                # time.sleep(10)
                # self.main_title(soup)


                print('/?/?/?/?/')

        except Exception as e:
            print(e)
            print("start crawling 오류")
            # time.sleep(100000)


    # --------------------------------Dbpia 코드---------------------------------------
    def DBPIA_API_Advanced(self,send_name,send_ktitle):
        count = 0
        for i in range(0,len(send_ktitle)):
            input_name = send_name
            apiKeyword = send_ktitle[i]
            print('이름: '+ input_name + ' / 제목: ' + apiKeyword)

            url = "http://api.dbpia.co.kr/v2/search/search.xml"
            queryParams = "?" + "key=" + "785daf59cf68133cc5df9a87a8d8f6c9" + "&target="+ "se" + "&searchall=" + apiKeyword +"&pagecount="+"1"    
            url = url + queryParams
            # print(url)
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
                try:
                    item = xmldict['root']['result']['items']['item']
                    
                    if isinstance(item['authors']['author'], list):
                        name_list = []
                        id_list = []
                        name_list = [0]*len(item['authors']['author'])
                        id_list = [0]*len(item['authors']['author'])
                        
                        for z in range(0, len(item['authors']['author'])):
                            name_list[z]=item['authors']['author'][z]['name']
                            try:
                                id_list[z]=','.join(re.findall('\d+',item['authors']['author'][z]['url']))
                            except:
                                id_list[z]=''
                            if input_name in name_list[z]:
                                rawData['author'] = name_list[z]
                                rawData['author_id'] = id_list[z]
                    else:
                        rawData['author'] = item['authors']['author']['name']
                        rawData['author_id'] =",".join(re.findall('\d+',item['authors']['author']['url']))

                    rawData['title'] = re.sub('<.+?>','',item['title'])
                    rawData['issn'] = item['publication']['issn']
                    print(rawData)
                except:
                    nothing = {}
                    nothing['progress'] = 1.0
                    nothing['title'] = apiKeyword
                    nothing['isPartial'] = False
                    print("Error Code /검색결과없음/ " + str(rescode))           # url정상접속으로 rescode가 200이지만 검색결과가 없어서 엑셉트로 빠진경우
                    count += 1
                    print('노검색결과 count= '+ str(count))
                                 
            else:
                nothing = {}
                nothing['progress'] = 1.0
                nothing['title'] = apiKeyword
                nothing['isPartial'] = False
                print("Error Code /url접속문제/ " + str(rescode))               # url접속오류로 rescode가 500인경우
                count += 1
                print('노검색결과 count= '+ str(count))
                
        print('총노검색결과 count= ' + str(count))
        
    # ----------------------------------------------------------------------------

__main__()