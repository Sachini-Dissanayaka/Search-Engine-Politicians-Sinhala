import csv
from scrap import get_all_data 

#position:[link,name,start,end,party]
url_list = {"President":["https://en.wikipedia.org/wiki/List_of_presidents_of_Sri_Lanka",3,4,5,7,7],
"Prime Minister":["https://en.wikipedia.org/wiki/List_of_prime_ministers_of_Sri_Lanka",3,4,5,7,7],
"Minister of Health":["https://en.wikipedia.org/wiki/Ministry_of_Health,_Nutrition_and_Indigenous_Medicine#Ministers",1,4,5,3,5],
"Opposition Leader":["https://en.wikipedia.org/wiki/Leader_of_the_Opposition_(Sri_Lanka)",1,2,3,5,5],
"Minister of Defence":["https://en.wikipedia.org/wiki/Minister_of_Defence_(Sri_Lanka)",2,3,4,5,6],
"Minister of Education" :["https://en.wikipedia.org/wiki/Minister_of_Education_(Sri_Lanka)",1,4,4,3,4],
"Minister of Finance" : ["https://en.wikipedia.org/wiki/Minister_of_Finance_(Sri_Lanka)",1,4,4,3,4],
"Minister of Sports" : ["https://en.wikipedia.org/wiki/Ministry_of_Sports_(Sri_Lanka)#List_of_Sports_Ministers",1,4,4,3,4],
"Minister of Transport" :["https://en.wikipedia.org/wiki/Ministry_of_Transport_and_Civil_Aviation_(Sri_Lanka)#Ministers",1,4,5,3,5],
"Minister of Labour" : ["https://en.wikipedia.org/wiki/Ministry_of_Labour,_Trade_Union_Relations_and_Sabaragamuwa_Development#Ministers",1,4,5,3,5],
"Minister of Foreign Affairs" : ["https://en.wikipedia.org/wiki/Minister_of_Foreign_Affairs_(Sri_Lanka)",1,4,4,3,4],
"Speaker of the Parliament" : ["https://en.wikipedia.org/wiki/Speaker_of_the_Parliament_of_Sri_Lanka",0,3,3,2,3]
}

politicians = []
politicians_sinhala = []
count = 0

for key in url_list:
    each = url_list[key]
    print("Log : Feching "+key+" List")
    out_eng, out_si = get_all_data(key,each[0],each[1],each[2],each[3],each[4],each[5])
    politicians += out_eng
    politicians_sinhala += out_si
    count += len(out_eng)

# csv_columns = ['Name','Gender','Start Date', 'End Date', 'Political Party', 'Position', 'Early Life', 'Education', 'Political Career','Family']
csv_columns = ['Name','Gender','Period', 'Political Party', 'Position', 'Early Life', 'Education', 'Political Career','Family']
csv_file = "Corpus/politician_corpus_with_english_final.csv"
try:
    with open(csv_file, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
        writer.writeheader()
        for politician in politicians:
            writer.writerow(politician)
except IOError:
    print("I/O error")


csv_file_sinhala = "Corpus/politician_corpus_with_sinhala_final.csv"
try:
    with open(csv_file_sinhala, 'w', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
        writer.writeheader()
        for politician_sin in politicians_sinhala:
            writer.writerow(politician_sin)
except IOError:
    print("I/O error")

print("Info : Total Number of Records " + str(count))