# import html
# chan = html.unescape("Kim &#x00B7; Lee")
# print(chan)


# import re
# sentence = '한국<!HS>재료<!HE>학회'
# sentence1 = re.sub('<.+?>', '', sentence)
# print(sentence1)


# a = [[1,2], [3,4,5]]
# a = sum(a, [])
# print(a)

# lst = ["a", "b", "c"]
# print(";".join(lst))
# print(lst[-1])

# text = "가능성"
# text = text.rstrip("을""에서""를""에")
# print(text)
# _pyear = []
# _pyear.append(int('2022'[0:4]))
# print(_pyear)

pYears = [[2021, 2021], [2021], [2022], [2021], [2022], [2021], [2021], [2021], [2021], [2021], [2021], [2021], [2021], [2021], [2021], [2021], [2021, 2021], [2021], [2021, 2021], [2022, 2022], [2021], [2021], [2021], [2021], [2022, 2021], [2022, 2022], [2021], [2021], [2021], [2021], [2021], [2021], [2021], [2022], [2022, 2022, 2022, 2022, 2021], [2022], [2021], [2021], [2021], [2021], [2022, 2021], [2021], [2021], [2021], [2022, 2022], [2022], [2021], [2021], [2021], [2021], [2021], [2022, 2022], [2022], [2022, 2021], [2022], [2021], [2021], [2021], [2021], [2021], [2021], [2021], [2021], [2021], [2022], [2022], [2021], [2021], [2022], [2021], [2021], [2021], [2022], [2021], [2022, 2022], [2022], [2021], [2021], [2022], [2022], [2021], [2021], [2021], [2022], [2022], [2022], [2021], [2022, 2022], [2021], [2021], [2021], [2021], [2021], [2021], [2021], [2021], [2021], [2022], [2021], [2021]]

for i in range(len(pYears)):
    # print(pYears[i])
    # print(len(pYears[i]))
    year_avg = round(sum(pYears[i]) / len(pYears[i]))
    print(year_avg)


# lst = ["가능성", "가능성", "가능성"]
# r = []
# for l in lst:
#     r.append(l)
# print(r)


# from bson.objectid import ObjectId
# from pymongo import MongoClient

# client = MongoClient('mongodb://203.255.92.141:27017', authSource='admin')
# ID = client['ID']

# ID_coopList = ID['coopList']

# doc1 = {
#   "_id" : ObjectId("62578968d7345e9e2ec45e36"),
#   "fid" : 0,
#   "keyId" : 777,
#   "name" : "유재수",
#   "inst" : "충북대학교",
#   "SCIENCEON" : {
#     "inst" : "상명대학교 정보보안공학과",
#     "A_id" : ["s1560959"],
#     "papers" : [ObjectId("62578947eb14f8f17f29fb49")],
#     "oriInst" : "상명대학교"
#   },
#   "KCI" : {
#     "inst" : "상명대학교",
#     "A_id" : ["s378600"],
#     "papers" : [ObjectId("6257893b9592a1f18a29f7ec")],
#     "oriInst" : "상명대학교"
#   }
# }

# coop_cursor = ID['coopList'].find({'name': doc1['name'], 'college': doc1['inst']})

# # for c in coop_cursor:
# #     print(c['ngvCoop']) 

# def ngv_Coop(doc1):
#     for coop_cursor in ID['coopList'].find({'name': doc1['name'], 'college': doc1['inst']}):
#         print(coop_cursor)
    
# ngv_Coop(doc1)

# from multiprocessing.dummy import freeze_support
# from pymongo import MongoClient
# import pandas as pd
# import numpy as np
# from bson.objectid import ObjectId

# import nltk
# from nltk.stem import WordNetLemmatizer, SnowballStemmer
# import gensim
# from nltk.tokenize import word_tokenize
# from nltk.tag import pos_tag
# from gensim.corpora.dictionary import Dictionary
# # nltk.download('punkt')
# # nltk.download('wordnet')


# if __name__=='__main__':
#     freeze_support()

#     client = MongoClient('mongodb://203.255.92.141:27017', authSource='admin')
#     db = client['SCIENCEON']
#     # print(db.list_collection_names())

#     scienceOn_author = db['Author']
#     scienceOn_authorPapers = db['AuthorPapers']
#     scienceOn_rawData = db['Rawdata']

#     author_cursor = scienceOn_author.find({'name':'유재수', 'inst': '충북대학교'})

#     for author in author_cursor:
#         researcher_ID = author['_id']

#     authorPapers_cursor = scienceOn_authorPapers.find({'A_ID':researcher_ID})
    
#     document_result = []
    
#     for authorPapers in authorPapers_cursor:
#         papers = authorPapers['papers']
#         for i in range(len(papers)):
#             papersID = papers[i]
#             objInstance = ObjectId(papersID)
#             rawData_cursor = scienceOn_rawData.find({ "_id" : objInstance })
#             for document in rawData_cursor:
#                 if type(document['paper_keyword']) != list:
#                     new_document = document['title'] + ' ' + document['english_title'] + ' ' + document['abstract'] + ' ' + document['paper_keyword'] + ' ' + document['english_abstract']
#                 else:
#                     paper_keyword = ''
#                     for j in range(len(document['paper_keyword'])):
#                         paper_keyword += document['paper_keyword'][j] + ' '
#                     new_document = document['title'] + ' ' + document['english_title'] + ' ' + document['abstract'] + paper_keyword + document['english_abstract']
#                 document_result.append(new_document)

#     divide_result = []
    
#     for text in document_result:
#         tokenized_text = word_tokenize(text)
#         print(tokenized_text)
#         # for word, pos in tokenized_text:
#         #     if (pos == 'NN' or pos == 'NNP' or pos == 'NNS' or pos == 'NNPS'):
#         #         print(word)
        
#         # divide_result.append(tokenized_text)
#     # print(divide_result)

#     # dictResult = Dictionary(divide_result)
#     # print(dictResult.token2id)

#     # bow_corpus = [dictResult.doc2bow(doc) for doc in divide_result]
#     # print(bow_corpus)

#     # lda_model = gensim.models.LdaMulticore(corpus=bow_corpus, id2word=dictResult, num_topics=5)

#     # for idx, topic in lda_model.print_topics(-1):
#     #     print('Topic: {} \nwords: {}'.format(idx, topic))