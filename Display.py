import BDD as database
import os
import tablib
class Display(object):
	def __init__(self):
		self.first_menu_list = ["Quels aliments souhaitez-vous remplacer ?",
							"Retrouvez mes aliments substitués."]

		self.category_list = ["Produits laitiers", "Boissons", "Petit-déjeuners",
								 "Viandes", "Desserts"]
		self.sub_category_list = [["Laits", "Beurres", "Boissons lactées", "Fromages"],
									["Sodas", "Boissons au thé", "Boissons énergisantes"],
									["Céréales pour petit-déjeuner", "Pâtes à tartiner",
									"Confitures et marmelades"],["Charcuteries",
									"Volailles"],["Desserts au chocolat", "Compotes",
									"Desserts lactés", "Snacks sucrés"]]
		self.substituate_list = []

		self.menu_list = [self.first_menu_list,self.category_list, self.sub_category_list, self.substituate_list]
		self.bdd = database.BDD()

	def menu(self):
		index, intern_index, name = 0, 0, 0
		index_list = [0,1,2]
		functions_list = [self.first_menu, self.category_menu,self.sub_cat_menu,self.products_menu,self.substituate_menu]
		launched = True
		while launched:
			parameters_list = [[index],[index],[index, intern_index], [index, name],[]]
			index, intern_index,name = functions_list[index](*parameters_list[index])
			os.system("cls")

	def make_choice(self, liste):
		for i, element in enumerate(liste):
			print(str(i + 1), "-", str(element))
		answer = input("Quel choix voulez-vous?: ")
		answer = int(answer) - 1
		element = liste[answer]
		return answer, element


	def first_menu(self, index):
		answer, name = self.make_choice(self.first_menu_list)
		if answer == 0:
			index += 1
		elif answer == 1:
			index += 4
		return index, answer, name
		
	def category_menu(self, index):
		answer, name = self.make_choice(self.category_list)
		if answer == -1:
			index -= 1
		else:
			index += 1
		return index, answer, name

	def sub_cat_menu(self, index, intern_index):
		answer, name = self.make_choice(self.sub_category_list[intern_index])
		if answer == -1:
			index -= 1
		else:
			index += 1

		return index, answer, name
	def create_tablib(self, products_list,headers_list):
		data, data.headers = tablib.Dataset(),headers_list	
		keys_list,index = list(products_list[0].keys()), 1
		for dictionnary in products_list:
			value_to_append = []
			for key in keys_list:
				value_to_append.append(dictionnary[key])
			value_to_append.insert(0, index)
			index += 1
			data.append(value_to_append)
		print(data)
		return data.dict

	def make_choice_product(self,products_list):
		while True:
			answer = int(input("Quel produit choisisez-vous?: "))
			if 0 <= answer <= len(products_list):
				break
			else:
				print("Ce n'est pas un chiffre valide, recommencez svp") 
		product = products_list[answer - 1]
		return (product["code barre"], product ["Score"])


	def products_menu(self, index, name):
		list_products = self.bdd.find_products(name)
		columns_list = ["touche", "code barre", "Nom du produit"
						, "Marque","url", "Score"]
		tablib_list_product = self.create_tablib(list_products,columns_list)
		product = self.make_choice_product(tablib_list_product)
		list_substitute = self.bdd.find_products(name, product[1])
		tablib_list_substitute = self.create_tablib(list_substitute,columns_list)
		substitute = self.make_choice_product(tablib_list_substitute)
		return 0,0,0
		
	def substituate_menu(self):
		print(self.bdd.find_substitute())
		print("#"*20)
		answer = input("Appuyez sur entrée pour quitter")
		return 0,0,0


if __name__ == "__main__":
	display = Display()
	display.menu()
