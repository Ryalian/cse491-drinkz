import app
import urllib

def test_index():
	environ = {}
	environ["PATH_INFO"] = '/'

	d = {}
	def my_start_response(s, h, return_in = d):
		d['status'] = s
		d['headers'] = h
	app_obj = app.SimpleApp()
	results = app_obj(environ, my_start_response)
	
	text = "".join(results)
	status, headers = d['status'], d['headers']
	
    	assert text.find('Visit:') != -1, text
    	assert ('Content-type', 'text/html') in headers
	assert status == '200 OK'


def test_recipe():

    environ = {}
    environ['PATH_INFO'] = '/recipe'

    d = {}
    def my_start_response(s, h, return_in=d):
        d['status'] = s
        d['headers'] = h

    app_obj = app.SimpleApp()
    results = app_obj(environ, my_start_response)

    text = "".join(results)
    status = d['status']
    headers = d['headers']

    assert text.find("vodka martini") != -1, text
    assert ('Content-type', 'text/html') in headers
    assert status == '200 OK'

