from multiprocessing.dummy import freeze_support
from pymongo import MongoClient
import numpy as np
import pandas as pd
from bson.objectid import ObjectId
from konlpy.tag import Komoran, Okt, Hannanum
import gensim
from gensim.corpora.dictionary import Dictionary


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

    document_result = []

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
                new_document.replace('.', '').replace(',','').replace("'","").replace('·', ' ').replace('=','').replace('\n','')
                document_result.append(new_document)
    print(document_result)

    komoran = Komoran()
    hannanum = Hannanum()
    
    with open('ko_stopword.txt', 'r', encoding='utf8') as f:
        stopword = f.read()
        stopwords = stopword.split('\n')
        
    divide_result = []

    for text in document_result:
        noun_words = komoran.nouns(text)
        for word in noun_words:
            if word in stopwords:
                while word in noun_words: noun_words.remove(word)
        divide_result.append(noun_words)
    # print(divide_result) #preprocessed_docs

    dictResult = Dictionary(divide_result)
    # print(dictResult.token2id) #dictionary

    bow_corpus = [dictResult.doc2bow(doc) for doc in divide_result]
    # print(bow_corpus)

    # lda_model = gensim.models.LdaMulticore(corpus=bow_corpus, id2word=dictResult, num_topics=5)
    
    # for idx in range(5):
    #     # print(idx)
    #     # print("Topic_num: {} ".format(idx))
    #     topic_set = lda_model.show_topic(idx, 5)
    #     print("Topic: {} \nWords: {}".format(idx, topic_set))
    #     # print(topic_set)