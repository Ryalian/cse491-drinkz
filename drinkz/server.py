#!/usr/bin/env python
import random
import socket
import time
import db,app
import os, sys



s = socket.socket()         # Create a socket object
host = socket.gethostname() # Get local machine name
port = random.randint(8000, 9999)
s.bind((host, port))        # Bind to the port


print 'Starting server on', host, port


s.listen(5)                 # Now wait for client connection.
while True:
   c, addr = s.accept()     # Establish connection with client.
   print 'Got connection from', addr
   
   input_data = c.recv(1024)
   path = "".join(input_data.split())
   path = path[3:-8]
   #print path+ 'aaaaaaaaaaaaaaa'
   
   environ = {}
   environ['PATH_INFO'] = path
   
   d = {}
   def my_start_response(s, h, return_in=d):
        d['status'] = s
        d['headers'] = h

   app_obj = app.SimpleApp()
   results = app_obj(environ, my_start_response)
   
   status, headers = d['status'], d['headers']
   
   text = "".join(results)  #
   
   print " Hello~~"

   time.sleep(2)
   c.send(status)
   #c.send(list(headers))
   c.send('\n')
   c.send(text)
   #c.send("good bye.")
   c.close()
