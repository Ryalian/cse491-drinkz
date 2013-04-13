#! /usr/bin/env python
# -*- coding: iso-8859-1 -*-
from wsgiref.simple_server import make_server
import urlparse
import simplejson
import db, recipes
import sys
import os
import css_html
import jinja2
import test_load_recipe


sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
try:
    _path_db = os.path.dirname(__file__) + '/../database'
    db.load_db(_path_db)
except:
    _path_db = os.path.dirname(__file__) + '../database'  
    db.load_db(_path_db)
#Input different data







dispatch = {
    '/' : 'index',
    '/recipe' : 'recipe',
    '/inventory' : 'inventory',
    '/liquor_type' : 'liquor_type',
    '/convert' : 'convert',
    '/convert_result' : 'convert_result',
    '/enter_liquor_type' : 'enter_liquor_type',
    '/enter_liquor_type_result' : 'enter_liquor_type_result',
    '/enter_liquor_inventory' : 'enter_liquor_inventory',
    '/enter_liquor_inventory_result' : 'enter_liquor_inventory_result',
    '/enter_recipes' : 'enter_recipes',
    '/enter_recipes_result' : 'enter_recipes_result',
    '/rpc'  : 'dispatch_rpc',
    '/bill' : 'bill',
    '/bill_result' : 'bill_result'
}

html_headers = [('Content-type', 'text/html')]


direction = """\n
Visit:
<p><a href='index'>Index</a>
<p><a href='recipe'>Recipe</a>
<p><a href='inventory'>Inventory</a>
<p><a href='liquor_type'>Liquor Types</a>
<p><a href='convert'>Unit Conversion</a>
<p><a href='enter_liquor_type'>Enter Liquor type</a>
<p><a href='enter_liquor_inventory'>Enter Liquor Inventory</a>
<p><a href='enter_recipes'>Enter Recipes</a>
<p><a href='bill'>BILL</a>\n
"""

class SimpleApp(object):
    def __init__(self):
	self.convertvalue = 0;

    def __call__(self, environ, start_response):

        path = environ['PATH_INFO']
        fn_name = dispatch.get(path, 'index')
        


        # retrieve 'self.fn_name' where 'fn_name' is the
        # value in the 'dispatch' dictionary corresponding to
        # the 'path'.
        fn = getattr(self, fn_name, None)

        if fn is None:
            start_response("404 Not Found", html_headers)
            return ["No path %s found" % path]

        return fn(environ, start_response)
            
    def index(self, environ, start_response):
        data = direction
        start_response('200 OK', list(html_headers))
	data = css_html.cssgen('red','30','Index') + data + css_html.htmlgen()
        return [data]


    def error(self, environ, start_response):
        status = "404 Not Found"
        content_type = 'text/html'
        data = "Couldn't find your stuff."
       
        start_response('200 OK', list(html_headers))
        return [data]


#Recipe page
    def recipe(self,environ, start_response):
	data = direction
	lack = db.get_all_recipes()
	recipes = "<ol>"
	for r in lack:
		if(db.need_ingredients(r) ==[]):
			lacks = "Yes"
		else:
			lacks = "No"
		
		recipes += "<li>" + r.name +": " + lacks+"</li>\n"
	data = css_html.cssgen('green','30','Recipe')+data + recipes + css_html.htmlgen()
	start_response('200 OK', list(html_headers))
	return [data]	
#Inventory Page
    def inventory(self, environ, start_response):
	data = direction
	inventory = "<ol>"
	for liquor in db.get_liquor_inventory():
		mfg = liquor[0]
		l   = liquor[1]
		amount = db.get_liquor_amount(mfg,l)
		inventory += "<li>" + mfg + ", " + l + ": " + str(amount) + "ml </li>\n"
	data = data + inventory + "</ol>"
        data = css_html.cssgen('blue','30','Inventory') + data + css_html.htmlgen()
	start_response('200 OK', list(html_headers))
	return [data]

#Liquor Type
    def liquor_type(self, environ, start_response):
	data = direction
	liquors = "<ol>" 
	for mfg, liquor, typ in db._bottle_types_db:
		liquors += "<li>" + mfg + "  " + "</li>"
	data = data + liquors +"</o>"
        data = css_html.cssgen('yellow','30','Liquor Type') + data + css_html.htmlgen()
	start_response('200 OK', list(html_headers))
	return [data]

