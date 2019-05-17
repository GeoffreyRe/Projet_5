"""
This class has the responsibility to manage display of menu
and navigation inside menu.
"""
import os
import json
import tablib
import Bdd as database

class Display():
    """
    This class has the responsibility to manage display of menu
    and navigation inside menu.
    """
    def __init__(self):
        self.first_menu_list = ["Quels aliments souhaitez-vous remplacer ?",
                                "Retrouvez mes aliments substitués.",
                                "Quitter le programme."]

        self.category_list = ["Produits laitiers", "Boissons", "Petit-déjeuners",
                              "Viandes", "Desserts"]
        self.sub_category_list = [
            ["Laits", "Beurres", "Boissons lactées", "Fromages"],
            ["Sodas", "Boissons au thé", "Boissons énergisantes"],
            ["Céréales pour petit-déjeuner", "Pâtes à tartiner", "Confitures et marmelades"],
            ["Charcuteries", "Volailles"],
            ["Desserts au chocolat", "Compotes", "Desserts lactés", "Snacks sucrés"]
            ]
        self.bdd = database.Bdd()
        self.command = None # this attribute will be initialized in 'import_json_data' method

    def import_json_data(self):
        """
        Method that imports datas contained into json file
        """
        # we use method of module json
        with open("config.json", "r") as file:
            config = json.load(file)
            self.command = config["Command"]

    def welcome(self):
        """
        Method wich makes an "introduction" of program
        """
        self.import_json_data()
        sentences = ("Bonjour et bienvenue sur le programme de la startup 'PurBeurre'.",
                     "Ce programme vous permet de récupérer directement les données de ",
                     "la (gigantesque) base de données 'OpenFoodFacts'. Pour plus ",
                     "d'informations sur l'utilisation de ce logiciel, n'hésitez pas ",
                     "à lire le fichier 'README.md'. Bonne utilisation !",
                     "")
        for sentence in sentences:
            print(sentence)
        input("Appuyez sur 'enter' pour continuer")

    def menu(self):
        """
        Method wich manages travel inside menu and allows to called method wich corresponds
        of user's choice.
        """
        index, intern_index, name = 0, 0, 0
        functions_list = [self.first_menu, self.category_menu, self.sub_cat_menu,
                          self.products_menu, self.user_menu]
        launched = True
        while launched:
            os.system(self.command)
            # needed parameters for each function
            parameters_list = [[index], [index], [index, intern_index],
                               [index, name, intern_index], []]
            launched, index, intern_index, name = functions_list[index](*parameters_list[index])


    def validate_answer_int(self, product_list, sentence=0):
        """
        Method wich attends to validate an 'int' user's answer. This method verifies if
        response of user is an integer, if this response is possible...
        """
        self.create_space()
        validate = False
        sentences = ["Quel choix voulez-vous ?: ",
                     "Sur quel produit voulez-vous plus d'information ?: ",
                     "Plus d'information ?: "]
        while not validate:
            answer = input(sentences[sentence]) # we display the good question
            try:
                answer = int(answer) #checking if it is a int
            except:
                print("Ce n'est pas un chiffre")
                continue # we raise the question again.
            if 0 <= answer <= len(product_list):
                validate = True # if answer is a possible choice.
            else:
                print("Ce chiffre ne correspond à aucun choix")
        return answer - 1

    def validate_answer_yes_no(self, question):
        """
        Method wich attends to validate an answer of user of type 'Yes/No'.
        This method verify if the answer is 'O' or 'N'.
        """
        self.create_space()
        questions = ["Voulez-vous valider votre choix ? (O/N): ",
                     "Voulez-vous enregistrer votre choix ? (O/N): "]
        while True:
            answer = input(questions[question])
            if answer == "O":
                return True
            elif answer == "N":
                return False
            else:
                print("Ce n'est pas une réponse valide\n"+
                      "les seuls réponses possibles étant 'O' (='Oui') ou 'N' (='Non')")


    def make_choice(self, liste):
        """
        Method wich displays elements of a list and
        returns the chosen element by user and its position inside
        this list.
        """
        for i, element in enumerate(liste):
            print(str(i + 1), "-", str(element))
        answer = self.validate_answer_int(liste)
        element = liste[answer]
        return answer, element


    def first_menu(self, index):
        """
        Method wich attends to manage the first menu and allows to
        dispatch to other menus or stops the menu
        (depending on user's choice)
        """
        answer, name = self.make_choice(self.first_menu_list)
        launched = True
        if answer == 0:
            index += 1 # go to category_menu
        elif answer == 1:
            index += 4 # go to user_menu
        elif answer == 2:
            print("Merci et à bientôt !")
            launched = False # close the program
        return launched, index, answer, name

    def category_menu(self, index):
        """
        Method wich attends to manage choice of categories.
        """
        answer, name = self.make_choice(self.category_list)
        if answer == -1:
            index -= 1 # go back to first menu
        else:
            index += 1 # go to sub_category menu
        return True, index, answer, name

    def sub_cat_menu(self, index, intern_index):
        """
        Method wich attends to manage choice of sub-categories.
        """
        answer, name = self.make_choice(self.sub_category_list[intern_index])
        if answer == -1:
            index -= 1 # go back to category menu
        else:
            index += 1 # go to products menu

        return True, index, intern_index, name

    def create_tablib(self, products_list, headers_list):
        """
        Method wich allows to create and display an object of library tablib.
        It displays a list of products.
        This method returns user's choice
        """
        data = tablib.Dataset()
        data.headers = headers_list # name of columns
        keys_list, index = ["product_name", "brand", "nutrition_score"], 1
        for dictionnary in products_list: # for each product
            value_to_append = []
            for key in keys_list:
                value_to_append.append(dictionnary[key]) # we find value
            value_to_append.insert(0, index) # we insert at the beginning its (index + 1)
            index += 1
            data.append(value_to_append) # we append to Tablib object
        print(data) # we displays data table
        # user has to make a choice
        answer = self.validate_answer_int(products_list, 1)
        return answer

    def display_informations_product(self, product):
        """
        Method wich displays all the informations about a given product.
        It returns datas wich are needed if the user wants to record his choice
        into database.
        """
        self.create_space()
        tuple_keys_list = [("barcode", "Code barre produit"), ("product_name", "Nom du produit"),
                           ("brand", "Marque"), ("nutrition_grade", "Grade nutritionnel"),
                           ("nutrition_score", "Score nutritionnel"), ("stores", "Magasins"),
                           ("url", "Url")]
        # we displays each information contained into tuple_keys_list
        for key, value in tuple_keys_list:
            print(value, "=", product[key])
        answer = self.validate_answer_yes_no(0) # the answer must be validate
        return answer, (product["barcode"], product["nutrition_score"])

    def product(self, index, name, products_list):
        """
        Method wich attends to manage and display products of a sub-category.
        It allows to access to substitutes of product the user has chosen.
        """
        if products_list == 0: # If we has not already communicated with database
            products_list = self.bdd.find_products(name) # we find products of a sub-category
        # we will displays a 'summary' of each product
        headers_list = ["Touche", "Nom produit", "Marque", "Score"]
        while True:
            os.system(self.command)
            print("Tableau Produits:\n", " ")
            answer = self.create_tablib(products_list, headers_list)
            if answer == -1: # we go back to sub-category menu
                return False, index, products_list, 0
            # else
            sub_answer, value_product = self.display_informations_product(products_list[answer])
            if sub_answer:
                index += 1 # we go to substitutes of the chosen product
                return True, index, products_list, value_product
            continue


    def recording_into_user(self, value_product, value_substitute):
        """
        Method wich deals with request for recording into database. Method
        use bdd object wich allows to communicate with database.
        """
        answer = self.validate_answer_yes_no(1)
        if answer: # if answer is yes (=True)
            self.bdd.record_table_user(value_product, value_substitute)
        else: # if answer is no (=False)
            print("Vous allez être redirigé vers le menu")

    def substitute(self, index, name, products_list, value):
        """
        Method wich attends to manage and display substitute products.
        At the end, if user want it, method uses a method that allows
        recording into database.
        """
        # substitute list of a given product (and a given nutriscore)
        substitute_list = self.bdd.find_products(name, value[1])
        headers_list = ["Touche", "Nom produit", "Marque", "Score"]
        while True:
            os.system(self.command)
            print("Tableau Substituts:\n", " ")
            answer = self.create_tablib(substitute_list, headers_list)
            if answer == -1:
                index -= 1 # we go back to product menu
                return True, index, products_list, 0
            sub = substitute_list[answer] # the substitute user has chosen
            # we displays all informations about this substitute
            sub_answer, value_substitute = self.display_informations_product(sub)
            if sub_answer: # if the user wants to record into database
                self.recording_into_user(value, value_substitute)
                # we go back to sub_category menu
                return False, index, products_list, value
            continue

    def products_menu(self, index, name, index_2):
        """
        Method wich allows to manage navigation through choice of products and choice
        of substitutes.
        """
        intern_index, products_list, value = 0, 0, 0
        # list of functions : first = manage products
        #                     second = manage substitutes of the chosen product
        functions_list = [self.product, self.substitute]
        launched = True
        while launched:
            # parameters needed for functions contained in functions_list
            parameters_list = [[intern_index, name, products_list],
                               [intern_index, name, products_list, value]]
            launched, intern_index, products_list, value = \
            functions_list[intern_index](*parameters_list[intern_index])
        index -= 1 # we go back to the sub-category menu
        return True, index, index_2, 0

    def user_menu(self):
        """
        Method wich allows to display and manage the user's menu (= list of all recordings the user
        made while he was using the program). This method allows to consults details of
        each recording).
        """
        # method wich returns a list of datas contained into table 'user'
        prod_sub_list = self.bdd.find_substitute()
        headers_list = ["Touche", "Nom produit", "Nutriscore produit",
                        "Nom substitut", "Nutriscore substitut"]
        while True:
            os.system(self.command)
            answer = self.create_tablib_user(prod_sub_list, headers_list)
            if answer == -1:
                break # we go back to first menu
            # we display informations about a line user has chosen
            self.display_informations_user(prod_sub_list[answer])

        return True, 0, 0, 0

    def create_tablib_user(self, user_list, headers_list):
        """
        Method wich allows to create and display an object of librairie tablib.
        It displays a list of products previously recorded by user.
        This method returns the choice of user.
        """
        data = tablib.Dataset()
        data.headers = headers_list
        # informations of products and substitutes we will display
        keys_list, index = ["name_product", "nutrition_score_product",
                            "name_substitute", "nutrition_score_sub"], 1
        for dictionnary in user_list: # for each line into table user
            value_to_append = [] # datas we will append in Dataset
            for key in keys_list: # for each information we will display
                value_to_append.append(dictionnary[key])
            value_to_append.insert(0, index)
            index += 1
            data.append(value_to_append)
        print(data) # we display dataset
        # we ask to user wich line he wants details
        answer = self.validate_answer_int(user_list, 2)
        return answer

    def create_space(self):
        """
        Method wich allows to properly separate two 'displays'
        """
        print("")
        print("#"*60)
        print("")

    def display_informations_user(self, product):
        """
        Method wich allows to completely display
        details of a product and its substitute.
        """
        self.create_space()
        # we create a list of tuples that contained a key and
        # its "display" name
        tuple_keys_product_list = [
            ("id_product", "code barre produit"), ("name_product", "nom produit"),
            ("brand_product", "marque produit"), ("url_product", "url produit"),
            ("nutrition_grade_product", "grade produit"),
            ("nutrition_score_product", "score produit"),
            ("stores_product", "magasins où trouver le produit"),
            ("name_category", "nom catégorie"), ("name_sub_category", "nom sous_catégorie")]

        tuple_keys_sub_list = [
            ("id_substitute", "code barre substitut"), ("name_substitute", "nom substitut"),
            ("brand_substitute", "marque substitut"), ("url_substitute", "url substitut"),
            ("nutrition_grade_sub", "grade substitut"), ("nutrition_score_sub", "score substitut"),
            ("stores_substitute", "magasins où trouver le substitut"),
            ("name_category", "nom catégorie"), ("name_sub_category", "nom sous_catégorie")]
        # we display each information about a product
        for key, value in tuple_keys_product_list:
            print(value, "=", product[key])
        self.create_space()
        print("Substitué par :")
        self.create_space()
        # then we display each information about its substitute
        for key, value in tuple_keys_sub_list:
            print(value, "=", product[key])

        input("Appuyez sur entrée :")

