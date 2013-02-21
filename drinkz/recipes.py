import db

class Recipe:
	def __init__(self, name, r):
	   self.name = name
	   self.recipe = r

	def need_ingredients(self):
	   short = []
	 
	   for type, amount in self.recipe:
		need = db.convert_to_ml(amount)
		leck = db.check_inventory_for_type(type,need)

		if leck>0:
		   short.append((type,leck))
	
	   return short
