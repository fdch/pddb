#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# **************************************************************************** #
# This file is part of the pdpy project
# Copyright (C) 2021 Fede Camara Halac
# **************************************************************************** #
import json
# from types import SimpleNamespace

with open("internals.json","r") as f:
  internals = json.load(f)
  # internals = json.load(f, object_hook=lambda d:SimpleNamespace(**d))

def getkind(query):
  for obj_kind, obj_subkind in internals.items():
    matches = []
    if isinstance(obj_subkind, dict):
      for obj_subkinds, obj_names in obj_subkind.items():
        for obj_name in obj_names:
          if query in obj_name:
            matches.append((obj_name, obj_kind, obj_subkinds))
    else:
      for obj_name in obj_subkinds:
          if query in obj_name:
            matches.append((obj_name, obj_kind, obj_subkinds))
    if len(matches):
      return matches

# print(getkind(""))