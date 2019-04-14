from bs4 import BeautifulSoup
from urllib import request
from urllib.request import Request, urlopen
import re
import get_ids as gi
import json

def scrape_dr(names):
    url = "https://www.drugs.com/drug-interactions/"
    urlnames = [url + name + ".html" for name in names]
    urls = [urlopen(Request(url=urlname, headers={'User-Agent': 'Mozilla/5.0'})) for urlname in urlnames]

    urlsindex = [url + name + '-index.html?filter=3' for name in names]
    urls_index = [urlopen(Request(url=urlindex, headers={'User-Agent': 'Mozilla/5.0'})) for urlindex in urlsindex]

    pages = []
    pages_index = []

    interactions_counter = {}
    interaction = {}

    for url in urls:
        with url as response:
            pages.append(response.read())

    for url in urls_index:
        with url as response:
            pages_index.append(response.read())

    souper = BeautifulSoup(pages[0], "html.parser")

    soup = souper.find_all("li", {"class" : "int_3"})
    soup2 = souper.find_all("li", {"class" : "int_2"})
    soup3 = souper.find_all("li", {"class" : "int_1"})

    major = soup[0].text.split(" ")[0]
    interactions_counter["major"] = int(major)

    moderate = soup2[0].text.split(" ")[0]
    interactions_counter["moderate"] = int(moderate)

    minor = soup3[0].text.split(" ")[0]
    interactions_counter["minor"] = int(minor)

    diseases = []

    for i in soup[1:]:
        diseases.append(i.text)

    soup = BeautifulSoup(pages_index[0], "html.parser")

    soup = soup.find_all("li", {"class" : "int_3"})
    interaction["drugs"] = [s.text for s in soup[0:interactions_counter["major"]]]
    interaction["diseases"] = diseases

    sum = 0

    for key, value in interactions_counter.items():
        sum += value

    partly = [round((value/sum) * 100, 2) for key, value in interactions_counter.items()]

    return interaction, partly

def scrape_drugs(names):
    res = []
    for name in names:
        try:
            a = scrape_dr([name])[1]
            res.append(a)
        except:
            res.append("No interactions found")
            continue
    sum = 0

    for key,value in res[0].items():
        sum += value

    partly = []

    for key, value in res[0].items():
        partly.append((value/sum) * 100)

    partly = [round(i, 2) for i in partly]
    return partly

def scrape_sc(names):
    url = "https://www.the-scientist.com/search?for="
    urlnames = [url + name for name in names]
    urls = [request.urlopen(url=urlname) for urlname in urlnames]
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
    res = {}
    for name in names:
        try:
            a = scrape_sc([name])
            res[name] = a
        except:
            res[name] = ["No articles found."]
            continue
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
            #text = re.sub('\\\n', '</br>', text)
            clean_dict[i] = text

    scraped = scrape_dr([clean_dict["Name"].lower()])
    clean_dict["Drug interactions"] = ', '.join(scraped[0]['drugs'])
    clean_dict["Disease interactions"] = ', '.join(scraped[0]['diseases'])

    clean_dict["major_num"] = scraped[1][0]

    clean_dict["moderate_num"] = scraped[1][1]

    clean_dict["minor_num"] = scraped[1][2]

    #print(clean_dict["Name"])
    return clean_dict

def get_full_list(list_names):
    list_id = gi.ID_from_Name(list_names)
    list_scrapes = []
    articles = []
    for x in range(len(list_id)):
        list_scrapes.append(scrape_db(list_id[x]))

        names = [i['Name'] for i in list_scrapes]
        articles = scrape_scientist(names)

    return list_scrapes, articles


#print(scrape_dr(['acarbose']))
x = get_full_list(['acarbose'])
print(x)
