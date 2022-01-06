from pymongo import MongoClient

client = MongoClient('mongodb://203.255.92.141:27017', authSource='admin')
scion_exfa = client['SCIENCEON']['ExpertFactor']
scion_aut = client['SCIENCEON']['Author']

ntis_exfa = client['NTIS']['ExpertFactor']
ntis_aut = client['NTIS']['Author']
ntis_row = client['NTIS']['Rawdata']

dbpia_exfa = client['DBPIA']['ExpertFactor']
dbpia_aut = client['DBPIA']['Author']

id_domestic = client['ID']['Domestic']

keyid = 588 #input

scion_key_query = scion_exfa.find({ 'keyId' : keyid })
ntis_key_query = ntis_exfa.find({ 'keyId' : keyid })
dbpia_key_query = dbpia_exfa.find({ 'keyId' : keyid })

key_querys = [scion_key_query, ntis_key_query, dbpia_key_query]
#key_querys = [ntis_key_query]
auts = [scion_aut, ntis_aut, dbpia_aut]
site = ['Scienceon', 'NTIS', 'DBPIA']

Aid = []
a_id = []
all_name_inst = []
all_name = []
all_inst = []
all_site = []
reCopy = []
reCopy_site = []
reCopy_aid = []
Answer_list = []
Answer_dict = {}

for i in range(len(key_querys)):
    #print(key_querys[i])
    for key_query in key_querys[i]:
        Aid = []

        a_id.append(key_query['A_ID'])

        if site[i] == 'NTIS' : 
            # if "11638621" == a_id[-1] :
            #print("check")
            ntis_key_query1 = ntis_row.find_one({'$and':[{'keyId':keyid},{'mngId':a_id[-1]}]})
            #print(ntis_key_query1)

            if ntis_key_query1 == None :
            #print("check2")
                continue
            else :
                Aid = key_query['A_ID']
        elif site[i] == 'Scienceon' :
            Aid.append(key_query['A_ID'])
        elif site[i] == 'DBPIA' :
            Aid.append(key_query['A_ID'])

        aut_query = auts[i].find_one({'_id':key_query['A_ID']})
        #print(aut_query)

        #all_name_inst.append(aut_query['name'] + '/' + aut_query['inst'])
        all_name.append(aut_query['name'])
        all_inst.append(aut_query['inst'].replace("(주) ", "").replace("(주)", "").split(' ')[0])
        all_site.append(site[i])
        
        Answer = {'name' : all_name[-1], site[i] : {'inst' : all_inst[-1], 'A_id': Aid} }
   
        if all_name[-1] not in Answer_dict and all_name[-1]+'0' not in Answer_dict :
            Answer_dict[all_name[-1]] = Answer
         #   print("insert")
        else :
            
            count = 0
            flag = True
            while flag :
                temp = None 
                tempName = all_name[-1]

              
                if tempName in Answer_dict :        # 이름 으로만 key가ㅣ 존재         
                    temp = Answer_dict[tempName]
                    flag = False
                else :
                    tempName = all_name[-1]+str(count)  # 이름 + 숫자로 key가ㅣ 존재
                    if tempName not in Answer_dict :
                        flag = False 
                       # print(tempName)
                        break
                    temp = Answer_dict[tempName]
                      
                for key in temp.keys() : # 사이트 돌면서
                    if key != 'name' : 
                        src = ""
                        tgt = ""

                        if len(all_inst[-1]) >= len(temp[key]['inst']):
                            src = temp[key]['inst']
                            tgt = all_inst[-1]

                        elif len(all_inst[-1]) < len(temp[key]['inst']):
                            src = all_inst[-1]
                            tgt = temp[key]['inst']
                        # if tempName == '김영미' :
                        #     print(all_inst[-1], temp[key])
                        #     print(ssrc, ttgt)

                        if key == site[i] :# 사이트가 동일할때
                            if temp[key]['inst'] == all_inst[-1] or (src != "" and src in tgt) :  # 소속 같을때
                                flag = False
                                break
                            elif all_name[-1]+str(count+1) not in Answer_dict :
                                Answer_dict[all_name[-1]+str(count+1)] = Answer
                                #if tempName != all_name[-1] :
                                if tempName == all_name[-1]:
                                    Answer_dict[all_name[-1]+'0'] = temp
                                    del Answer_dict[all_name[-1]]

                        else :# 사이트가 다를때 
                            if temp[key]['inst'] == all_inst[-1] or (src != "" and src in tgt):  # 소속 같을때
                                #if len(src) == 0:
                                 #   flag = False
                                #else:
                                    #print(tempName, site[i], all_inst[-1])
                                    Answer_dict[tempName][site[i]] =  {'inst' : all_inst[-1], 'A_id': Aid}
                                    flag = False
                                    break
                            
                            elif all_name[-1]+str(count+1) not in Answer_dict :
                                Answer_dict[all_name[-1]+str(count+1)] = Answer
                                #if tempName != all_name[-1] :
                                if tempName == all_name[-1]:
                                    Answer_dict[all_name[-1]+'0'] = temp
                                    del Answer_dict[all_name[-1]]   

                count += 1

        # Answer_list.append(Answer)

print(len(Aid), len(all_name), len(all_inst) )
#Answer_dict.sort()
#print(len(Answer_dict))
#print(Answer_dict)
print(sorted(Answer_dict.items()))