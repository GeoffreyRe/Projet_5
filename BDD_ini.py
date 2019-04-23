import records
import json
import API
import copy
class BDD_ini(object):
	def __init__(self):
		self.stores_list = ["Carrefour", "Carrefour Market", "Carrefour Planet",
		 "Carrefour Express", "Carrefour GB", "Colruyt", "Spa",
		 "Delhaize", "Delhaize City","Proxy Delhaize", "AD Delhaize", "Shop\\'n Go",
		 "Albert Heijn", "Intermarché", "Cora", "Match", "Smatch" , "Louis Delhaize",
		 "Aldi", "Lidl", "Magasins U", "Super U", "Hyper U", "Auchan", "Noz", "Casino",
		 "Leclerc", "Géant", "Dia", "Edeka", "magasins diététiques"]
		self.category_list = ["Produits laitiers", "Boissons", "Petit-déjeuners",
								 "Viandes", "Desserts"]
		self.sub_category_list = [["Laits", "Beurres", "Boissons lactées", "Fromages"],
									["Sodas", "Boissons au thé", "Boissons énergisantes"],
									["Céréales pour petit-déjeuner", "Pâtes à tartiner",
									"Confitures et marmelades"],["Charcuteries",
									"Volailles"],["Desserts au chocolat", "Compotes",
									"Desserts lactés", "Snacks sucrés"]]
		self.openfoodfact = API.API()
	def import_json_data(self):
		with open("config.json", "r") as file:
			self.config = json.load(file)
		
	def connection(self):
		self.database = records.Database("mysql+mysqlconnector://{}:{}@localhost".format(self.config["User"],self.config["Pw"]))

	def go_to_database(self):
		self.database.query("SET NAMES 'utf8mb4'")
		self.database.query("USE {}".format(self.config["Database"]))
	def check_initialisation(self):
		if self.config["Initialisation"] == 0:
			self.config["Initialisation"] = 1
			return True
		else:
			return False
	def add_single_string(self, str):
		try:
			str = "\"" + str + "\""
		except:
			str = str
		return str

	def fill_table_store(self):
		for store in self.stores_list:
			self.database.query("INSERT INTO Store VALUES (NULL, {})".format(self.add_single_string(store)))

	def retrieve_store_dict(self):
		self.dict_of_stores = {}
		stores = self.database.query("SELECT * FROM Store").all(as_dict = True)
		for store in stores:
			self.dict_of_stores[store["name"]] = store["id"]
		return self.dict_of_stores

	def fill_table_category(self):
		for category in self.category_list:
			category = self.add_single_string(category)
			self.database.query("INSERT INTO Category VALUES (NULL,{})".format(category))

	def fill_table_sub_category(self):
		for index, sub_category in enumerate(self.sub_category_list):
			category_name = self.add_single_string(self.category_list[index])
			query_1 = "SELECT id FROM Category WHERE name = {}".format(category_name)
			foreign_key_id = ((self.database.query(query_1)).all(as_dict = False))[0]["id"]
			for sub_cat in sub_category:
				sub_cat = self.add_single_string(sub_cat)
				query_2 = "INSERT INTO Sub_category VALUES (NULL, {0},{1})".format(sub_cat,foreign_key_id)
				self.database.query(query_2)

	def call_api(self,sub_category):
		self.openfoodfact.find_informations(sub_category)
		products_list = copy.deepcopy(self.openfoodfact.products_list)
		self.openfoodfact.reset_products_list()
		return products_list

	def find_correspondence_store(self,product):
		index = self.openfoodfact.variables_list.index("stores")
		stores = product[index]
		stores_id = []
		for store in stores:
			stores_id.append(self.dict_of_stores[store])
		product.remove(stores)
		product.insert(index,stores_id)
		return product

	def fill_table_assoc(self, product):
		index_stores = self.openfoodfact.variables_list.index("stores")
		index_barcode = self.openfoodfact.variables_list.index("_id")
		stores_product = self.add_single_string(product[index_stores])
		barcode_product = self.add_single_string(product[index_barcode])
		for store in stores_product:
			query = "INSERT INTO Assoc_product_store VALUES ({},{})".format(barcode_product, store)
			self.database.query(query)
	def fill_table_product(self):
		for sub_category in self.sub_category_list:
			for sub_cat in sub_category:
				for product in self.call_api(sub_cat):
					product = self.find_correspondence_store(product)
					list_variables = ["a","b","c","d","e","f"]
					list_value = ["_id","product_name","brands","url",
					"nutrition_grades","nutriments"]
					for i, var in enumerate(list_variables):
						locals()[var] = self.add_single_string(product\
						[self.openfoodfact.variables_list.index(list_value[i])])
					g = self.database.query("SELECT id FROM Sub_category\
					WHERE name={}".format(self.add_single_string(sub_cat))).all(as_dict = True)[0]["id"]
					query = "INSERT INTO product VALUES({},{},{},\
					{},{},{},{})".format(locals()["a"],locals()["b"],locals()["c"],\
					locals()["d"],locals()["e"],locals()["f"],g).replace("\n","")
					try:
						self.database.query(query)
						self.fill_table_assoc(product)
					except:
						pass
	def connection_and_init(self):
		self.import_json_data()
		self.connection()
		self.go_to_database()

	def complete_fill(self):
		self.connection_and_init()
		if self.check_initialisation():
			self.fill_table_store()
			self.fill_table_category()
			self.fill_table_sub_category()
			self.retrieve_store_dict()
			self.fill_table_product()
			with open("values.json", "w") as file:
				file.write(json.dumps(self.config ,ensure_ascii = False, indent = 4))
		else:
			print("The database is already filled")

if __name__ == "__main__":
	bdd = BDD_ini()
	bdd.complete_fill()



		

