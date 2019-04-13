import csv
import re
import pandas as pd

"""def get_ids():
    file = "data_drug_id_name.csv"
    with open(file, encoding="utf-8") as f:
        data = {}
        for line in csv.DictReader(f):
            name = re.sub('\"', "", line['Names'])
            name = name.strip('[')
            name = name.strip(']')
            name = re.sub("\'", "", name)
            name = name.split(", ")
            newname = []
            for i in name:
                if i != "":
                    newname.append(i)
            data[tuple(newname)] = line['DrugBank ID']

    return data
"""

def make_list(name):
    name = name.strip('[')
    name = name.strip(']')
    name = re.sub("'", "", name)
    name = name.split(", ")
    names = name
    return names

def ID_from_Name(names):
    names = [x.lower() for x in names]
    data_drug_id_name = pd.read_csv('data_drug_id_name.csv')
    data_drug_id_name = pd.DataFrame(data_drug_id_name)
    data_drug_id_name['Names'] = data_drug_id_name.Names.apply(make_list)
    IDs = []

    for name in names:
        for x in range(len(data_drug_id_name)):
            if name in data_drug_id_name['Names'][x]:
#                if(data_drug_id_name['Names'][x][data_drug_id_name['Names'][x].index(name)]):
                IDs.append(data_drug_id_name['DrugBank ID'][x])

    return IDs
"""
def findxd(*name):
    data = get_ids()
    for n in name:
        for key,value in data.items():
            if n in key:
                return value
"""