#Convertion Page
    def convert(self, environ, start_response):
	data = convert()
        data = css_html.cssgen('pink','30','Convertion') + data + css_html.htmlgen()
	start_response('200 k', list(html_headers))
	data +="<p><a href='index'>Index</a>"
	return [data]

    def convert_result(self, environ, start_response):
        formdata = environ['QUERY_STRING']
        results = urlparse.parse_qs(formdata)
	
        amount = results['amount'][0]
        unit = results['unit'][0]
        ml = db.convert_to_ml(amount + " " + unit)
        content_type = 'text/html'
        data = "<a>After unit conversion: %s ml</a>   <a href='./'><p> return to index</a>" % (ml)
        
 	if amount != 0 and ml ==0:
		data = "<a>Wrong format<a>     <a href='./'><p> return to index</a>"
        start_response('200 OK', list(html_headers))
        return [data]
        
        
#HW 5-1-C Using Jinja to build page
    def enter_liquor_type(self, environ, start_response):
	# this sets up jinja2 to load templates from the 'templates' directory
	loader = jinja2.FileSystemLoader('./templates')
	env = jinja2.Environment(loader=loader)
	
	filename = 'form.html'
	vars = dict(input_type = 'liquor type', result_action = 'enter_liquor_type_result')
	
	template = env.get_template(filename)
	start_response('200 k', list(html_headers))
	print template.render(vars)
        return str(template.render(vars))

    def enter_liquor_type_result(self, environ, start_response):
	# this sets up jinja2 to load templates from the 'templates' directory
	loader = jinja2.FileSystemLoader('./templates')
	env = jinja2.Environment(loader=loader)
	
        formdata = environ['QUERY_STRING']
        results = urlparse.parse_qs(formdata)
	
        liquor_type = results['Input'][0]
        list0 = liquor_type.split()
        db.add_bottle_type(list0[0], list0[1], list0[2])
        
        filename = 'form_result.html'
	vars = dict(input_type = 'liquor type', direction = direction, result_action = 'enter_liquor_type_result')
	
	template = env.get_template(filename)
        start_response('200 OK', list(html_headers))
        return str(template.render(vars))
#################################################################################
    def enter_liquor_inventory(self, environ, start_response):
	# this sets up jinja2 to load templates from the 'templates' directory
	loader = jinja2.FileSystemLoader('./templates')
	env = jinja2.Environment(loader=loader)
	
	filename = 'form.html'
	vars = dict(input_type = 'liquor inventory', result_action = 'enter_liquor_inventory_result')
	
	template = env.get_template(filename)
	start_response('200 k', list(html_headers))
	print template.render(vars)
        return str(template.render(vars))

    def enter_liquor_inventory_result(self, environ, start_response):
	# this sets up jinja2 to load templates from the 'templates' directory
	loader = jinja2.FileSystemLoader('./templates')
	env = jinja2.Environment(loader=loader)
	
        formdata = environ['QUERY_STRING']
        results = urlparse.parse_qs(formdata)
	
        liquor_inventory = results['Input'][0]
        list0 = liquor_inventory.split()
        db.add_to_inventory(list0[0], list0[1], list0[2]+' '+list0[3])
        
        filename = 'form_result.html'
	vars = dict(input_type = 'liquor inventory', direction = direction, result_action = 'enter_liquor_inventory_result')
	
	template = env.get_template(filename)
        start_response('200 OK', list(html_headers))
        return str(template.render(vars))
##########################################################################
    def enter_recipes(self, environ, start_response):
	# this sets up jinja2 to load templates from the 'templates' directory
	loader = jinja2.FileSystemLoader('./templates')
	env = jinja2.Environment(loader=loader)
	
	filename = 'form.html'
	vars = dict(input_type = 'recipes', result_action = 'enter_recipes_result')
	
	template = env.get_template(filename)
	start_response('200 k', list(html_headers))
	print template.render(vars)
        return str(template.render(vars))

    def enter_recipes_result(self, environ, start_response):
	# this sets up jinja2 to load templates from the 'templates' directory
	loader = jinja2.FileSystemLoader('./templates')
	env = jinja2.Environment(loader=loader)
	
        formdata = environ['QUERY_STRING']
        results = urlparse.parse_qs(formdata)
	
        recipe = results['Input'][0]
        test_load_recipe.load_recipe(recipe)
        
        filename = 'form_result.html'
	vars = dict(input_type = 'recipes', direction = direction, result_action = 'enter_recipes_result')
	
	template = env.get_template(filename)
        start_response('200 OK', list(html_headers))
        return str(template.render(vars))
