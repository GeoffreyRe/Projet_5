import requests
class API(object):
	def __init__(self):
		self.products_list =[]
		self.variables_list = ["_id", "nutrition_grades", "product_name", "url", "stores"]

	def get_request_product(self,http_link):
		try:
			request = requests.get(http_link)
		except:
			self.products = {}
			return self.products
		request = request.json()
		self.products = request["products"]
		return self.products

	def find_value(self,dictionary,key):
		try:
			dictionary_value = dictionary[key]
		except KeyError:
			dictionary_value = ""

		return dictionary_value

	def separate_stores(self,stores):
		stores_list_formatted = []
		stores_list = stores.split(",")
		for store in stores_list:
			stores_list_formatted.append(store.strip())
		return stores_list_formatted




	def find_informations(self):
		for product in self.products:
			variables_of_a_product = []
			for variable_name in self.variables_list:
				value = self.find_value(product, variable_name).strip()
				if variable_name == "stores":
					value = self.separate_stores(value)
				variables_of_a_product.append(value)

			print(variables_of_a_product)
			if "" in variables_of_a_product:
				pass
			else:
				self.products_list.append(variables_of_a_product)

openfoodfact = API()
openfoodfact.get_request_product("https://be-fr.openfoodfacts.org/cgi/search.pl?search_simple=1&action=process&tagtype_0=categories&tag_contains_0=contains&tag_0=Cremes&sort_by=unique_scans_n&page_size=100&json=1")
openfoodfact.find_informations()









