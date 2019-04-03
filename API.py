import requests
class API(object):
	def __init__(self):
		self.products_list =[]
		self.variables_list = ["_id", "nutrition_grades", "product_name", "url", "stores", "nutriments"]
		self.variables_list_2 = [0,0,0,0,0,"nutrition-score-fr"]
		self.stores_list = ["Carrefour", "Carrefour Market", "Carrefour Planet",
		 "Carrefour Express", "Carrefour GB", "Colruyt", "Spa",
		 "Delhaize", "Delhaize City","Proxy Delhaize", "AD Delhaize", "Shop'n Go",
		 "Albert Heijn", "Intermarché", "Cora", "Match", "Smatch" , "Louis Delhaize",
		 "Aldi", "Lidl", "Magasins U", "Super U", "Hyper U", "Auchan", "Noz", "Casino",
		 "Leclerc", "Géant", "Dia", "Edeka", "Magasins diététiques"]

	def get_request_product(self,categorie ,nutriscore):
		http_link = ("https://be-fr.openfoodfacts.org/cgi/search.pl?search_simple=1&action=process&"
		"tagtype_0=categories&tag_contains_0=contains&tag_0={}&tagtype_1=nutrition_grades&tag_contains_1=contains"
		"&tag_1={}&sort_by=unique_scans_n&page_size=150&json=1")
		try:
			request = requests.get(http_link.format(categorie,nutriscore))
		except:
			self.products = {}
			return self.products
		request = request.json()
		self.products = request["products"]
		return self.products

	def find_value(self,dictionary,key, key_2):
		if key_2 == 0:
			try:
				dictionary_value = dictionary[key]
			except KeyError:
				dictionary_value = ""
		elif key_2 != 0:
			try:
				dictionary_value = dictionary[key][key_2]
			except KeyError:
				dictionary_value = ""

		return str(dictionary_value)

	def separate_stores(self,stores):
		stores_list_formatted = []
		stores_list = stores.split(",")
		for store in stores_list:
			stores_list_formatted.append(store.strip())
		return stores_list_formatted

	def title(self, str_list):
		title_list = []
		for string in str_list:
			title_list.append(string.title())
		return title_list

	def verify_stores(self, stores):
		verified_stores = []
		stores = self.separate_stores(stores)
		for store in stores:
			if store == "":
				return ""
			elif store in (self.stores_list + self.title(self.stores_list)):
				verified_stores.append(store)
		if len(verified_stores) >= 1: 
			return verified_stores
		else:
			return ""



	def find_informations(self):
		for product in self.products:
			variables_of_a_product = []
			for i, variable_name in enumerate(self.variables_list):
				value = self.find_value(product, variable_name, self.variables_list_2[i]).strip()
				if variable_name == "stores":
					value = self.verify_stores(value)
				variables_of_a_product.append(value)

			if "" in variables_of_a_product:
				pass
			else:
				self.products_list.append(variables_of_a_product)

openfoodfact = API()
openfoodfact.get_request_product("crèmes", "d")
openfoodfact.find_informations()
for produit in openfoodfact.products_list:
	print(produit)










