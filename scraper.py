from bs4 import BeautifulSoup
from urllib import request
from urllib.request import Request, urlopen
import re
import get_ids as gi
import json

def scrape_sc(names):
    url = "https://www.the-scientist.com/search?for="
    urls = [request.urlopen(url=url + name) for name in names]
    articles = []

    pages = []

    for url in urls:
        with url as response:
            pages.append(response.read())

    soup = BeautifulSoup(pages[0], "html.parser")

    soup2 = soup.find_all("section", {"class" : "text"})

    soups = [i.find_all("header") for i in soup2]

    soups_titles = [i[0].findAll("a") for i in soups]
    soups_titles = [i[0].string for i in soups_titles]

    soups_links = [i[0].findAll("a") for i in soups]
    soups_links = [i[0].get('href') for i in soups_links]

    soups_dscs = [i.find_all("div") for i in soup2]
    soups_dscs = [i[1].text for i in soups_dscs]

    for i in range(len(soups_titles)):
        article = {}
        article['title'] = soups_titles[i]
        article['link'] = "https://www.the-scientist.com" + soups_links[i]
        article['dscs'] = soups_dscs[i]
        articles.append(article)

    i = 0
    while i < len(articles):
        if articles[i]['title'] == None:
            del articles[i]
        i += 1

    return articles

def scrape_scientist(names):
    #articles = []
    res = {}
    for name in names:
        a = scrape_sc([name])
        res[name] = a
    return res

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
                "Clearance", "Toxicity", "Food Interactions"]

    clean_dict = {}
    for i in imp_fields:
        if i in this.keys():
            text = this[i]
            text = re.sub('\[\d\]', '', text)
            text = re.sub('\[\d\d\]', '', text)
            text = re.sub('\[Label\]', '', text)
            text = re.sub(' \.', '.', text)
            text = re.sub(r'[^\x00-\x7F]+', '', text)
            text = re.sub('\\\n', '</br>', text)
            clean_dict[i] = text

    return clean_dict

def get_full_list(list_names):
    list_id = gi.ID_from_Name(list_names)
    list_scrapes = []
    for x in range(len(list_id)):
        list_scrapes.append(scrape_db(list_id[x]))

    names = [i['Name'] for i in list_scrapes]
    articles = scrape_scientist(names)
    return list_scrapes, articles
