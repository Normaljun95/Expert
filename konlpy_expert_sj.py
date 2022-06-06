from pymongo import MongoClient
from bson.objectid import ObjectId
from konlpy.tag import Komoran
import gensim
from gensim.corpora.dictionary import Dictionary


client = MongoClient('mongodb://203.255.92.141:27017', authSource='admin')
ID = client['ID']
ntis_client = client['NTIS']
scienceon = client['SCIENCEON']
KCI_main = client['KCI']
DBPIA = client['DBPIA']

ntis_author = ntis_client['Author']
ntis_authorpaper = ntis_client['AuthorPapers']
ntis_rawdata = ntis_client['Rawdata']

scienceon_author = scienceon['Author']
scienceon_authorpaper = scienceon['AuthorPapers']
scienceon_rawdata = scienceon['Rawdata']

kci_author = KCI_main['Author']
kci_authorpaper = KCI_main['AuthorPapers']
kci_rawdata = KCI_main['Rawdata']

dbpia_author = DBPIA['Author']
dbpia_authorpaper = DBPIA['AuthorPapers']
dbpia_rawdata = DBPIA['Rawdata']

getBackdata = []


Domestic_cursor = ID['Domestic'].find({'keyId':754})
for data1 in Domestic_cursor:
    getBackdata.append(data1)
# print(getBackdata)


for data in getBackdata:
    getSites = list(data.keys())[5:]
    
    document_result = []
    
    for i in range(len(getSites)):
        if getSites[i] == 'DBPIA':
            dbpia_result = []
            # print(data[getSites[i]]['papers']) #[ObjectId('62391addb655744ebae43f24'), ObjectId('62391b06b655744ebae444e5')]
            for papers in data[getSites[i]]['papers']:
                dbpia_cursor = dbpia_rawdata.find({'_id':papers})
                for dbpia_data in dbpia_cursor:
                    dbpia_document = dbpia_data['title']
                    dbpia_document.replace('.', '').replace(',','').replace("'","").replace('·', ' ').replace('=','').replace('\n','').replace('■','').replace('...', '')
                    document_result.append(dbpia_document)

            # print(document_result) #["'번역문학'이라는 불가능성의 가능성", '리듬과 의미']
            
        elif getSites[i] == 'SCIENCEON':
            scienceon_result = []
            for papers in data[getSites[i]]['papers']:
                scienceon_cursor = scienceon_rawdata.find({'_id':papers})
                for scienceon_data in scienceon_cursor:
                    if type(scienceon_data['paper_keyword']) != list:
                        scienceon_document = scienceon_data['title'] + ' ' + scienceon_data['abstract'] + scienceon_data['paper_keyword'] + ' ' + scienceon_data['english_title'] + ' ' + scienceon_data['english_abstract']
                    else:
                        paper_keyword = ''
                        for j in range(len(scienceon_data['paper_keyword'])):
                            paper_keyword += scienceon_data['paper_keyword'][j] + ' '
                        scienceon_document = scienceon_data['title'] + ' ' + scienceon_data['abstract'] + paper_keyword + ' ' + scienceon_data['english_title'] + ' ' + scienceon_data['english_abstract']
                    scienceon_document.replace('.', '').replace(',','').replace("'","").replace('·', ' ').replace('=','').replace('\n','').replace('■','').replace('...', '')
                    document_result.append(scienceon_document)

        elif getSites[i] == 'KCI':
            kci_result = []
            for papers in data[getSites[i]]['papers']:
                kci_cursor = kci_rawdata.find({'_id':papers})
                for kci_data in kci_cursor:
                    kci_document = kci_data['title'] + ' ' + kci_data['english_title'] + ' ' + kci_data['abstract'] + ' ' + kci_data['english_abstract']
                kci_document.replace('.', '').replace(',','').replace("'","").replace('·', ' ').replace('=','').replace('\n','').replace('■','').replace('...', '')
                document_result.append(kci_document)
            
        elif getSites[i] == 'NTIS':
            ntis_result = []
            for papers in data[getSites[i]]['papers']:
                ntis_cursor = ntis_rawdata.find({'_id':papers})
                for ntis_data in ntis_cursor:
                    ntis_document = ntis_data['koTitle'] + ' ' + ntis_data['enTitle'] + ' ' + ntis_data['goalAbs'] + ' ' + ntis_data['absAbs'] + ' ' + ntis_data['effAbs'] + ' ' + ntis_data['koKeyword'].replace(",", " ") + ' ' + ntis_data['enKeyword'].replace(",", " ")
                ntis_document.replace('.', '').replace(',','').replace("'","").replace('·', ' ').replace('=','').replace('\n','').replace('■','').replace('...', '')
                document_result.append(ntis_document)
            
        else:
            continue
        
    # print(document_result)
    komoran = Komoran()
    
    with open('ko_stopword.txt', 'r', encoding='utf-8') as f:
        stopword = f.read()
        stopwords = stopword.split('\n')
        
    