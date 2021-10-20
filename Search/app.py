from flask import Flask
from flask import request
from flask_cors import CORS

from search import search

app = Flask(__name__)
CORS(app)
host = "127.0.0.1"

@app.route('/hello/', methods=['GET', 'POST'])
def welcome():
    return "Hello World!"

@app.route('/searchBy', methods=['GET', 'POST'])
def searchby_term():
    term = request.args.get('term')
    return search(term,host)

if __name__ == '__main__':
    app.run()