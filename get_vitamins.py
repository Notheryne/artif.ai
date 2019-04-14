import re
import pandas as pd

def get_Vitamins(fruit_name):
    data_fruits = pd.read_csv('data_fruits.csv')
    vitamins = data_fruits[data_fruits['Fruit'] == fruit_name]['Vitamin']
    vitamins[1] = re.sub(r'\(',"",vitamins[1])
    vitamins[1] = re.sub(r'\)',"",vitamins[1])
    vitamins = vitamins[1].split()
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
