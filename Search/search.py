import json
import requests

name_key_words = ["ගෙ"]
female_key_words = ["ගැහැණු", "කාන්තා", "කාන්තාව", "ස්ත්‍රී", "ගැහැණිය", "කාන්තාවන්"]
male_key_words = ["පිරිමි", "පුරුෂ"]
gender_key_words = ["ගැහැණු", "කාන්තා", "කාන්තාව", "ස්ත්‍රී", "පිරිමි", "පුරුෂ", "ගැහැණිය", "කාන්තාවන්"]
period_key_words = ["දී", "සිට"]
party_key_words = ["පක්ෂය", "පක්ෂ", "යේ", "පෙරමුණේ", "සංධානයේ", "පක්ෂයේ", "පෙරමුණ", "සංධානය"]
position_key_words = ["ජනාධිපති", "ජනාධිපතිවරයා" , "ජනාධිපතිවරු", "සභාපති", "අගමැති", "අගමැතිවරයා" , "අගමැතිවරු","මන්ත්‍රී", "අමාත්ය", "ඇමති", "ඇමතිවරු", "විපක්ෂ" "නායක", "කථානායක"]

aggs =      {
                "Name filter": {
                "terms": {
                    "field": "Name_si.keyword",
                    "size": 10
                }
                },
                "Gender filter": {
                "terms": {
                    "field": "Gender_si.keyword",
                    "size": 10
                }
                },
                "Period filter": {
                "terms": {
                    "field": "Period_si.keyword",
                    "size": 10
                }
                },
                "Party filter": {
                "terms": {
                    "field": "Political_Party_si.keyword",
                    "size": 10
                }
                },
                "Position filter": {
                "terms": {
                    "field": "Position_si.keyword",
                    "size": 10
                }
                }
            }

def generate_query(term, size,sort):
    if (sort):
        query = {
            "size" : size,
            "sort": [{"Rate": {"order": "desc"}}],
            "query":{
                "query_string":{
                    "query": term
                    }
                    },
                    "aggs" : aggs
                    }
    else:
        query = {
            "size" : size,
            "query":{
                "query_string":{
                    "query": term
                    }
                    },
                    "aggs" : aggs
                    }
    return query


def generate_query_with_keywords(mustObj,shouldobj,shouldmin,term, size,sort): 
    if (sort):  
        query = {
            "size": size,
            "sort": [{"Rate": {"order": "desc"}}],
            "aggs": aggs,
            "query": {
                "bool": {
                    "must": [
                        {
                        "query_string": {
                            "query": term
                        }
                        }
                    ],
                    "filter":mustObj,
                    "should":shouldobj,
                    "minimum_should_match" :shouldmin
                    }
                }
            }
    else:
        query = {
        "size": size,
        "aggs": aggs,
        "query": {
            "bool": {
                "must": [
                    {
                    "query_string": {
                        "query": term
                    }
                    }
                ],
                "filter":mustObj,
                "should":shouldobj,
                "minimum_should_match" :shouldmin
                }
            }
        }

    return query