######################################################################################
############Bill's function to check how much liquor he needs#########################
######################################################################################
    def bill(self, environ, start_response):
	# this sets up jinja2 to load templates from the 'templates' directory
	loader = jinja2.FileSystemLoader('./templates')
	env = jinja2.Environment(loader=loader)
	
	filename = 'bill_form.html'
	vars = dict(input_type = 'Input recipe and amount:', result_action = 'bill_result')
	
	template = env.get_template(filename)
	start_response('200 k', list(html_headers))
	print template.render(vars)
        return str(template.render(vars))
        
        
    def bill_result(self, environ, start_response):
	# this sets up jinja2 to load templates from the 'templates' directory
	loader = jinja2.FileSystemLoader('./templates')
	env = jinja2.Environment(loader=loader)
	
        formdata = environ['QUERY_STRING']
        results = urlparse.parse_qs(formdata)
	
        recipe = results['Input'][0]
        amount = results['Number'][0]
        #test_load_recipe.load_recipe(recipe)
        try:
	  short = db.need_ingredients_multi(recipe, amount)
	  if short == []:
	   short = 'Nothing you have enough stuff'
        except:
	  short = 'Wrong input'
	  pass
        filename = 'bill_form_result.html'
	vars = dict(input_type = 'Recipt and Number', direction = direction,cont ='c', amount = amount, recipe = recipe,short = str(short))
	
	template = env.get_template(filename)
        start_response('200 OK', list(html_headers))
        return str(template.render(vars))

################################################################################

    def dispatch_rpc(self, environ, start_response):
        # POST requests deliver input data via a file-like handle,
        # with the size of the data specified by CONTENT_LENGTH;
        # see the WSGI PEP.
        
        if environ['REQUEST_METHOD'].endswith('POST'):
            body = None
            if environ.get('CONTENT_LENGTH'):
                length = int(environ['CONTENT_LENGTH'])
                body = environ['wsgi.input'].read(length)
                response = self._dispatch(body) + '\n'
                start_response('200 OK', [('Content-Type', 'application/json')])

                return [response]

        # default to a non JSON-RPC error.
        status = "404 Not Found"
        content_type = 'text/html'
        data = "Couldn't find your stuff."
       
        start_response('200 OK', list(html_headers))
        return [data]


    def _decode(self, json):
        return simplejson.loads(json)

    def _dispatch(self, json):
        rpc_request = self._decode(json)

        method = rpc_request['method']
        params = rpc_request['params']
        
        rpc_fn_name = 'rpc_' + method
        fn = getattr(self, rpc_fn_name)
        result = fn(*params)

        response = { 'result' : result, 'error' : None, 'id' : 1 }
        response = simplejson.dumps(response)
        return str(response)

#Homework 4-5
    def rpc_convert_units_to_ml(self,amount):
	return db.convert_to_ml(amount)

    def rpc_get_recipe_names(self):
        lack = db.get_all_recipes()
        recipe = []
	for r in db.get_all_recipes():
		recipe.append(r.name)
	return recipe

    def rpc_liquor_inventory(self):
	inventory = []
	liquor =  db.get_liquor_inventory()
	for mfg ,l in liquor:
		inventory.append(mfg)
	return inventory
	
	
	
#HW 5-1-D Using Jinja to build page, Json-RPC
    def rpc_enter_liquor_type(self, environ, start_response):
	# this sets up jinja2 to load templates from the 'templates' directory
	loader = jinja2.FileSystemLoader('./templates')
	env = jinja2.Environment(loader=loader)
	
	filename = 'form.html'
	vars = dict(input_type = 'liquor type', result_action = 'enter_liquor_type_result')
	
	template = env.get_template(filename)
	start_response('200 k', list(html_headers))
	print template.render(vars)
        return str(template.render(vars))

    def rpc_enter_liquor_type_result(self, environ, start_response):
	# this sets up jinja2 to load templates from the 'templates' directory
	loader = jinja2.FileSystemLoader('./templates')
	env = jinja2.Environment(loader=loader)
	
        formdata = environ['QUERY_STRING']
        results = urlparse.parse_qs(formdata)
	
        liquor_type = results['Input'][0]
        list0 = liquor_type.split()
        db.add_bottle_type(list0[0], list0[1], list0[2])
        
        filename = 'form_result.html'
	vars = dict(input_type = 'liquor type', direction = direction)
	
	template = env.get_template(filename)
        start_response('200 OK', list(html_headers))
        return str(template.render(vars))
