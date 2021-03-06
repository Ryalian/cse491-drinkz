# -*- coding: iso-8859-1 -*-
import app
import urllib
from StringIO import StringIO
import db, recipes
import simplejson


def tjsonrpc(method, param):
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
    try:
	    app_obj.load_database()
    except db.DuplicateRecipeName:
	    pass	
    results = app_obj(environ, my_start_response)

    text = "".join(results)
    res = simplejson.loads(text)
    status, headers = d['status'], d['headers']


    assert ('Content-Type', 'application/json') in headers
    assert status == '200 OK'
    return res


def test_converts_unit_to_ml():
	result = tjsonrpc('convert_units_to_ml', ['10 oz'])
	
	
	assert result['result'] == 295.7

def test_get_recipe_names():
	result = tjsonrpc('get_recipe_names',[])
	recipe = result['result']
	for rec in recipe:
		print rec
	assert 'vodka martini' in recipe
	  
def test_liquor_inventory():
	result = tjsonrpc('liquor_inventory',[])
	inventory = result['result']
	assert  'Johnnie Walker' in inventory
