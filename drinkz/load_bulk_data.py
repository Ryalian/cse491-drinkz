"""
Module to load in bulk data from text files.
"""

# ^^ the above is a module-level docstring.  Try:
#
#   import drinkz.load_bulk_data
#   help(drinkz.load_bulk_data)
#

import csv                              # Python csv package

from . import db                        # import from local package

def load_bottle_types(fp):
    """
    Loads in data of the form manufacturer/liquor name/type from a CSV file.

    Takes a file pointer.

    Adds data to database.

    Returns number of bottle types loaded
    """
    reader = data_reader(fp)

    x = []
    n = 0
    for line in reader:
        try:
        	(mfg, name, typ) = line
        	n += 1
	except:
		print 'not a valid format'
	try:
	        db.add_bottle_type(mfg, name, typ)
	except:
		print 'Fail to add bottle type'
		pass
    return n

def load_inventory(fp):
    """
    Loads in data of the form manufacturer/liquor name/amount from a CSV file.

    Takes a file pointer.

    Adds data to database.

    Returns number of records loaded.

    Note that a LiquorMissing exception is raised if bottle_types_db does
    not contain the manufacturer and liquor name already.
    """
    reader = data_reader(fp)

    x = []
    n = 0
    for line in reader:
	try:
		(mfg,name,amount) = line
	        n += 1
        except:
		print 'not at valid format'

	try:
		db.add_to_inventory(mfg, name, amount)
	except db.LiquorMissing:
		print 'Can not find this liqour in inventory'
    return n



"""
generator wrapper 
PS: I fogot to save last time, redoing everything:(
"""

def data_reader(fp):
	reader = csv.reader(fp)
	for line in reader:
	    try:
		if line[0].startswith('#') or not line[0].strip():
		   continue
		yield line
	    except:
	  	pass

if __name__ == '__main__':
  recipe = raw_input('Input recipe(In format of "<name (name,amount) (name,amount)...>"\n')
  print recipe+'bbbb'
  load_recipe(recipe)

