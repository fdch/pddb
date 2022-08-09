#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# **************************************************************************** #
# This file is part of the pdpy project
# Copyright (C) 2022 Fede Camara Halac
# **************************************************************************** #
""" Output a list of all Pure Data internals """
import pddb
import pdpy

db = pddb.PDDB(dbname="../pddb.json", listen=False)

with pdpy.PdPy(name="all_internals", root=True) as f:

  for i in db.internals():
    if "obj" in i: continue
    if "acoustics" in i: continue
    if "arithmetic" in i: continue
    if "messresponder" in i: continue
    if "clone-outlet" in i: continue
    if "libpd" in i: continue
    if "gfx" in i: continue
    if "gtemplate" in i: continue
    if "guiconnect" in i: continue
    if "alist" in i: continue

    internal = str(i).replace("_tilde", "~")
    internal = internal.replace("_new", "")
    
    if "g_array" in internal:
      f.createArray(pdpy.GOPArray())
      continue
    
    internal = internal.replace("g_","").replace("x_","").replace("m_","")
    if "sig" in internal and "~" not in internal:
      internal = internal.replace("sig", "") + "~"
    internal = internal.replace("list_", "list ")
    internal = internal.replace("file_", "file ")
    if internal.startswith("v") and internal.endswith("let"):
      internal = internal.replace("v", "") + "~"
    internal = internal.replace("plus", "+~")
    internal = internal.replace("times", "*~")
    internal = internal.replace("minus", "-~")
    internal = internal.replace("over", "/~")
    if 'curve' in internal: internal = "draw" + internal
    if 'elem' in internal: internal += "ent"
    if internal.endswith("sf") or internal == 'tabreceive' or internal  == 'tabsend' or internal in ("adc", "dac", "osc", "phasor", "noise"):
      internal += "~"
    
    if "hradio" in internal or "hdl" in internal: 
      f.create(pdpy.Radio(className="hradio"))
      continue
    if "vradio" in internal or "vdl" in internal: 
      f.create(pdpy.Radio(className="vradio"))
      continue
    if "vslider" in internal or "vsl" in internal:
      f.create(pdpy.Slider(className="vslider"))
      continue
    if "hslider" in internal or "hsl" in internal:
      f.create(pdpy.Slider(className="hslider"))
      continue
    if "template" == internal: 
      f.create(pdpy.Struct())
      continue
    if "pdint" in internal: 
      f.create(pdpy.Int())
      continue
    if "pdfloat" in internal:  
      f.create(pdpy.Float())
      continue
    if "pdsymbol" in internal: 
      f.create(pdpy.Symbol())
      continue
    if "numbox" in internal:
      f.create(pdpy.Nbx())
      continue
    if "mycanvas" in internal: 
      f.create(pdpy.Cnv())
      continue
    if "vumeter" in internal:  
      f.create(pdpy.Vu())
      continue

    if "canvas" == internal: continue

    f.create(pdpy.Obj(internal))
