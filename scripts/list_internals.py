#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# **************************************************************************** #
# This file is part of the pdpy project
# Copyright (C) 2021 Fede Camara Halac
# **************************************************************************** # Open the file 'pddb.json' and load its contents to 'data'.
  
import json

with open('pddb.json') as f:
    data = json.load(f)

# extract every element inside the 'classes' field of the 'data' variable into a 'classes' variable.
names = []

for d in data:
  if d['classes']:
    c = d['classes']
    if isinstance(c, list):
      for a in c:
        if isinstance(a, list):
          for b in a:
            names.append(b['attributes']['methods']['name'])
        else:
          if 'methods' in a['attributes'] and isinstance(a['attributes']['methods'], list):
            for b in a['attributes']['methods']:
              if isinstance(b, str):
                names.append(b)
              else:
                names.append(b['name'])
          # else:
            # print("no method")
            # names.append(a['attributes'])
    else:
      names.append(c['attributes']['methods']['name'])



# print(len(names))
# classes = [d['classes'] for d in data if d['classes']]
# print(names)

# extract the 'name' field inside the 'method' field of the 'attributes' field of 

argtypes=[]
kinds=[]
subkinds=[]

def get_types(a):
  if 'description' in a:
      if a['description']['kind'] not in kinds:
        kinds.append(a['description']['kind'])
      if a['description']['subkind'] not in subkinds:
        subkinds.append(a['description']['subkind'])

  if 'arguments' in a and isinstance(a['arguments'], dict):
    for arg in a['arguments']['args']:
      if arg not in argtypes:
        argtypes.append(arg)
  
for d in data:
  if d['classes']:
    c = d['classes']
    for a in c:
      if isinstance(a['attributes'], list):
        for att in a['attributes']:
          get_types(att)
      else:
        get_types(a['attributes'])
print("-"*80)
print("Arg Types")
for i in argtypes:
  print(i)
print("-"*80)
print("Kinds")
for i in kinds:
  print(i)
print("-"*80)
print("Sub Kinds")
for i in subkinds:
  print(i)