def detect_keywords(term):
    mustobj = []
    words = term.split()
    text ,name, gender, period, party, position,period1,period2 = "", "", "", "","","",0,0
    for i in range (len(words)):
        word = words[i]
        print(word)
        if word  in name_key_words:
            name = words[i-2] + " "+ words[i-1]
            matchObjName = {"match" : {"Name_si" : name}}
            mustobj.append(matchObjName)

        elif word in male_key_words:
            gender = "පිරිමි"
            matchObjGender = {"match" : {"Gender_si" : gender}}
            mustobj.append(matchObjGender)
        
        elif word in female_key_words:
            gender = "ගැහැණු"
            matchObjGender = {"match" : {"Gender_si" : gender}}
            mustobj.append(matchObjGender)
        
        elif word  in period_key_words:
            if (word == "සිට" and (words[i+2]=="දක්වා" or words[i+2]=="තෙක්") and words[i-1].isdigit() and words[i+1].isdigit()):
                period1 = int(words[i-1])
                period2 = int(words[i+1])
            
            if(period1!=0 or period2!=0):
                period_list = list(range(period1,period2+1))
                matchObjPeriod = {"match" : {"Period_si" : " ".join(map(str,period_list))}}
            else:
                period = words[i-1]
                matchObjPeriod = {"match" : {"Period_si" : period}}
            mustobj.append(matchObjPeriod)

        elif word  in party_key_words:
            if(word == "යේ"):
                party = words[i-2] + " " + words[i-1]
            else:
                party = words[i-2] + " " + words[i-1]
            matchObjParty = {"match" : {"Political_Party_si" : party}}
            mustobj.append(matchObjParty)
        
        elif word  in position_key_words:
            if word in ["ජනාධිපති", "ජනාධිපතිවරයා" , "ජනාධිපතිවරු", "සභාපති"]:
                position = "සභාපති"
            elif word in ["ඇමති", "ඇමතිවරු", "මන්ත්‍රී","අමාත්ය"]:
                position = words[i-1] 
            elif word in ["අගමැති", "අගමැතිවරයා","අගමැතිවරු"]:
                position = "අගමැති"
            else:
                position = word
            matchObjPosition = {"match" : {"Position_si" : position}}
            mustobj.append(matchObjPosition)

        else:
            text += word + " "

    text_cleaned = ""
    text_splited = text.split()
    for word in text_splited:
        if not(word in name or  word in gender or  word in party or word in position or word in period):
            text_cleaned += word + " "
    text_cleaned = text_cleaned.strip()
    text_cleaned = (''.join([i for i in text_cleaned if not i.isdigit()])).strip()
    
    shouldobj = []
    if(len(text_cleaned)>0 and len(mustobj) > 0):
        shouldobj = [
            {"match": {"Early_Life":{"query": text_cleaned,"fuzziness": "AUTO"}}},
            {"match": {"Education":{"query": text_cleaned,"fuzziness": "AUTO"}}},
            {"match": {"Political_Career":{"query": text_cleaned,"fuzziness": "AUTO"}}},
            {"match": {"Family":{"query": text_cleaned,"fuzziness": "AUTO"}}}
            ]
  
    return mustobj,shouldobj

# {"match" : {"Early_Life" : text_cleaned}},{"match" : {"Education" : text_cleaned}},{"match" : {"Political_Career" : text_cleaned}},{"match" : {"Family" : text_cleaned}}

def perfom_query(query, host):
    URL = "http://" + str(host) + ":9200/index-politicians/_search"
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    response = (requests.post(URL, data = json.dumps(query), headers = headers)).text
    res = json.loads(response)
    hits = res['hits']['hits']
    politicians = []

    for politician in hits:
        politicians.append(politician['_source'])

    
    facets = res['aggregations']
    
    response_body = {
            "results" : politicians,
            "facets" : {
                "Name filter" : facets['Name filter']['buckets'],
                "Gender filter" : facets['Gender filter']['buckets'],
                "Period filter" : facets['Period filter']['buckets'],
                "Party filter" : facets['Party filter']['buckets'],
                "Position filter" : facets['Position filter']['buckets'],
            }      
        }

    return response_body


def hasNumbers(inputString):
    return any(char.isdigit() for char in inputString)


def get_number(term):
    size = 0
    number = [int(i) for i in term if (i.isdigit() and len(i)<3)]
    if(len(number)>0):
        size = number[0]
    return size


def intent_classifier(search_term):
    top_keywords = ["හොඳම", "කැමතිම", "ජනප්‍රියම", "ප්‍රසිද්ධම"]
    select_type = False
    resultword = ''

    search_term_list = search_term.split()
    similarwords  = [word for word in search_term_list if word in top_keywords]
    if(len(similarwords)>0):
        select_type = True
        resultword = " ".join([word for word in search_term_list if word not in top_keywords])
    else:
        select_type = False
        resultword = search_term

    return select_type,  resultword


def search(term, host):

    words = term.split()

    if(len(words)>1):

        sort,  resultword = intent_classifier(term)
        print(resultword)
        size = get_number(words)
        if(size>0):
            search_term = " ".join([word for word in resultword.split() if word!=str(size)])
        else:
            size = 20
            search_term = resultword
        
        mustObj, shouldobj = detect_keywords(search_term)
                        
        if (len(mustObj) > 0):
            if(len(shouldobj)>0):
                query = generate_query_with_keywords(mustObj, shouldobj,1, term, size,sort)
            else:
                query = generate_query_with_keywords(mustObj, shouldobj,0, term, size,sort)
        else:
            query = generate_query(term, size,sort)

       
    else:
        query = generate_query(term, 50,0)



    try:
        print(query)
        return perfom_query(query, host)
    except:
        print("Error")