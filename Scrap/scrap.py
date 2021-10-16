# import required modules
from bs4 import BeautifulSoup
import requests
import csv
import json
import unicodedata
import re
from googletrans import Translator


def isEnglish(s):
    return re.search('[a-zA-Z]', s)

def hasNumbers(inputString):
    return any(char.isdigit() for char in inputString)

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

    politician = []
    politician_sinhala = []
    tables = soup.find_all('table',class_="wikitable")
    

    for table in tables:
        rows = table.find_all('tr')
        
        for row in rows:
            cells = row.find_all('td')
            if (len(cells) > max and len(cells[name_cell].find_all('a'))>0):
                if(len(cells[name_cell].find_all('b'))>0):
                    name = cells[name_cell].find_all('b')[0].find('a')
                else:
                    name = cells[name_cell].find_all('a')[0]
                link = name.get('href')
                if(start_cell!=end_cell):
                    start = get_date(cells[start_cell].text.strip())
                    end = get_date(cells[end_cell].text.strip())
                    period = start + " - " + end
                else:
                    period = cells[start_cell].text.strip()            
                party = cells[party_cell].text.strip()
                early_life,education,political_career,family = get_polotician_obj(link)

                politician_obj = {
                    "Name" : (unicodedata.normalize('NFKD', name.text).encode('ascii', 'ignore')).strip(),
                    "Gender" : "Male",
                    "Period": period,
                    "Political Party" : party,
                    "Position" : position,
                    "Early Life" : unicodedata.normalize('NFKD', early_life).encode('ascii', 'ignore'),
                    "Education" : unicodedata.normalize('NFKD', education).encode('ascii', 'ignore'),
                    "Political Career" : unicodedata.normalize('NFKD', political_career).encode('ascii', 'ignore'),
                    "Family" : unicodedata.normalize('NFKD', family).encode('ascii', 'ignore')
                }

                politician.append(politician_obj)

                politician_sinhala_obj = {
                    "Name" : translate_to_sinhala(name.text.strip()),
                    "Gender" : translate_to_sinhala("Male"),
                    "Period" : translate_to_sinhala(period),
                    "Political Party" :translate_to_sinhala(party),
                    "Position" : translate_to_sinhala(position),
                    "Early Life" : translate_to_sinhala(early_life),
                    "Education" : translate_to_sinhala(education),
                    "Political Career" : translate_to_sinhala(political_career),
                    "Family" : translate_to_sinhala(family)
                }

                politician_sinhala.append(politician_sinhala_obj)
                
    return politician,politician_sinhala


