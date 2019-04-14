import re
import pandas as pd

def get_Vitamins(fruit_name):
    data_fruits = pd.read_csv('data_fruits.csv')
    #fruit_name = fruit_name.lower()
    print("I'm here1")
    vitamins = data_fruits['Fruit']
    index = 0
    for i in range(len(vitamins)):
        if vitamins[i] == fruit_name:
            index = i
    
    y = data_fruits['Fruit'][index]
    print(y)
    print(vits)
    vit = vitamins.loc[1]
    print("ELO")
    vitamins = vit.split()
    print("I'm here3")
    vit = iter(vitamins)
    next(vit)
    vitamins_v2 = [' '.join((first, second))
              for first, second in zip(vitamins, vit)]

    vitamins = []
    for x in range(len(vitamins_v2)):
        if x%2==0:
            vitamins.append(vitamins_v2[x])

    content = data_fruits[data_fruits['Fruit'] == fruit_name]['Content']
    content = content[1].split()
    content

    zipped_data = dict(zip(vitamins, content))
    zipped_data

    data = {}
    data['fruit_name'] = vitamins
    data['content'] = zipped_data

    return data

"""
OUTPUT : 
{'content': {'folate folic': '0,003',
  'vitamin a': '0,005',
  'vitamin b1': '0,02',
  'vitamin b2': '0,01',
  'vitamin b6': '0,05',
  'vitamin c': '5000'},
 'fruit_name': ['vitamin a',
  'vitamin b1',
  'vitamin b2',
  'vitamin b6',
  'vitamin c',
  'folate folic']}
"""