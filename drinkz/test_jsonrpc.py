# -*- coding: iso-8859-1 -*-
import app
import urllib
from StringIO import StringIO
import db, recipes
import simplejson


def test_jsonrpc(method, param):
    environ = {}
    environ['PATH_INFO'] = '/rpc'
    environ['REQUEST_METHOD'] = 'POST'
    
    environ['wsgi.input'] = StringIO(simplejson.dumps({
        'method': method,
        'params': param,
	'id': 1
    }))
    environ['CONTENT_LENGTH'] = len(environ['wsgi.input'].getvalue())

    d = {}
    def my_start_response(s, h, return_in=d):
        d['status'] = s
        d['headers'] = h

    app_obj = app.SimpleApp()
    results = app_obj(environ, my_start_response)

    text = "".join(results)
    res = simplejson.loads(text)
    status, headers = d['status'], d['headers']


    assert ('Content-Type', 'application/json') in headers
    assert status == '200 OK'
    return res


def test_converts_unit_to_ml():
	result = test_jsonrpc('convert_units_to_ml', ['10 oz'])
	
	
	assert result['result'] == 295.7

def test_get_recipe_names():
	result = test_jsonrpc('get_recipe_names',[])
	recipe = result['result']

	assert 'vodka martini' in recipe
	  
def test_liquor_inventory():
	result = test_jsonrpc('liquor_inventory',[])['result']
	
	assert  'Johnnie Walker' in result
	
