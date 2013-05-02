#!/usr/bin/env python
import random
import socket
import time
import db,app
import os, sys
import simplejson
from StringIO import StringIO

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
   
   while "\r\n\r\n" not in input_data:
      data = c.recv(1024)
      if not data:
         break
      input_data += data
      time.sleep(1)
   print 'got entire request:', (input_data,)
   
   
   # now, parse the HTTP request.
   lines = input_data.splitlines()
   request_line = lines[0]
   request_type, path, protocol = request_line.split()
   print 'GOT', request_type, path, protocol
   
   key = ''
   name1 = ''
   key = lines[-2].split()[-1][6:]

   request_headers = lines[1:] # irrelevant, discard for GET.
#   print "request_headers:      ", request_headers   ,"################"
   query_string = ""
   if '?' in path:
      path, query_string = path.split('?', 1)   
   


   #print path+ 'aaaaaaaaaaaaaaa'
   
   environ = {}
   if request_type == "POST": 
   
        l_List = [cont for cont in request_headers if "Content-Length" in cont]
        length = l_List[0]
        
        n_List = [int(i) for i in length.split() if i.isdigit()]
        number = n_List[0]
        environ['CONTENT_LENGTH'] = number

        wsgi_input = request_headers[-1]

        environ['wsgi.input'] = StringIO(wsgi_input)   
   
   environ['PATH_INFO'] = path
   environ['QUERY_STRING'] = query_string 
   environ['REQUEST_METHOD'] = request_type
   environ['HTTP_COOKIE']= key
   d = {}
   def my_start_response(s, h, return_in=d):
        d['status'] = s
        d['headers'] = h

   app_obj = app.SimpleApp()
   
   try:
      results = app_obj(environ, my_start_response)
      response_headers = []
      for k, v in d['headers']:
	  h = "%s: %s" % (k, v)
	  response_headers.append(h)
      if request_type == 'POST': 
	  res = simplejson.loads("".join(results))
	  res["success"] = True
	  text = "\r\n".join(response_headers) + "\r\n\r\n" + "".join(simplejson.dumps(res))
      else:  
	  text = "\r\n".join(response_headers) + "\r\n\r\n" + "".join(results)   
      
      c.send("HTTP/1.0 %s\r\n" % d['status'])
      
    
      c.send(text)
      c.close()
   except:
      pass