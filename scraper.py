from bs4 import BeautifulSoup
from urllib import request
import re
import get_ids as gi
import json


def scrape_db(drug_id):
    urls = "http://www.drugbank.ca/drugs/"
    x = request.urlopen(url=urls + drug_id)

    with x as response:
        page = response.read()

    soup = BeautifulSoup(page, "html.parser")

    soup2 = soup.find_all("dt")
    fields = []
    for i in soup2:
        fields.append(i.string)

    soup2 = soup.find_all("dd")
    inside = []
    for i in soup2:
        inside.append(i.text)

    this = {}
    for i in range(len(fields)):
        this[fields[i]] = inside[i]

    imp_fields = ["Name", "Synonyms", "Description", "Indication", "Half life",
                "Clearance", "Toxicity", "Food interactions"]

    clean_dict = {}
    for i in imp_fields:
        if i in this.keys():
            text = this[i]
            text = re.sub('\[\d\]', '', text)
            text = re.sub('\[Label\]', '', text)
            text = re.sub(' \.', '.', text)
            text = re.sub(r'[^\x00-\x7F]+', '', text)
            clean_dict[i] = text

    return clean_dict

def get_full_list(list_names):
    list_id = gi.ID_from_Name(list_names)
    list_scrapes = []
    for x in range(len(list_id)):
        list_scrapes.append(scrape_db(list_id[x]))
    return list_scrapes