#################################################################################
    def rpc_enter_liquor_inventory(self, environ, start_response):
	# this sets up jinja2 to load templates from the 'templates' directory
	loader = jinja2.FileSystemLoader('./templates')
	env = jinja2.Environment(loader=loader)
	
	filename = 'form.html'
	vars = dict(input_type = 'liquor inventory', result_action = 'enter_liquor_inventory_result')
	
	template = env.get_template(filename)
	start_response('200 k', list(html_headers))
	print template.render(vars)
        return str(template.render(vars))

    def rpc_enter_liquor_inventory_result(self, environ, start_response):
	# this sets up jinja2 to load templates from the 'templates' directory
	loader = jinja2.FileSystemLoader('./templates')
	env = jinja2.Environment(loader=loader)
	
        formdata = environ['QUERY_STRING']
        results = urlparse.parse_qs(formdata)
	
        liquor_inventory = results['Input'][0]
        list0 = liquor_inventory.split()
        db.add_to_inventory(list0[0], list0[1], list0[2]+' '+list0[3])
        
        filename = 'form_result.html'
	vars = dict(input_type = 'liquor inventory', direction = direction)
	
	template = env.get_template(filename)
        start_response('200 OK', list(html_headers))
        return str(template.render(vars))
##########################################################################
    def rpc_enter_recipes(self, environ, start_response):
	# this sets up jinja2 to load templates from the 'templates' directory
	loader = jinja2.FileSystemLoader('./templates')
	env = jinja2.Environment(loader=loader)
	
	filename = 'form.html'
	vars = dict(input_type = 'recipes', result_action = 'enter_recipes_result')
	
	template = env.get_template(filename)
	start_response('200 k', list(html_headers))
	print template.render(vars)
        return str(template.render(vars))

    def rpc_enter_recipes_result(self, environ, start_response):
	# this sets up jinja2 to load templates from the 'templates' directory
	loader = jinja2.FileSystemLoader('./templates')
	env = jinja2.Environment(loader=loader)
	
        formdata = environ['QUERY_STRING']
        results = urlparse.parse_qs(formdata)
	
        recipe = results['Input'][0]
        test_load_recipe.load_recipe(recipe)
        
        filename = 'form_result.html'
	vars = dict(input_type = 'recipes', direction = direction)
	
	template = env.get_template(filename)
        start_response('200 OK', list(html_headers))
        return str(template.render(vars))



################################################################################


    def load_database(self):
	try:
        	db.load_db(_path_db)
	except:

        	db.add_bottle_type('Johnnie Walker', 'black label', 'blended scotch')
        	db.add_to_inventory('Johnnie Walker', 'black label', '500 ml')
        	db.add_bottle_type('Uncle Herman\'s', 'moonshine', 'blended scotch')
        	db.add_to_inventory('Uncle Herman\'s', 'moonshine', '5 liter')
        	db.add_bottle_type('Gray Goose', 'vodka', 'unflavored vodka')
        	db.add_to_inventory('Gray Goose', 'vodka', '1 liter')
        	db.add_bottle_type('Rossi', 'extra dry vermouth', 'vermouth')
        	db.add_to_inventory('Rossi', 'extra dry vermouth', '24 oz')
        	r1 = recipes.Recipe('vomit inducing martini', [('orange juice','6 oz'),('vermouth','1.5 oz')])
        	r2 = recipes.Recipe('scotch on the rocks', [('blended scotch', '4 oz')])
        	r3 = recipes.Recipe('vodka martini', [('unflavored vodka', '6 oz'),('vermouth', '1.5 oz')])
        	db.add_recipe(r1)
        	db.add_recipe(r2)
        	db.add_recipe(r3)
       
def form():
    return """
<form action='recv'>
Your first name? <input type='text' name='firstname' size'20'>
Your last name? <input type='text' name='lastname' size='20'>
<input type='submit'>
</form>
"""

def convert():
    return """
<form action='convert_result'>
amount <input type='text' name='amount' size'20'>
unit <input type='text' name='unit' size='20'>
<input type='submit'>
</form>
"""


if __name__ == '__main__':
    import random, socket
    port = random.randint(8000, 9999)
    
    app = SimpleApp()
    
    httpd = make_server('', port, app)
    print "Serving on port %d..." % port
    print "Try using a Web browser to go to http://%s:%d/" % \
          (socket.getfqdn(), port)
    httpd.serve_forever()
