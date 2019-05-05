class ProductClassifier(object):
	""" Class that will verify values from Openfoodfacts API"""
	def __init__(self):
		#self.api= openfoodfact.API()
		self.variables_list = ["_id", "nutrition_grades", "product_name", "url", "stores", "brands", "nutriments"]
		self.stores_list = ["Carrefour", "Carrefour Market", "Carrefour Planet",
		 "Carrefour Express", "Carrefour GB", "Colruyt", "Spa",
		 "Delhaize", "Delhaize City","Proxy Delhaize", "AD Delhaize", "Shop\'n Go",
		 "Albert Heijn", "Intermarché", "Cora", "Match", "Smatch" , "Louis Delhaize",
		 "Aldi", "Lidl", "Magasins U", "Super U", "Hyper U", "Auchan", "Noz", "Casino",
		 "Leclerc", "Géant", "Dia", "Edeka", "magasins diététiques"]

	def capital_letter(self, str_list):
		"""
		method that put capital letter at 
		the beginning of each word of a list
		 """
		title_list = [] 
		for string in str_list:
			title_list.append(string.title())
		return title_list

	def separate_stores(self,stores):
		"""
		method that separate and isolate each store of a product
		"""
		stores_list_formatted = []
		stores_list = stores.split(",")
		for store in stores_list:
			stores_list_formatted.append(store.strip())
		return stores_list_formatted

	def verify_stores(self, stores):
		"""
		method that verify if a store is known or not
		"""
		verified_stores = []
		stores = self.separate_stores(stores)
		for store in stores:
			if store == "":
				return ""
			elif store in self.stores_list:
				verified_stores.append(store)
		if len(verified_stores) >= 1: 
			return verified_stores
		else:
			return ""

	def remove_bad_products(self,list_products):
		"""
		method that removes products that don't satisfy conditions
		"""
		good_products = []
		for i,product in enumerate(list_products):
			if "" in product:
				pass
			else:
				good_products.append(product)
		return good_products

	def separate_brands(self, brands):
		"""
		method that return the first brand of a product
		"""
		if "," in brands:
			brands_list = brands.split(",")
			return brands_list[0].strip()
		return brands
			
	def complete_check(self,list_products):
		"""
		methode qui effectue la vérification complète des produits d'une catégorie
		et qui retire à terme, les produits qui ont des informations manquantes
		"""
		verified_products = []
		for product in list_products:
			verified_product = []
			for i, variable in enumerate(product):
				if i == self.variables_list.index("stores"):
					variable = self.verify_stores(variable)
				elif i == self.variables_list.index("brands"):
					variable = self.separate_brands(variable)
				verified_product.append(variable)
			verified_products.append(verified_product)
		verified_products = self.remove_bad_products(verified_products)
		return verified_products






		