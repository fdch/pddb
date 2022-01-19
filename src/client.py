#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# **************************************************************************** #
# This file is part of the pdpy project
# Copyright (C) 2022 Fede Camara Halac
# **************************************************************************** #
""" Pure Data Live Database Client """

import socket
import pickle

__all__ = ['connect']

def connect(host='127.0.0.1', port=9226, callback=print):
  """ Connect to the socket server """
  with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    # The server's hostname or IP address and the port used by the server
    s.connect((host, port))
    while True:
      x = input()
      if x == 'quit()' or x == 'QUIT' or x == 'EXIT': break
      s.sendall(x.encode('utf-8'))
      data = s.recv(1024)
      data = pickle.loads(data)
      callback(data)
    s.close()
  return

if __name__ == '__main__':
  connect()
