#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# **************************************************************************** #
# This file is part of the pdpy project
# Copyright (C) 2022 Fede Camara Halac
# **************************************************************************** #
""" Pure Data Live Database Client """

import socket
import sys
import pickle

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 9226         # The port used by the server

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
  s.connect((HOST, PORT))
  while True:
    x = input()
    if x == 'quit()' or x == 'QUIT' or x == 'EXIT':
      s.close()
      sys.exit()
    s.sendall(x.encode('utf-8'))
    data = s.recv(1024)
    data = pickle.loads(data)
    print('Received:', repr(data))
  s.close()