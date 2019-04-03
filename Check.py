class Check(object):
	""" Class that will verify values from Openfoodfacts API"""
	def __init__(self):
		self.stores_list = ["Carrefour", "Carrefour Market", "Carrefour Planet",
		 "Carrefour Express", "Carrefour GB", "Colruyt", "Spa",
		 "Delhaize", "Delhaize City","Proxy Delhaize", "AD Delhaize", "Shop'n Go",
		 "Albert Heijn", "Intermarché", "Cora", "Match", "Smatch" , "Louis Delhaize",
		 "Aldi", "Lidl", "Magasins U", "Super U", "Hyper U" "Auchan", "Noz", "Casino",
		 "Leclerc", "Géant", "Dia", "Edeka", "Magasins diététiques"]

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
			elif store in (self.stores_list or self.title(self.stores_list)):
				verified_stores.append(store)
		if len(verified_stores) >= 1: 
			return verified_stores
		else:
			return ""

	def remove_bad_products(self):
		"""method that remove products that don't satisfy conditions"""
		
