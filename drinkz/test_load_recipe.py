import sys
import db, recipes

def load_recipe(fp):
    listed_fp = fp.replace('>','<').split('<')
    recipe_list = []
    
    for recipe in listed_fp:
      if not recipe.startswith(' ') and not recipes=='':
	recipe_list.append(recipe)
    recipe_list = filter(None, recipe_list)
    for recipe_ in recipe_list:
      element_list = recipe_.replace('(',')').split(')')
      name = element_list.pop(0)
      list_of_liquor = []
      for element in element_list:
	 if not element.startswith(' ') and element!='':
	   liquor = element.split(',')
	   list_of_liquor.append((liquor[0],liquor[1]))
	   r = recipes.Recipe(name,list_of_liquor)

      db.add_recipe(r)



if __name__ == '__main__':
  fp = raw_input("Input recipes:  ")
  load_recipe(fp)