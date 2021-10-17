# import required modules
from bs4 import BeautifulSoup
import requests
import csv
import json
import unicodedata
import re
from googletrans import Translator


def translate_to_sinhala(value):
    sinhala_val = value
    if(len(value)>0):
        translator = Translator()
        sinhala_val = translator.translate(value, dest='si').text
    
    return sinhala_val

def get_date(str):
    items = str
    if(len(str.split())>1):
        match = re.match(r"([a-z]+)([0-9]+)", str.split()[1], re.I)
        if match:
            items = str.split()[0] + " " + " ".join(match.groups())
    return items

#get long data
def get_polotician_obj(title):
    page = requests.get("https://en.wikipedia.org"+title)

    soup = BeautifulSoup(page.content, 'lxml')
  
    # display scrapped data
    early_life = ""
    education = ""
    political_career = ""
    family = ""
  
    allh2s = soup.find_all("h2")
    allh3s = soup.find_all("h3")
    allheads = allh2s + allh3s

    pattern = r'(\[[,\d\s ]*)[0-9]([,\d\s ]*\])'

    for head in allheads:
        allspan = head.find_all('span',class_="mw-headline")
        for each in allspan:
            if(each["id"].find("Early_life_and_education")==0):
                sib = head.find_next_siblings()
                for i in range(len(sib)-1):
                    try:
                        tag_name1 = sib[i].name
                        tag_name2 = sib[i+1].name
                    except AttributeError:
                        tag_name = ""
                    if(tag_name1 == "p"):
                        early_life = re.sub(pattern, '', sib[i].text.strip())
                        if(tag_name2 == "p"):
                            education = re.sub(pattern, '', sib[i+1].text.strip())
                        break
            elif(each["id"].find("Political_career")==0 or each["id"].find("Early_political_career")==0):
                for sib in head.find_next_siblings():
                    try:
                        tag_name = sib.name
                    except AttributeError:
                        tag_name = ""
                    if(tag_name == "p"):
                        political_career = re.sub(pattern, '', sib.text.strip())
                        break
            elif(each["id"].find("Family")==0 or each["id"].find("Personal_life")==0 or each["id"].find("Marriage")==0 or each["id"].find("Private_life")==0):
                for sib in head.find_next_siblings():
                    try:
                        tag_name = sib.name
                    except AttributeError:
                        tag_name = ""
                    if(tag_name == "p"):
                        family = re.sub(pattern, '', sib.text.strip())
                        break
            elif(each["id"].find("Early_life")==0):
                for sib in head.find_next_siblings():
                    try:
                        tag_name = sib.name
                    except AttributeError:
                        tag_name = ""
                    if(tag_name == "p"):
                        early_life = re.sub(pattern, '', sib.text.strip())
                        break
            elif(each["id"].find("Education_and_early_career")==0 or each["id"].find("Education")==0):
                for sib in head.find_next_siblings():
                    try:
                        tag_name = sib.name
                    except AttributeError:
                        tag_name = ""
                    if(tag_name == "p"):
                        education = re.sub(pattern, '', sib.text.strip())
                        break

    return early_life,education,political_career,family


#get all data
def get_all_data(position,url,name_cell,start_cell,end_cell,party_cell,max):

    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'lxml')

    female_list = ["Sirimavo","Chandrika","Siva","Vimala","Renuka"]

    politician_english = []
    politician_sinhala = []
    politician_meta_data = []

    tables = soup.find_all('table',class_="wikitable") 

    for table in tables:
        rows = table.find_all('tr')
        
        for row in rows:
            cells = row.find_all('td')
            if (len(cells) > max and len(cells[name_cell].find_all('a'))>0):
                if(len(cells[name_cell].find_all('b'))>0):
                    name_link = cells[name_cell].find_all('b')[0].find('a')
                else:
                    name_link = cells[name_cell].find_all('a')[0]

                link = name_link.get('href')
                name = name_link.text.strip()

                if(len(name.split())>0 and (name.split()[0] in female_list)):
                    gender = "Female"
                else:
                    gender = "Male"

                if(start_cell!=end_cell):
                    start = get_date(cells[start_cell].text.strip())
                    end = get_date(cells[end_cell].text.strip())
                    period = start + " - " + end
                else:
                    period = cells[start_cell].text.strip()    

                party = cells[party_cell].text.strip()

                early_life,education,political_career,family = get_polotician_obj(link)

                name_si = translate_to_sinhala(name)
                gender_si = translate_to_sinhala(gender)
                period_si = translate_to_sinhala(period) 
                political_party_si = translate_to_sinhala(party)
                position_si = translate_to_sinhala(position)
                early_life_en =  unicodedata.normalize('NFKD', early_life).encode('ascii', 'ignore')
                early_life_si = translate_to_sinhala(early_life)
                education_en = unicodedata.normalize('NFKD', education).encode('ascii', 'ignore')
                education_si = translate_to_sinhala(education)
                political_career_en = unicodedata.normalize('NFKD', political_career).encode('ascii', 'ignore')
                political_career_si = translate_to_sinhala(political_career)
                family_en = unicodedata.normalize('NFKD', family).encode('ascii', 'ignore')
                family_si = translate_to_sinhala(family)

                politician_en_obj = {
                    "Name" : name,
                    "Gender" : gender,
                    "Period": period,
                    "Political Party" : party,
                    "Position" : position,
                    "Early Life" : early_life_en,
                    "Education" : education_en,
                    "Political Career" : political_career_en,
                    "Family" : family_en
                }

                politician_english.append(politician_en_obj)

                politician_sinhala_obj = {
                    "Name" : name_si,
                    "Gender" : gender_si,
                    "Period" : period_si,
                    "Political Party" :political_party_si,
                    "Position" : position_si,
                    "Early Life" : early_life_si,
                    "Education" : education_si,
                    "Political Career" : political_career_si,
                    "Family" : family_si
                }

                politician_sinhala.append(politician_sinhala_obj)

                politician_obj = {
                    "Name_en" : name,
                    "Name_si" : name_si,
                    "Gender_en" : gender,
                    "Gender_si" : gender_si,
                    "Period_en" : period,
                    "Period_si" : period_si,
                    "Political_Party_en" : party,
                    "Political_Party_si" :political_party_si,
                    "Position_si" : position_si,
                    "Early_Life" : early_life_si,
                    "Education" : education_si,
                    "Political_Career" : political_career_si,
                    "Family" : family_si
                }

                politician_meta_data.append(politician_obj)

    return politician_english,politician_sinhala,politician_meta_data


