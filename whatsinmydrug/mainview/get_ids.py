import csv
import re
import pandas as pd
#from py_translator import Translator

def make_list(name):
    name = name.strip('[')
    name = name.strip(']')
    name = re.sub("'", "", name)
    name = name.split(", ")
    names = name
    return names
"""
def ID_from_Name(names):
    names = [x.lower() for x in names]
    data_drug_id_name = pd.read_csv('data_drug_id_name.csv')
    data_drug_id_name = pd.DataFrame(data_drug_id_name)
    data_drug_id_name['Names'] = data_drug_id_name.Names.apply(make_list)
    IDs = []
    for name in names:
        regex = h + r"(\s\w+)?"
        for x in range(len(data_drug_id_name)):
            if name in data_drug_id_name['Names'][x]:
                #if(data_drug_id_name['Names'][x][data_drug_id_name['Names'][x].index(name)]):
                IDs.append(data_drug_id_name['DrugBank ID'][x])
    return IDs
"""

def ID_from_Name(names):
    names = [x.lower() for x in names]
    names = [name.strip(' ') for name in names]
    print("names new", names)
    data_drug_id_name = pd.read_csv('data_drug_id_name.csv')
    data_drug_id_name = pd.DataFrame(data_drug_id_name)
    data_drug_id_name['Names'] = data_drug_id_name.Names.apply(make_list)
    IDs = []
    lista = []
    for name in names:
        regex = name+r"(\s\w+)?"
        matches = []
        for x in range(len(data_drug_id_name)):
            for s in data_drug_id_name['Names'][x]:
                lok = re.findall(regex,s)
                if len(lok) > 0:
                    matches.append(lok)
        for p in range(len(matches)):
            lista.append(name + matches[p][0])
    for name_lista in lista:
        for x in range(len(data_drug_id_name)):
            if name_lista in data_drug_id_name['Names'][x]:
                IDs.append(data_drug_id_name['DrugBank ID'][x])

    output = []
    for x in IDs:
        if x not in output:
            output.append(x)

    return output