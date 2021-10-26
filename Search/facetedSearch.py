import json
import requests

from search import intent_classifier, get_number

def facetedSearch(data, host):
    
    term = data['term']
    words = term.split()
    sort,  resultword = intent_classifier(term)
    print(resultword)
    size = get_number(words)
    if(size>0):
        search_term = " ".join([word for word in resultword.split() if word!=str(size)])
    else:
        size = 20
        search_term = resultword
    
    if(sort):
        sort_method = [{"Rate": {"order": "desc"}}]
    else:
        sort_method = [{"_score": {"order": "desc"}}]

    filter = []

    for filterobj in data['filter']:
        matchObj = {
            "match" : filterobj
        }

        filter.append(matchObj)
    query = {
        "size" : size,
        "sort" : sort_method,
        "query": {
            "bool": {
            "must": [
                {
                "query_string": {
                    "query": search_term,
                    "fuzziness": "AUTO"
                }
                }
            ],
            "filter": filter
            }
        },
        "aggs" :  {
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
    }


    try:
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
        print(query)
        return response_body

    except:
        print("Error")