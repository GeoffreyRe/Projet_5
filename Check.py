class Check(object):
	""" Class that will verify values from Openfoodfacts API"""
	def __init__(self):
		#self.api= openfoodfact.API()
		self.variables_list = self.variables_list = ["_id", "nutrition_grades", "product_name", "url", "stores", "brands", "nutriments"]
		self.stores_list = ["carrefour", "carrefour market", "carrefour planet",
		 "carrefour express", "carrefour GB", "colruyt", "spa",
		 "delhaize", "delhaize city","proxy delhaize", "aD delhaize", "shop'n go",
		 "albert heijn", "intermarché", "cora", "match", "smatch" , "louis delhaize",
		 "aldi", "lidl", "magasins U", "super U", "hyper U", "auchan", "noz", "casino",
		 "leclerc", "géant", "dia", "edeka", "magasins diététiques"]

	def capital_letter(self, str_list):
		""" method that put capital letter at 
		the beginning of each word of a list """
		title_list = [] 
		for string in str_list:
			title_list.append(string.title())
		return title_list

	def separate_stores(self,stores):
		"""method that separate and isolate each store of a product"""
		stores_list_formatted = []
		stores_list = stores.split(",")
		for store in stores_list:
			stores_list_formatted.append(store.strip())
		return stores_list_formatted

	def verify_stores(self, stores):
		"""method that verify if a store is known or not"""
		verified_stores = []
		stores = self.separate_stores(stores)
		for store in stores:
			if store == "":
				return ""
			elif store in (self.stores_list + self.capital_letter(self.stores_list)):
				verified_stores.append(store)
		if len(verified_stores) >= 1: 
			return verified_stores
		else:
			return ""

	def remove_bad_products(self,list_products):
		good_products = []
		"""method that remove products that don't satisfy conditions"""
		for i,product in enumerate(list_products):
			if "" in product:
				pass
			else:
				good_products.append(product)
		return good_products

	def separate_brands(self, brands):
		if "," in brands:
			brands_list = brands.split(",")
			return brands_list[0].strip()
		return brands
			

	def complete_check(self,list_products):
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






		