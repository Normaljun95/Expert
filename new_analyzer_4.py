from email.mime import base
import re, math,threading, datetime
from typing import List
import pymongo
from sklearn.feature_extraction.text import TfidfVectorizer
from multiprocessing import Pool
from pymongo import MongoClient
from numpy.linalg import norm
from threading import Thread
import scipy.sparse as sp
from time import sleep
from numpy import dot
import numpy as np
from multiprocessing.dummy import freeze_support
import gensim
from gensim.corpora.dictionary import Dictionary
import nltk
from collections import Counter

from itertools import chain
from collections import defaultdict


class factor_integration(threading.Thread):
    def __init__(self, start, num_data, fid, keyID, stop_words):
        threading.Thread.__init__(self)
        # 받아오는 값
        self.keyId          = keyID
        self.fid            = fid
        self.start_index    = start # 시작위치
        self.end            = num_data # 총 데이터 >> 이걸 100개씩 나눠서 실행시켜야함.

        self.client         = MongoClient('203.255.92.141:27017', connect=False)
        self.ID             = self.client['ID']
        self.PUBLIC         = self.client['PUBLIC']
        self.new_max_factor = self.PUBLIC['new_factor']

        self.WOS            = self.client['WOS']
        self.SCOPUS         = self.client['SCOPUS']

        self.stop_words     = stop_words

        self.rank_inst      = self.PUBLIC['rank_inst']
        self.FilterCategory = self.PUBLIC['FilterCategory']

        if self.fid == 0:
            paper_inst          = None
            project_inst        = None
            for doc in self.FilterCategory.find({'keyId' : self.keyId, 'fId' : self.fid}):
                paper_inst      = doc['paper']['inst']['list']

            self.base_insts     = defaultdict(list)

            for k, v in paper_inst.items():
                self.base_insts[k].append(v)
            for k, v in self.base_insts.items():
                self.base_insts[k] = sum(v)

            self.rank_inst.insert_one({'keyId' : self.keyId, 'Insts' : self.base_insts})

        self.KCI  = self.client.PUBLIC.KCI
        self.SCI  = self.client.PUBLIC.SCI
        self.kDic = {}
        self.sDic = {}
        for doc in self.KCI.find({}) :
            self.kDic[doc['name']] = doc['IF']
        for doc in self.SCI.find({}) :
            self.sDic[doc['name']] = doc['IF']

    def run(self):
        all_count   = self.end - self.start_index
        dataPerPage = 100
        allPage     = math.ceil(all_count/dataPerPage)

        temp = []
        for i in range(allPage):

            qual    = []
            sCount  = self.start_index + (i*dataPerPage)
            lCoount = min(dataPerPage, self.end - sCount )
            data, object_data, base_data = self.getBackdata(sCount, lCoount, self.fid, self.keyId)

            (pYears, keywords, _WOSQtyBackdata, _WOSContBackdata, _WOSCoopBackdata) = self.getRawBackdata(data,self.keyId, object_data)['WOS']
            (_SCOPUSQtyBackdata, _SCOPUSContBackdata, _SCOPUSCoopBackdata)  = self.getRawBackdata(data,self.keyId, object_data)['SCOPUS']
            (querykey, numPapers_list, totalcitation_list, recentYear_list, totalcoop_list, coopList) = self.getRawBackdata(data,self.keyId, object_data)['etc']
            temp.append(self.getRawBackdata(data,self.keyId, object_data)['insts_to_update'])

            for k in range(len(self.scoquality(_SCOPUSQtyBackdata))):
                qual.append([self.scoquality(_WOSQtyBackdata)[k] + self.scoquality(_SCOPUSQtyBackdata)[k]])

            accuracy = self.acc(keywords, querykey)
            lda_ls = self.lda(keywords)
            # print(pYears)
            recentness, lct_list = self.recentness(pYears)
            
            self.insert_max_factor(qual, accuracy, totalcoop_list, recentness, self.keyId)

            real_final_last_data = []
            count_base_data      = 0

            for doc2 in base_data:

                doc2['numProjects']   = 0
                doc2['numPapers']     = numPapers_list[count_base_data]
                doc2['totalCitation'] = totalcitation_list[count_base_data]
                doc2['recentYear']    = recentYear_list[count_base_data]
                doc2['totalCoop']     = totalcoop_list[count_base_data]
                doc2['score']         = 0
                doc2['coopList']      = coopList[count_base_data]
                doc2['LDA']           = lda_ls[count_base_data]


                factor                = {}
                factor['interQual']   = qual[count_base_data][0]
                factor['lct']         = lct_list[count_base_data] / 2 ## 최신성 최대 0.5점
                factor['acc']         = accuracy[count_base_data]
                factor['coop']        = totalcoop_list[count_base_data]
                factor['qunt']        = recentness[count_base_data] # 정규화 후
                doc2['factor']        = factor
                count_base_data       += 1
                real_final_last_data.append(doc2)

            self.ID['test'].insert_many(real_final_last_data)

        tmp = [ _.items() for _ in temp ]
        insts_to_update_dict = defaultdict(list)
        for k, v in chain.from_iterable(tmp):
            insts_to_update_dict[k].append(v)
        for k, v in insts_to_update_dict.items():
            insts_to_update_dict[k] = sum(v)

        if self.fid == 0 :
            for k, v in insts_to_update_dict.items():
                try:
                    self.rank_inst.update_one(
                        { 'keyId'  : self.keyId },
                        { '$inc'   : {f'Insts.{k}' : v } },
                        upsert=True
                    )
                except Exception as e:
                    print(e)
                    continue


    def insert_max_factor(self, qual, accuracy, coop, pYears, keyID):
        interQual  = max(map(lambda x:x[0], qual))
        accuracy   = max(accuracy)
        coop       = max(coop)
        recentness = max(pYears)
        keyId      = keyID

        # 정규화를 하기 위한 각 factor당 max값을 넣어줌.
        self.new_max_factor.update_one({"keyId" : keyId}, {'$max':{"interQual":interQual, "accuracy":accuracy , "recentness":recentness , "coop":coop }})

    def getBackdata(self, i, dataPerPage, fid, keyID):
        self.keyID    = keyID

        objectid_data = []
        getBackdata   = []
        base_data     = self.ID['International'].find({"keyId":keyID, "fid":fid}).skip(i).limit(dataPerPage)
        base_data1    = []
        for doc in base_data:
            base_data1.append(doc)
            papersNumber   = 0
            getBackdataDic = {}
            objectid_data.insert(0,(doc['_id']))
            if ("WOS" in doc):
                getBackdataDic['WOS'] = doc['WOS']['A_id']
                getBackdataDic['WOS papers'] = doc['WOS']['papers']
                papersNumber += len(doc['WOS']['papers'])
            else:
                getBackdataDic['WOS'] = None
                getBackdataDic['WOS papers'] = []

            if ("SCOPUS" in doc):
                getBackdataDic['SCOPUS'] = doc['SCOPUS']['A_id']
                getBackdataDic['SCOPUS papers'] = doc['SCOPUS']['papers']
                papersNumber += len(doc['SCOPUS']['papers'])
            else:
                getBackdataDic['SCOPUS'] = None
                getBackdataDic['SCOPUS papers'] = []

            getBackdataDic['number'] = papersNumber
            getBackdata.append(getBackdataDic)
        return  getBackdata, objectid_data, base_data1

    def getRawBackdata(self, getBackdata, keyID, object_data):

        pYears       = [] #WOS & SCOPUS
        keywords     = [] #WOS & SCOPUS

        authorInsts4 = [] #WOS
        authors4     = [] #WOS
        issueInsts4  = [] #WOS
        issueLangs4  = [] #WOS
        citation4    = [] #WOS
        WOS_id       = [] #WOS

        authorInsts5 = [] #SCOPUS
        authors5     = [] #SCOPUS
        issueInsts5  = [] #SCOPUS
        issueLangs5  = [] #SCOPUS
        citation5    = [] #SCOPUS
        SCOPUS_id    = [] #SCOPUS


        querykey     = []

        totalcitation_list = []
        recentYear_list    = []
        totalcoop_list     = []
        numPapers_list     = []
        coopList           = []

        insts_to_update    = {}

        for i in range(len(getBackdata) - 1, -1, -1):

            coopname      = []
            totalcitation = 0
            recentYear    = []
            totalcoop     = 0
            numPapers     = 0

            _pYear        = [] #WOS & SCOPUS
            _keywords     = [] #WOS & SCOPUS

            _keyword4     = [] #WOS
            _authorInsts4 = [] #WOS
            _authors4     = [] #WOS
            _issueInsts4  = [] #WOS
            _issueLangs4  = [] #WOS
            _citation4    = [] #WOS
            _WOS_id       = [] #WOS

            _keyword5     = [] #SCOPUS
            _authorInsts5 = [] #SCOPUS
            _authors5     = [] #SCOPUS
            _issueInsts5  = [] #SCOPUS
            _issueLangs5  = [] #SCOPUS
            _citation5    = [] #SCOPUS
            _SCOPUS_id    = [] #SCOPUS

            if (getBackdata[i]['WOS'] != None):

                WOS_id.insert(0, getBackdata[i]['WOS'])

                for doc in self.WOS['Rawdata'].find({"keyId": keyID, "_id": {"$in" : getBackdata[i]['WOS papers']}}):
                    originalName = doc['author_inst']
                    originalName1 = originalName.split(';')

                    pcnt = len(originalName1) - 1
                    cnt = 0
                    for n in range(pcnt):
                        coopname.append(originalName1[n])

                    if cnt != pcnt and cnt >= 1:
                        totalcoop += 1
                    for j in doc['qryKeyword']:
                        if j not in querykey:
                            querykey.append(j)

                    _keyword4.append(doc['title'])
                    _keyword4.append(doc['paper_keyword'])
                    _keyword4.append(doc['abstract'])
                    # _pYear.append(int(doc['issue_year'][0:4]))
                    _pYear.append(int(doc['issue_year']))
                    # recentYear.append(int(doc['issue_year'][0:4]))
                    recentYear.append(int(doc['issue_year']))
                    _authorInsts4.append(doc['author_inst'])
                    _authors4.append(doc['author_id'])
                    _issueInsts4.append(doc['issue_inst'])
                    _issueLangs4.append(doc['issue_lang'])

                    _citation4.append(int(doc['citation']))
                    totalcitation += int(doc['citation'])
                    numPapers += 1

                    temp_list = doc['author_inst'][:-1].split(';')
                    for _ in temp_list:
                        if _ != temp_list[-1]:
                            insts_to_update[_] = insts_to_update.get(_, 0) + 1

                if len(_keyword4) != 0:
                    authorInsts4.insert(0, _authorInsts4)
                    authors4.insert(0, _authors4)
                    issueInsts4.insert(0, _issueInsts4)
                    _keywords.insert(0,_keyword4)
                    issueLangs4.insert(0,_issueLangs4)
                    citation4.insert(0,_citation4)
            else:
                issueInsts4.insert(0, _issueInsts4)
                issueLangs4.insert(0,_issueLangs4)
                citation4.insert(0,_citation4)
                authors4.insert(0,"WOS"+str(i))
                WOS_id.insert(0,"WOS"+str(i))
                authorInsts4.insert(0,_authorInsts4)

            if (getBackdata[i]['SCOPUS'] != None):

                SCOPUS_id.insert(0, getBackdata[i]['SCOPUS'])

                for doc in self.SCOPUS['Rawdata'].find({"keyId": keyID, "_id": {"$in" : getBackdata[i]['SCOPUS papers']}}):
                    numPapers += 1
                    originalName = doc['originalName']
                    originalName2 = originalName.split(';')

                    pcnt = len(originalName2)-1
                    cnt = 0
                    for m in range(pcnt):
                        coopname.append(originalName2[m])

                    if cnt != pcnt and cnt >= 1:
                        totalcoop += 1

                    for j in doc['qryKeyword']:
                        if j not in querykey:
                            querykey.append(j)

                    _keyword5.append(doc['title'])
                    _keyword5.append(doc['paper_keyword'])
                    _keyword5.append(doc['abstract'])
                    # _pYear.append(int(doc['issue_year'][0:4]))
                    _pYear.append(int(doc['issue_year']))
                    # recentYear.append(int(doc['issue_year'][0:4]))
                    recentYear.append(int(doc['issue_year']))
                    _authorInsts5.append(doc['author_inst'])
                    _authors5.append(doc['author_id'])
                    _issueInsts5.append(doc['issue_inst'])
                    _issueLangs5.append(doc['issue_lang'])

                    _citation5.append(int(doc['citation']))
                    totalcitation += int(doc['citation'])

                    temp_list = doc['originalName'][:-1].split(';')
                    for _ in temp_list:
                        if _ != temp_list[-1]:
                            insts_to_update[_] = insts_to_update.get(_, 0) + 1

                if len(_keyword5) != 0:
                    authorInsts5.insert(0, _authorInsts5)
                    authors5.insert(0, _authors5)
                    issueInsts5.insert(0, _issueInsts5)
                    _keywords.insert(0,_keyword5)
                    issueLangs5.insert(0,_issueLangs5)
                    citation5.insert(0,_citation5)
            else:
                issueInsts5.insert(0, _issueInsts5)
                issueLangs5.insert(0,_issueLangs5)
                citation5.insert(0,_citation5)
                authors5.insert(0,"SCOPUS"+str(i))
                SCOPUS_id.insert(0,"SCOPUS"+str(i))
                authorInsts5.insert(0,_authorInsts5)

            totalcoop_list.insert(0,totalcoop)
            coopname = list(set(coopname))
            for num, q in enumerate(coopname):
                if coopname[num] == "":
                    coopname.pop(num)
            coopList.insert(0, coopname)

            if recentYear == []:
                recentYear_list.insert(0, 0)
            else:
                recentYear_list.insert(0,max(recentYear))
            totalcitation_list.insert(0,totalcitation)
            numPapers_list.insert(0,numPapers)
            pYears.insert(0,_pYear)
            keywords.insert(0,_keywords)

        return {'WOS' : [pYears, keywords, {'issueInsts' : issueInsts4, 'issueLangs' : issueLangs4, 'citation' : citation4}, {'authors' : authors4, 'A_ID' : WOS_id}, authorInsts4],
                'SCOPUS' : [{'issueInsts' : issueInsts5, 'issueLangs' : issueLangs5, 'citation' : citation5}, {'authors' : authors5, 'A_ID' : SCOPUS_id}, authorInsts5],
                'etc' : [querykey, numPapers_list, totalcitation_list, recentYear_list, totalcoop_list, coopList],
                'insts_to_update' : insts_to_update}

    def recentness(self, pYears):
        dt = datetime.datetime.now()
        rct_list = []
        lct_list = []
        for i in range(len(pYears)):
            rct = 0
            lct = 0
            try:
                # year_avg = sum(pYears[i] / len(pYears[i]))
                year_avg = sum(pYears[i]) / len(pYears[i])
                
                if year_avg >= int(dt.year)-2:
                    lct = 1
                elif int(dt.year)-15 < year_avg <= int(dt.year)-3:
                    lct = max(round((1-(int(dt.year)-3-year_avg)*0.1),2), 0)

            except Exception as e:
                rct_list.append(0)
                lct_list.append(0)
                continue

            for j in range(len(pYears[i])):
                if (year_avg - 5 < pYears[i][j] < year_avg + 5):
                    rct += 1

            if len(pYears[i]) != 0:
                rct_list.append(rct)
                lct_list.append(lct)
            else:
                rct_list.append(0)
                lct_list.append(0)

        return rct_list, lct_list

    def coop(self, _coopBackdata):
        """
        @ Method Name     : coop
        @ Method explain  : 협업도 계산 함수
        @ _contBackdata   : getRawBackdata 함수에서 mngIds, A_ID 값을 가지고 있는 변수
        """
        oemList = ["Hyundai", "Kia","Toyota","Honda","Nissan","General Motors", "Chevrolet","Ford motor", "Volkswagen", "Audi", "BMW", "Bayerische Motoren Werke", "Mercedes-Benz", "daimler", "Volvo", "Renault", "Jaguar", "Acura", "Mazda", "Subaru", "Suzuki", "Isuzu","Daihatsu","Peugeot","Mclaren", "Bugatti", "Rolls Royce", "Bentley", "Aston Martin", "Land Rover", "Lotus","Lexus",   "Infiniti", "Datson", "Mitsubishi", "Mitsuoka","Great Wall","Cadillac", "Tesla", "Jeep", "Dodge", "Chrysler","Porsche", "Opel", "Borgward", "Gumfut", "FIAT", "Ferrari", "Lamborghini", "Maserati","Peugeot"]
        score = []
        for i in range(len(_coopBackdata)):
            point = 0
            for insts in _coopBackdata[i]:
                if insts != None :
                    for oem in oemList :
                        if oem in insts:
                            point = point + 1
                            break
            score.append(point)
        return score

    def scoquality(self, _qtyBackdata):
        issueInsts = _qtyBackdata['issueInsts']
        issueLangs = _qtyBackdata['issueLangs']
        citation   = _qtyBackdata['citation']

        IF = []
        for i in range(len(issueInsts)):
            tempIF = 0
            for j in range(len(issueInsts[i])):
                tempIFIF = 0
                n = 1
                if issueLangs[i][j] == 'kor':
                    if isinstance(issueInsts[i][j], str) :
                        tempIFIF = self.kDic.get(issueInsts[i][j], 0)
                else:
                    if isinstance(issueInsts[i][j], str) :
                        tempIFIF = self.sDic.get(issueInsts[i][j], 0)
                    n = 3

                tempIF += math.log(((citation[i][j]*n)+1) * (tempIFIF+1.1))
            IF.append(tempIF)
        return IF

    def acc(self, keywords, querykey):
        rtv = [0 for r in range(len(keywords))]
        for i in range(len(keywords)):
            temp = calAcc(keywords[i], querykey, self.stop_words)
            if temp == 0.0 :
                rtv[i] = 0.02
            else :
                rtv[i] = temp
        return rtv

    def lda(self, keywords):
        rtv = [0 for r in range(len(keywords))]
        for i in range(len(keywords)):
            temp = LDA_model(keywords[i], self.stop_words)
            rtv[i] = temp
        return rtv



