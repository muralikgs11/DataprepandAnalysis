#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May  9 11:12:28 2019

@author: murali
"""
from matplotlib import pyplot as plt 
import json
import numpy as np

with open('./data/annotations.json','r') as myfile:
    data = myfile.read()
    
annotDict = json.loads(data)

class_names = annotDict['types']
images = annotDict['imgs']

class_dict = dict()
for keys in class_names:
    class_dict[keys] = list()
    
for keys in images:
    objects = images[keys]['objects']
    if len(objects) > 0:
        for i in range(len(objects)):
            class_ind = objects[i]['category']
            class_dict[class_ind].append(keys)
            
num_elems = list()
for keys in class_dict:
    num_elems.append(len(class_dict[keys]))
    if len(class_dict[keys]) > 500:
        print(keys, len(class_dict[keys]))

index = np.argsort(num_elems)
    
plt.bar(range(len(num_elems)), np.array(num_elems)[index])
plt.show()

