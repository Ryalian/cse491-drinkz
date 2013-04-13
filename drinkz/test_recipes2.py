import sys
sys.path.insert(0, 'bin/') # allow _mypath to be loaded;
import os

from . import db, load_bulk_data, recipes
from cStringIO import StringIO
import imp
import test_load_recipe
import unittest




class TestRecipeStuff(unittest.TestCase):
    def setUp(self):                    # This is run once per test, before.
        db._reset_db()

    def tearDown(self):                 # This is run once per test, after.
        pass
      
    def test_add_recipe_1(self):
      #This is test for adding recipe by commend line
      #specifically, the commend line is in the format of:
      #<recipe_name (liquor,amount) (liquor2,amount2) ...etc>
      commend = '<scotch on the rocks, (blended scotch,4 oz)>'
      test_load_recipe.load_recipe(commend)
      
    def test_add_recipe_2(self):
      #This is test for adding recipe by commend line
      #specifically, the commend line is in the format of:
      #<recipe_name (liquor,amount) (liquor2,amount2) ...etc>
      #This one is to test the recipe with multi liquor
      commend = '<scotch on the rocks  (blended scotch,4 oz) (vodka,4 oz)>'
      test_load_recipe.load_recipe(commend)
      
      
    def test_add_recipe_3(self):
      #This is test for adding recipe by commend line
      #specifically, the commend line is in the format of:
      #<recipe_name (liquor,amount) (liquor2,amount2) ...etc>
      #This one is to test multi recipes input in one command line
      commend = '<scotch on the rocks  (blended scotch,4 oz) (vodka,4 oz)> <vodka martini  (unflavored vodka,6  oz) (vermouth, 1.5 oz)>'
      test_load_recipe.load_recipe(commend)    
      
      #test for getting all the available recipe we can use
class TestAvailable(object):
    def setUp(self):
        db._reset_db()


        db.add_bottle_type('Johnnie Walker', 'black label', 'blended scotch')
        db.add_to_inventory('Johnnie Walker', 'black label', '5000 ml')
        db.add_bottle_type('Uncle Herman\'s', 'moonshine', 'blended scotch')
        db.add_to_inventory('Uncle Herman\'s', 'moonshine', '5 liter')
        db.add_bottle_type('Gray Goose', 'vodka', 'unflavored vodka')
        db.add_to_inventory('Gray Goose', 'vodka', '1 liter')
        db.add_bottle_type('Rossi', 'extra dry vermouth', 'vermouth')
        db.add_to_inventory('Rossi', 'extra dry vermouth', '24 oz')
        r1 = recipes.Recipe('vomit inducing martini', [('black label','500 ml')])
        r2 = recipes.Recipe('scotch on the rocks', [('blended scotch', '4 oz')])
        r3 = recipes.Recipe('vodka martini', [('unflavored vodka', '6 oz'),('vermouth', '1.5 oz')])
        db.add_recipe(r1)
        db.add_recipe(r2)
        db.add_recipe(r3)

    def test_available_recipes(self):
	available_list = []
        available_list = db.get_available_recipe()

        assert not available_list == []

