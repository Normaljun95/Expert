from multiprocessing.dummy import freeze_support
from pymongo import MongoClient
import numpy as np
import pandas as pd
from bson.objectid import ObjectId
from konlpy.tag import Komoran, Okt
import gensim
from gensim.corpora.dictionary import Dictionary
from collections import Counter

if __name__=='__main__':
    freeze_support()

    client = MongoClient('mongodb://203.255.92.141:27017', authSource='admin')
    db = client['SCIENCEON']

    scienceOn_author = db['Author']
    scienceOn_authorPapers = db['AuthorPapers']
    scienceOn_rawData = db['Rawdata']

    author_cursor = scienceOn_author.find({'name':'유재수', 'inst': '충북대학교'})

    for author in author_cursor:
        researcher_ID = author['_id']

    authorPapers_cursor = scienceOn_authorPapers.find({'A_ID':researcher_ID})

    document_result_pre = []

    for authorPapers in authorPapers_cursor:
        papers = authorPapers['papers']
        for i in range(len(papers)):
            papersID = papers[i]
            objInstance = ObjectId(papersID)
            rawData_cursor = scienceOn_rawData.find({ "_id" : objInstance })
            for document in rawData_cursor:
                if type(document['paper_keyword']) != list:
                    new_document = document['title'] + ' ' + document['abstract'] + ' ' + document['paper_keyword'] + ' ' + document['english_title'] + document['english_abstract']
                else:
                    paper_keyword = ''
                    for j in range(len(document['paper_keyword'])):
                        paper_keyword += document['paper_keyword'][j] + ' '
                    new_document = document['title'] + ' ' + document['abstract'] + paper_keyword + ' ' + document['english_title'] + document['english_abstract']
                document_result_pre.append(new_document)
    # print(document_result_pre)
    
    document_result = ', '.join(document_result_pre)
    print(document_result)
    
    # text = re.sub('[-=+,#/\?:^$.@*\"※~&%ㆍ!』\\‘|\(\)\[\]\<\>`\'…》]','', readData)
    filtered_content = document_result.replace('.', '').replace(',','').replace("'","").replace('·', ' ').replace('=','').replace('\n','')
    # print(filtered_content)
    
    komoran = Komoran()
    # print(komoran.nouns(filtered_content))
    noun_words = komoran.nouns(filtered_content)
    
    with open('ko_stopword.txt', 'r', encoding='utf8') as f:
        stopword = f.read()
        stopwords = stopword.split('\n')
    
    pre_noun_words = set(noun_words)
    for word in pre_noun_words:
        if word in stopwords:
            while word in noun_words: noun_words.remove(word)
    c = Counter(noun_words)
    print(c.most_common(10))