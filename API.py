
import requests
import Check 
class API(object):
	def __init__(self):
		self.products_list =[]
		self.variables_list = ["_id", "nutrition_grades", "product_name", "url", "stores", "brands", "nutriments"]
		self.variables_list_2 = [0,0,0,0,0,0,"nutrition-score-fr"]
		self.checker = Check.Check()

	def get_request_product(self,categorie ,nutriscore):
		http_link = ("https://be-fr.openfoodfacts.org/cgi/search.pl?search_simple=1&action=process&"
		"tagtype_0=categories&tag_contains_0=contains&tag_0={}&tagtype_1=nutrition_grades&tag_contains_1=contains"
		"&tag_1={}&sort_by=unique_scans_n&page_size=200&json=1")
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

	def find_informations(self,categorie, nutriscore):
		self.get_request_product(categorie,nutriscore) 
		for product in self.products:
			variables_of_a_product = []
			for i, variable_name in enumerate(self.variables_list):
				value = self.find_value(product, variable_name, self.variables_list_2[i]).strip()
				variables_of_a_product.append(value)
			self.products_list.append(variables_of_a_product)
		self.use_the_checker()

	def use_the_checker(self):
		self.products_list = self.checker.complete_check(self.products_list)

if __name__ == "__main__": 
	openfoodfact = API()
	openfoodfact.find_informations("Aliments d'origine végétale", "a")
	a = 0
	for produit in openfoodfact.products_list:
		if "" in produit:
			a +=1

	print(a)
	print(len(openfoodfact.products_list))




