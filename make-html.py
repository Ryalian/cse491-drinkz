import os
from drinkz import db, recipes

#Input different data
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

try:
    os.mkdir('html/')
except OSError:
    # already exists
    pass



addr = """ <p><a href="index.html">Index</a>
<p><a href='inventory.html'>Inventory</a></p>
<p><a href='recipes.html'>Recipes</a></p>
<p><a href='liquor_types.html'>Liquor Types</a></p>
"""



#for index page
fp = open('html/index.html', 'w')

print >>fp, addr

fp.close()







#for recipe page
fp = open('html/recipes.html', 'w')

lack = db.get_all_recipes()
recipes = "<ol>"
for r in lack:
	if(r.need_ingredients() == []):
		lack = "Yes"
	else:
		lack = "No"
	recipes += "<li>" + r.name + ": " + lack + "</li>\n"

recipes = recipes + "</ol>"+ addr
print >> fp, recipes

fp.close()

# for inventory page
fp = open('html/inventory.html', 'w')

inventory = " <ol>"
for liquor in db.get_liquor_inventory():
	mfg = liquor[0]
	l = liquor[1]
	amount = db.get_liquor_amount(mfg, l)
	inventory += "<li>" + mfg + ", " + l + ": " + str(amount) + " ml</li>\n"
 

inventory = addr + inventory +"</ol>" 
print >> fp, inventory

fp.close()


#for liquor_types page
fp = open('html/liquor_types.html', 'w')

liquors = "<ol>"
for mfg,liquor,type in db._bottle_types_db:
      liquors += "<li>" +mfg+"  "+liquor+ "</li>"


liquors = liquors+"</ol>" + addr
print >> fp, liquors

fp.close()

