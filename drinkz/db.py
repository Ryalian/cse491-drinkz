# -*- coding: iso-8859-1 -*-
"""
Database functionality for drinkz information.
"""
import recipes

from cPickle import dump, load

# private singleton variables at module level
_bottle_types_db = set()
_inventory_db = {}
_recipe_db = {}
_converse = ''
class LiquorMissing(Exception):
    pass

class DuplicateRecipeName(Exception):
    pass

def _reset_db():
    "A method only to be used during testing -- toss the existing db info."
    global _bottle_types_db, _inventory_db, _recipe_db
    _bottle_types_db = set()
    _inventory_db = {}
    _recipe_db = {}

def add_recipe(r):
    if r.name in _recipe_db:
         raise DuplicateRecipeName()
	 print "oops"
    else:
        _recipe_db[r.name]=r

def get_recipe(name):
	for r in _recipe_db:
	   if r == name:
		return _recipe_db[r]
	return False

def get_all_recipes():
	all = []
	for recipe in _recipe_db:
		all.append(_recipe_db[recipe])
	return all

def save_db(filename):
    fp = open(filename, 'wb')

    tosave = (_bottle_types_db, _inventory_db, _recipe_db)
    dump(tosave, fp)

    fp.close()

def load_db(filename):
    global _bottle_types_db, _inventory_db, _recipe_db
    fp = open(filename, 'rb')

    loaded = load(fp)
    (_bottle_types_db, _inventory_db,_recipe_db) = loaded

    fp.close()

# exceptions in Python inherit from Exception and generally don't need to
# override any methods.


def add_bottle_type(mfg, liquor, typ):
    "Add the given bottle type into the drinkz database."
    _bottle_types_db.add((mfg, liquor, typ))

def _check_bottle_type_exists(mfg, liquor):
    for value in _bottle_types_db:
	m,l,_ = value
        if mfg == m and liquor == l:
            return True
    return False

def add_to_inventory(mfg, liquor, amount):
    "Add the given liquor/amount to inventory."
    if not _check_bottle_type_exists(mfg, liquor):
        err = "Missing liquor: manufacturer '%s', name '%s'" % (mfg, liquor)
        raise LiquorMissing(err)
	
    am = 0
    # just add it to the inventory database as a tuple, for now.
    size = amount.split(" ")
    if size[1] =="oz":
             am = float(size[0])*29.57
    if size[1] == "ml":
             am = float(size[0])
    if size[1] =="gallon":
	     am = float(size[0]) * 3785.41
    if size[1] =="liter":
	     am = float(size[0]) * 1000.0
    _inventory_db[(mfg,liquor)] = str(am + get_liquor_amount(mfg, liquor)) +" ml"

def check_inventory(mfg, liquor):
    for key in sorted(_inventory_db):
	m,l = key
        if mfg == m and liquor == l:
            return True
        
    return False

def get_liquor_amount(mfg, liquor):
    "Retrieve the total amount of any given liquor currently in inventory."
    amounts = 0
    am = 0
    for key in _inventory_db:
	m,l = key
	amount = _inventory_db[key]
        if mfg == m and liquor == l:
		size = amount.split(" ")
		if size[1] =="oz":
			am = float(size[0])*29.57
		if size[1] == "ml":
			am = float(size[0])
		if size[1] == "gallon":
			am == float(size[0]) * 3785.41
     		if size[1] =="liter":
             		am = float(size[0]) * 1000.0
		amounts = am +amounts

    return amounts

def get_liquor_inventory():
    "Retrieve all liquor types in inventory, in tuple form: (mfg, liquor)."
    for key in _inventory_db:
	m,l = key
        yield m, l

def check_inventory_for_type(liquor, amount):
	need = amount
	for key in _bottle_types_db:
	    m,l,t = key
	    if t == liquor:
		need = amount - get_liquor_amount(m,l)
	return need

def need_ingredients(recipe):
	   short = []
	 
	   for type, amount in recipe.recipe:
		leck = check_inventory_for_type(type,convert_to_ml(amount))

		if not leck<0.0:
		   short.append((type,leck))
	   return short
	   
	   
##for homework 5-2 #############################################
def check_inventory_for_type_multi(liquor, amount, number):
	need = amount
	for key in _bottle_types_db:
	    m,l,t = key
	    if t == liquor:
		need = amount * float(number) - get_liquor_amount(m,l) 
	return need


def need_ingredients_multi(recipe_name, number):
	   short = []
	   recipe = _recipe_db[recipe_name]
	   for type, amount in recipe.recipe:
		leck = check_inventory_for_type_multi(type,convert_to_ml(amount), number)

		if not leck<0:
		   short.append((type,leck))
	   return short  
  
  
  
  

def convert_to_ml(a):
	l = a.split(" ")
	am = 0
	if l[1] =="oz":
             am = float(l[0])*29.57
	elif l[1] == "ml":
             am = float(l[0]) 
        elif l[1] =="gallon":           
             am = float(l[0]) * 3785.41
	elif l[1] =="liter":
             am = float(l[0]) * 1000.0
	else:
	     am = False
	return am 


def get_available_recipe():
	available_recipe = []
	for recipe in _recipe_db:
	  if need_ingredients(_recipe_db[recipe]) == []:
	    available_recipe.append(recipe)
	return available_recipe