def calAcc(keywords, querykey, stop_words):
    # print("calAcc")
    flat_list = []
    for sublist in keywords :
        for item in sublist :
            if item is not None and item != 'None' and item != "" and isinstance(item, str) :
                flat_list.append(
                    " ".join(
                        [
                            word for word, pos in nltk.pos_tag(nltk.word_tokenize(item))
                            if (pos == 'NN' or pos == 'NNP' or pos == 'NNS' or pos == 'NNPS')
                            if word not in stop_words and len(word) > 2
                        ]
                    )
                )

    if len(flat_list) == 0 :
        return 0
    # print(flat_list)

    qs = querykey
    qs = [_qs for _qs in qs if len(_qs) >= 2]
    tfidf_vectorizer = TfidfVectorizer(analyzer='word', ngram_range=(1, 1))
    # print(querykey)
    tfidf_vectorizer.fit(querykey)

    arr = tfidf_vectorizer.transform(flat_list).toarray()
    qrytfidf = [1] *len(qs)
    if sum(arr[np.argmax(arr.sum(axis=1))]) != 0:
        return cos_sim(arr[np.argmax(arr.sum(axis=1))], qrytfidf)
    else:
        return 0

def cos_sim(A, B):
    return dot(A, B)/(norm(A)*norm(B))

def LDA_model(keywords, stop_words):

    flat_list = []
    for sublist in keywords:
        for item in sublist:
            if item is not None and item != 'None' and item != "" and isinstance(item, str) :
                    flat_list.append([word for word, pos in nltk.pos_tag(nltk.word_tokenize(item)) if (pos.startswith('N')) if word not in stop_words and len(word) > 2])
    dictResult = Dictionary(flat_list)
    bow_corpus = [dictResult.doc2bow(document) for document in flat_list]
    lda_model = gensim.models.LdaMulticore(corpus=bow_corpus, id2word=dictResult, num_topics=5)

    topic_list = []
    topic_result = []
    for idx in range(5):
        topic = lda_model.show_topic(idx, 5)
        for word, score in topic:
            topic_list.append(word)
    count_topic = Counter(topic_list).most_common(n=5)
    for t, n in count_topic:
        topic_result.append(t+";"+str(n))
    return topic_result
