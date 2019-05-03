import json
import records
class BDD(object):
	def __init__(self):
		self.import_json_data()
		self.connection()
		self.go_to_database()

	def import_json_data(self):
		with open("config.json", "r") as file:
			self.config = json.load(file)

	def connection(self):
		self.database = records.Database("mysql+mysqlconnector://{}:{}@localhost".format(self.config["User"],self.config["Pw"]))

	def go_to_database(self):
		self.database.query("SET NAMES 'utf8mb4'")
		self.database.query("USE {}".format(self.config["Database"]))

	def find_substitute(self):
		query = "SELECT User.id_product, Prod.product_name AS product, Prod.nutrition_score AS nut_score_product, User.id_substitute,\
			 Sub.product_name AS substitute, Sub.nutrition_score AS nut_score_sub FROM User INNER JOIN Product AS Prod ON\
			 Prod.barcode = User.id_product INNER JOIN Product AS Sub ON Sub.barcode = User.id_substitute"
		substitute_list = self.database.query(query).dataset
		return substitute_list

	def find_products(self, sub_category, nutrition_score = False):
		query_id_sub_cat = "SELECT id FROM Sub_category WHERE name = {}".format("'" + sub_category + "'")
		id_sub_cat = self.database.query(query_id_sub_cat).all(as_dict = True)[0]["id"]
		sub_query = "SELECT GROUP_CONCAT(name SEPARATOR ', ') FROM Assoc_product_store INNER JOIN Store ON Store.id = Assoc_product_store.id_store where barcode_product = barcode"
		if nutrition_score == False:
			query = "SELECT barcode, product_name, brand, nutrition_score, url, nutrition_grade, ({}) as stores FROM Product WHERE id_sub_category = {} ORDER BY RAND() LIMIT 10".format(sub_query, id_sub_cat)
		else:
			query = "SELECT barcode, product_name, brand, url, nutrition_score, nutrition_grade, ({}) as stores FROM Product WHERE id_sub_category = {}\
					 AND nutrition_score < {} ORDER BY RAND() LIMIT 10".format(sub_query, id_sub_cat, nutrition_score)
		products_list = self.database.query(query)
		products_list = products_list.all(as_dict = True)
		# pour retrouver les magasins : SELECT barcode_product, id_store, name, GROUP_CONCAT(name SEPARATOR ', ')
		# FROM Assoc_product_store INNER JOIN Store ON Store.id = Assoc_product_store.id_store where barcode_product = '7613035449596';
		return products_list



if __name__ == "__main__":
	bdd = BDD()
	print(bdd.find_products("snacks sucrés", 12))
		