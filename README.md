# Search-Engine-Politicians-Sinhala

This repository contain source code for Sinhala politicians search engine created using Python and Elasticsearch

## Directory Structure

The important files and directories of the repository is shown below

    ├── Corpus : data scraped from the [website](https://en.wikipedia.org/wiki/List_of_Sri_Lankan_politicians)                    
        ├── politician_corpus_english.csv : original data scrapped from the website in English
        ├── politician_corpus_sinhala.csv : translated data scraped form the website in Sinhala
        ├── politician_meta_data_corpus.json : contain all meta date related to the politicians
        └── politician_corpus.json : contain the final politician set
    ├── Frontend : UI related files 
    ├── Scrap : Source codes for the data scraper
        ├── scrap.py : Source code for web scrapper and translator
        └── scrap_all.py : Source code to create corpus, Contain all the urls
    ├── Search : Source codes for the data scraper
        ├── app.py : Backend of the web app created using Flask
        ├── search.py : Search functions used to classify user search phrases and elasticsearch queries
        ├── facetedSearch.py : Search function used for faceted search using filters
        └── upload_data.py : File to upload data to elasticsearch cluster
    ├── queries.txt :  Example queries          


## Starting the web app

### Quick Start

#### Pre requesists : 
- Python, Flask, requests library and Elasticsearch needed in your PC.

#### Steps : 
1. Clone the repository.
2. Run an Elasticsearch instance on port 9200.
3. Go to the folder Search. Run the python script upload_data.py to put the corpus to the Elasticsearch.
4. And then run the python script app.py 

```commandline
git clone https://github.com/Sachini-Dissanayaka/Search-Engine-Politicians-Sinhala.git
cd Search-Engine-Politicians-Sinhala
cd Search
python upload_data.py
python app.py
```

### To run the web scraper

```commandline
cd Search-Engine-Politicians-Sinhala
cd Scrap
python scrap_all.py
```

## Data fields 

Each politician record contain subset of following data fields

1. Name - English
2. Name - Sinhala
3. Gender - English
4. Gender - Sinhala
5. Period - English
6. Period - Sinhala
7. Political Party - English
8. Political Party - Sinhala
9. Position - English
10. Position - Sinhala
11. Rate
12. Early Life
13. Education
14. Political Career
15. Family

## Data Scraping process

The dataset for the project was scraped from the website List of Sri Lankan politicians using the HTML/XML parsing library BeautifulSoup. The search engine contains a collection of 259 politicians having 6 metadata fields except for Early Life, Education, Political Career, and Family. All the data were present only in the English language on the website. While scraping, first I generated clean data using simple regex techniques and then all the data were translated into Sinhala language using the googletrans library to provide full support for Sinhala language queries. 


## Search Process

### Indexing and quering

For indexing the dataset I used the standard analyzer. Since there is no issue with lowercase and uppercase letters in Sinhala I have disabled the lowercase token filter which is enabled by default in the standard tokenizer. A primary index named “index-politicians” was created and the data was indexed under that. Elastic search queries are dynamically generated depending on the intention of the data extracted from the query string entered by the user. If no data can be extracted from the query string a basic multi_match query is sent. If the query string contains any keywords related to a specific data field such as Name, Gender, Period, Political Party, or Position that field is boosted in the request and the filter is added on top of the query.  Either the score given by elastic search or the rate of the politician is used to sort the results depending on the input query. In Order to serve misspelled queries, fuzzy queries are allowed by setting fuzziness to auto in all the queries. 

## Advance Features                  
* Text mining and text preprocessing
    * Search queries are processed before intent classification, here generate the cleaned data using simple regex techniques and then translated into Sinhala language using a translator.
* Intent Classification
    * Once the query is added, intent behind the query is found by intent classification. As an example, a query like “හොඳම ගැහැණු අගමැතිවරු 6” will return the 6 Female Prime Ministers having the highest rate.
* Faceted Search
    * The search engine supported faceted search related to Political Party, Gender,and Position. 
* Synonyms support
    * The search engine also support synonyms in Sinhala. As an example “කාන්තා අගමැතිවරු” will return all the female prime ministers even though the politician data does not have the word “කාන්තා” in the gender field or any of its fields
* Resistant to simple spelling errors
    * The search engine servers misspelled queries using Fuzziness. 

