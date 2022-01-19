#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# **************************************************************************** #
# This file is part of the pdpy project
# Copyright (C) 2022 Fede Camara Halac
# **************************************************************************** #
""" Pure Data Live Database Server """

import json
from types import SimpleNamespace
import socket
import pickle

class PDDB(object):
  """ Pure Data Live Database """
  def __init__(self, dbname=None, host='127.0.0.1', port=9226, listen=True):
    """ Initialize the PDDB object
    """
    # the name of the database
    self.dbname = dbname
    # host and port for the socket server
    self.host = host
    self.port = port
    self.addr = None # the address of the client
    # the json object hook
    self.hook = lambda d: SimpleNamespace(**d) 
    # the data
    self.db = None
    # the connection
    self.conn = None
    # load the database
    if self.dbname: self.load()
    # Start the socket server
    if listen: self.listen()
  
  def listen(self):
    """ Start the socket server """
    self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.sock.bind((self.host, self.port))
    self.sock.listen(1)
    print("Listening on {}:{}".format(self.host, self.port))
    self.conn, self.addr = self.sock.accept()
    with self.conn:
      print('Connected by', self.addr)
      while True:
        q = self.conn.recv(1024)
        if not q: break
        q = q.decode('utf-8')
        o = self.is_obj(q)
        msg = []
        if o:
          msg.append(o)
          i = self.has_iolets(q)
          c = self.arg_count(q)
          if i:
            msg.append(i)
          if c:
            msg.append(c)
        else:
          msg.append(0)
        
        if len(msg):
          self.conn.sendall(pickle.dumps(msg))
    
    self.conn = None
    self.sock.close()

  
  def load(self, dbname=None):
    """ Load the database from a json file """
    with open(dbname or self.dbname, 'r') as fp:
      self.db = json.load(fp, object_hook=self.hook)
  
  def dumps(self):
    """ Dump the database as an indented string """
    if self.db: print(json.dumps(self.db, indent=4))
  
  def arg_count(self, q):
    """ Query the database for object number of creation self.__arguments__
    """
    for x in self.db:
      if len(x.classes):
        for c in x.classes:
          if hasattr(c,'attributes') and hasattr(c.attributes,'arguments') and hasattr(c.attributes.arguments,'name') and q == c.attributes.arguments.name:
            return len(c.attributes.arguments.args)

  def is_obj(self, q):
    """ Query the database to check if it is a pd object or not
    """
    if '->' in q or '<-' in q: return True
    if not (">" in q or "<" in q or q.startswith("\\") or "'" in q):
      for x in self.db:
        if len(x.classes):
          for c in x.classes:
            if hasattr(c,'attributes') and hasattr(c.attributes,'arguments'):
              if (hasattr(c.attributes.arguments,'name') and q == c.attributes.arguments.name) or q == c.attributes.arguments: 
                return True
    return False

  def has_iolets(self, q):
    """ Query the database to check if the pd object has iolets, return obj
    """
    if '->' in q or '<-' in q: 
      return self.has_iolets('loadbang')
    if not (">" in q or "<" in q or q.startswith("\\") or "'" in q):
      for x in self.db:
        if len(x.classes):
          for c in x.classes:
            if hasattr(c,'attributes') and hasattr(c.attributes,'iolets'):
              if (hasattr(c.attributes.arguments,'name') and q == c.attributes.arguments.name): 
                return c.attributes.iolets
    return False

if __name__ == "__main__":
  import sys
  pddb = PDDB(dbname=sys.argv[1])
