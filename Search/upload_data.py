from elasticsearch import Elasticsearch, helpers
import json

es = Elasticsearch([{'host': 'localhost', 'port':9200}])

def upload_data():
    with open('Corpus/politician_corpus.json') as f:
        data = json.loads(f.read())
    helpers.bulk(es, data, index='index-politicians', doc_type='sinhala-politicians')


if __name__ == "__main__":
    upload_data()