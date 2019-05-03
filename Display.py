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
		index, intern_index, name, intern_index_2 = 0, 0, 0, 0
		index_list = [0,1,2]
		functions_list = [self.first_menu, self.category_menu,self.sub_cat_menu,self.products_menu,self.substituate_menu]
		launched = True
		while launched:
			parameters_list = [[index],[index],[index, intern_index], [index, name, intern_index],[]]
			index, intern_index,name = functions_list[index](*parameters_list[index])
			os.system("cls")

	def validate_answer_int(self, product_list):
		validate = False
		while not validate:
			answer = input("Quel choix voulez-vous ?")
			try:
				answer = int(answer)
			except:
				print("Ce n'est pas un chiffre")
				continue
			if 0 <= answer <= len(product_list):
				validate = True
			else:
				print("Ce chiffre ne correspond à aucun choix")


		return (answer - 1)  


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

		return index, intern_index, name

	def create_tablib(self, products_list,headers_list):
		data, data.headers = tablib.Dataset(),headers_list	
		keys_list,index = ["product_name", "brand", "nutrition_score"], 1
		for dictionnary in products_list:
			value_to_append = []
			for key in keys_list:
				value_to_append.append(dictionnary[key])
			value_to_append.insert(0, index)
			index += 1
			data.append(value_to_append)
		print(data)
		answer = int(input("Plus d'info sur un produit: "))
		return (answer - 1)

		

	def display_informations_product(self, product):
		tuple_keys_list = [("barcode","Code barre produit"),("product_name", "Nom du produit"),
							("brand","Marque"), ("nutrition_grade", "Grade nutritionnel"),
							("nutrition_score", "Score nutritionnel"), ("stores", "Magasins"),
							("url", "Url") ]
		for key, value in tuple_keys_list:
			print(value, "=", product[key])
		answer = input("Validez votre choix: ")
		return answer, (product["barcode"], product["nutrition_score"])

	def product(self, index, name, products_list):
		if products_list == 0:
			products_list = self.bdd.find_products(name)
		headers_list = ["Touche", "Nom produit", "Marque", "Score"]
		while True:
			os.system("cls")
			answer = self.create_tablib(products_list, headers_list)
			if answer == -1:
				return False, index, products_list, 0
			sub_answer, value_product = self.display_informations_product(products_list[answer])
			if sub_answer == "O":
				index += 1
				return True, index, products_list, value_product
			continue


	def recording_into_user(self, value_product, value_substitute):
		answer = input("Voulez-vous enregistrer votre choix ?: ")
		if answer == "O":
			self.bdd.record_table_user()
			print("votre enregistrement a bien été effectué")
		else:
			print("pas de soucis")
		input()


				
	def substitute(self, index, name, products_list, value):
		substitute_list = self.bdd.find_products(name, value[1])
		headers_list = ["Touche", "Nom produit", "Marque", "Score"]
		while True:
			os.system("cls")
			answer = self.create_tablib(substitute_list, headers_list)
			if answer == -1:
				index -= 1
				return True , index, products_list, 0
			sub_answer, value_substitute = self.display_informations_product(substitute_list[answer])
			if sub_answer == "O":
				self.recording_into_user(value, value_substitute)
				return False, index, products_list, value
			continue
		
		

	def products_menu(self, index, name, index_2):
		intern_index, products_list, value = 0, 0, 0
		functions_list = [self.product, self.substitute]
		launched = True
		while launched:
			parameters_list = [[intern_index, name, products_list],
								[intern_index, name, products_list, value]]
			launched, intern_index, products_list, value = functions_list[intern_index](*parameters_list[intern_index])
		index -= 1
		return index,index_2,0



		
		




















		
	def substituate_menu(self):
		print(self.bdd.find_substitute())
		print("#"*20)
		answer = input("Appuyez sur entrée pour quitter")
		return 0,0,0


if __name__ == "__main__":
	display = Display()
	display.menu()
