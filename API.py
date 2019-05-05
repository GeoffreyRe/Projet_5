
import requests
import ProductClassifier as productC
class API(object):
	def __init__(self):
		self.products_list =[]
		self.variables_list = ["_id", "nutrition_grades", "product_name", "url", "stores", "brands", "nutriments"]
		self.variables_list_2 = [0,0,0,0,0,0,"nutrition-score-fr"]
		self.checker = productC.ProductClassifier()

	def get_request_product(self,categorie):
		"""
		méthode qui permet de récupérer les données 'brutes' d'une catégorie de l'API grâce au module requests.
		Ensuite, cette méthode retourne une liste de l'ensemble des produits  
		 """
		http_link = ("https://be-fr.openfoodfacts.org/cgi/search.pl?search_simple=1&action=process&"
		"tagtype_0=categories&tag_contains_0=contains&tag_0={}"
		"&sort_by=unique_scans_n&page_size=200&json=1")
		try:
			request = requests.get(http_link.format(categorie))
		except:
			self.products = {}
			return self.products
		request = request.json()
		self.products = request["products"]
		return self.products

	def find_value(self,dictionary,key, key_2):
		"""
		Cette méthode permet de trouver une valeur d'un produit via une clé. 
		Parfois, il se peut que l'on se retrouve avec un dictionnaire de dictionnaire
		"""
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

	def find_informations(self,categorie):
		"""
		Méthode qui permet de trouver les informations nécessaires(code barre,...) pour
		chaque produit trouvé d'une catégorie donnée et traite l'ensemble des produits via une boucle
		Ensuite, cette méthode ajoute à une liste 'products list', chaque produit 'traité' (qui est aussi
		une liste).
		"""
		self.get_request_product(categorie) 
		for product in self.products:
			variables_of_a_product = []
			for i, variable_name in enumerate(self.variables_list):
				value = self.find_value(product, variable_name, self.variables_list_2[i]).strip()
				variables_of_a_product.append(value)
			self.products_list.append(variables_of_a_product)
		self.use_the_checker()

	def use_the_checker(self):
		"""
		Méthode qui utilise l'objet checker qui permet d'analyser les données receuillies 
		"""
		self.products_list = self.checker.complete_check(self.products_list)

	def reset_products_list(self):
		"""
		Méthode qui réinitialise la liste de produits 'products list'
		"""
		self.products_list = []

if __name__ == "__main__": 
	openfoodfact = API()
	openfoodfact.find_informations("Laits", "a")
	print(openfoodfact.products_list)
	openfoodfact.reset_products_list()
	openfoodfact.find_informations("Beurres", "d")
	print(openfoodfact.products_list)
	a = 0
	for produit in openfoodfact.products_list:
		if "" in produit:
			a +=1

	print(a)
	




