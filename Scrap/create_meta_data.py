import json


def create_meta_all():
    dict_all_meta = {}
    list_keys = ['Name_en', 'Name_si', 'Gender_en', 'Gender_si', 'Political_Party_en', 'Political_Party_si', 'Position_en', 'Position_si']
    for i in list_keys :
        dict_all_meta[i] = []
    
    with open('Corpus/politician_corpus.json') as f:
        data = json.loads(f.read())
    
    for items in data:
        for key in items:
            if key in list_keys:
                if type(items[key]) == list:
                    for val in items[key]:
                        if val not in dict_all_meta[key]:
                            dict_all_meta[key].append(val)
                else :
                    if items[key] not in dict_all_meta[key]:
                        dict_all_meta[key].append(items[key])
	
    with open ('Corpus/politician_meta_data_corpus.json','w+') as f:
        f.write(json.dumps(dict_all_meta))


create_meta_all()