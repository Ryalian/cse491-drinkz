def cssgen(color, size, title):
	fp = """<html><head><title>"""
	fp += title
	fp += """.</title><style type='text/css'>h1 {color:"""
	fp += color
	fp += """;}body {font-size: """
	fp += size 
	fp += """px;}</style> """
	return fp


def htmlgen():
	fp = """<script>function myFunction(){alert("Hello! I am an alert box!");}</script>"""
	fp += """<p><input type="button" onclick="myFunction()" value="Show alert box" />""" 
	return fp
