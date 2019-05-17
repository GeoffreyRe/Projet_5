"""
Class that has the responsibility to fill different tables of
database.
"""
import json
import copy
import records
import Api as A

class BddIni():
    """
    Class that has the responsibility to fill different tables of
    database.
    """
    def __init__(self):
        self.stores_list = ["Carrefour", "Carrefour Market", "Carrefour Planet",
                            "Carrefour Express", "Carrefour GB", "Colruyt", "Spa",
                            "Delhaize", "Delhaize City", "Proxy Delhaize", "AD Delhaize",
                            "Shop\\'n Go", "Albert Heijn", "Intermarché", "Cora", "Match",
                            "Smatch", "Louis Delhaize", "Aldi", "Lidl", "Magasins U",
                            "Super U", "Hyper U", "Auchan", "Noz", "Casino", "Leclerc",
                            "Géant", "Dia", "Edeka", "magasins diététiques"]
        self.category_list = ["Produits laitiers", "Boissons", "Petit-déjeuners",
                              "Viandes", "Desserts"]
        self.sub_category_list = [
            ["Laits", "Beurres", "Boissons lactées", "Fromages"],
            ["Sodas", "Boissons au thé", "Boissons énergisantes"],
            ["Céréales pour petit-déjeuner", "Pâtes à tartiner", "Confitures et marmelades"],
            ["Charcuteries", "Volailles"],
            ["Desserts au chocolat", "Compotes", "Desserts lactés", "Snacks sucrés"]
            ]

        self.config = None # is going to be initialize in method 'import_json_data()'
        self.database = None # is going to be initialize in method 'connection()'
        self.dict_of_stores = None # is going to be initialize in method 'retrieve_store_dict()'
        self.openfoodfact = A.Api()

    def import_json_data(self):
        """
        Method that imports datas contained into json file
        """
        # we use method of module json
        with open("config.json", "r") as file:
            self.config = json.load(file)

    def connection(self):
        """
        Method that allows connection with mysql with an user and a password
        """
        sent_con = "mysql+mysqlconnector://{}:{}@localhost"
        self.database = records.Database(sent_con.format(self.config["User"], self.config["Pw"]))

    def go_to_database(self):
        """
        Method that allows to go to the right database and
        changes encoding
        """
        self.database.query("SET NAMES 'utf8mb4'")
        self.database.query("USE {}".format(self.config["Database"]))

    def check_initialisation(self):
        """
        Method that verifies constant 'initialisation' and
        change it.
        """
        if self.config["Initialisation"] == 0:
            self.config["Initialisation"] = 1
            return True

        return False
    def add_single_string(self, string):
        """
        method that adds " " " in order to insert values
        of type char, varchar,...
        """
        try:
            string = "\"" + string + "\""
        except:
            string = string
        return string

    def fill_table_store(self):
        """
        Method that fills table store from
        attribute stores_list.
        """
        for store in self.stores_list:
            sentence = "INSERT INTO Store VALUES (NULL, {})"
            self.database.query(sentence.format(self.add_single_string(store)))

    def retrieve_store_dict(self):
        """
        Method that returns a dictionnary where a key correspond to the name of a store and
        its value correspond to id of this store in table 'store'.
        """
        self.dict_of_stores = {}
        stores = self.database.query("SELECT * FROM Store").all(as_dict=True)
        for store in stores:
            self.dict_of_stores[store["name"]] = store["id"]
        return self.dict_of_stores

    def fill_table_category(self):
        """
        Method wich inserts datas into table 'Category'
        Méthode qui insére les données dans la table Category
        """
        for category in self.category_list:
            category = self.add_single_string(category)
            self.database.query("INSERT INTO Category VALUES (NULL,{})".format(category))

    def fill_table_sub_category(self):
        """
        Method that inserts datas into table 'Sub_category'
        """
        # sub_category contained in sub_category_list is a list
        # and the index of this list corresponds to index of
        # the category contained in category_list
        for index, sub_category in enumerate(self.sub_category_list):
            category_name = self.add_single_string(self.category_list[index])
            # We retrieve id of category wich corresponds to sub_category
            # example : category of 'laits' is 'produits laitiers'
            query_1 = "SELECT id FROM Category WHERE name = {}".format(category_name)
            foreign_key_id = ((self.database.query(query_1)).all(as_dict=False))[0]["id"]
            for sub_cat in sub_category:
                sub_cat = self.add_single_string(sub_cat)
                sentence = "INSERT INTO Sub_category VALUES (NULL, {0},{1})"
                query_2 = sentence.format(sub_cat, foreign_key_id)
                self.database.query(query_2)

    def call_api(self, sub_category):
        """
        Method wich allows to retrieve products of a sub_category
        (thanks to an object of Class API)
        """
        self.openfoodfact.find_informations(sub_category)
        products_list = copy.deepcopy(self.openfoodfact.products_list)
        self.openfoodfact.reset_products_list()
        return products_list

    def find_correspondence_store(self, product):
        """
        Method wich allows to find 1 (or more) id of store(s) wich correspond to a
        product.
        """
        # we find index of value "stores"
        index = self.openfoodfact.variables_list.index("stores")
        stores = product[index] # we find (1 or more) stores associated with a product
        stores_id = []
        for store in stores:
            stores_id.append(self.dict_of_stores[store]) # we find id of each store
        product.remove(stores)
        product.insert(index, stores_id) # we change names of stores into id of stores
        return product

    def fill_table_assoc(self, product):
        """
        Method wich allows to fill table 'Assoc_product_store' with
        barcode of product and 1 (or more) of correspondent store(s).
        """
        index_stores = self.openfoodfact.variables_list.index("stores")
        index_barcode = self.openfoodfact.variables_list.index("_id")
        stores_product = self.add_single_string(product[index_stores])
        barcode_product = self.add_single_string(product[index_barcode])
        for store in stores_product:
            query = "INSERT INTO Assoc_product_store VALUES ({},{})".format(barcode_product, store)
            self.database.query(query)

    def fill_table_product(self):
        """
        Method wich allows to fill table Product with all informations collected by API
        then processed by a ProductClassifier object.
        """
        counter = 0 # counter of sub_categories wich have been append to bdd.
        for sub_category in self.sub_category_list:
            for sub_cat in sub_category:
                counter += 1
                print("{} catégorie(s) télécharée(s)".format(counter))
                # for each product in a sub_category
                for product in self.call_api(sub_cat):
                    product = self.find_correspondence_store(product)
                    list_value = [] # list of values of one product
                    for index in [0, 2, 5, 3, 1, 6]: # index of each information we need
                        value = self.add_single_string(product[index])
                        list_value.append(value)
                    value = self.database.query("SELECT id FROM Sub_category\
                    WHERE name={}".format(self.add_single_string(sub_cat)))
                    value = value.all(as_dict=True)[0]["id"] # we find id of sub_cat in bdd
                    list_value.append(value)
                    query = "INSERT INTO product VALUES({},{},{},\
                    {},{},{},{})".format(*list_value).replace("\n", "")
                    try:
                        self.database.query(query) # we insert the product
                        self.fill_table_assoc(product) # we fill table Assoc
                    except:
                        pass # if there is a problem (primary key constraint,...)
                             # we don't add the product

    def connection_and_init(self):
        """
        Method wich calls 3 other methods wich are needed to communiquate with database.
        """
        self.import_json_data()
        self.connection()
        self.go_to_database()

    def complete_fill(self):
        """
        Method wich gathers togheter methods in order to completely fill the database.
        It returns True if fillig is a success or False if filling has failed.
        """
        try:
            self.connection_and_init()
        except:
            sentence = ("La connexion à la base de données a échouée, "
                        + "vérifiez vos identifiants dans 'config.json'")
            print(sentence)
            input("Appuyez sur 'Enter' pour arrêter le programme")
            return False
        if self.check_initialisation(): # if database is not already filled
            print("La base de données se remplit, un petit instant svp...")
            self.fill_table_store()
            self.fill_table_category()
            self.fill_table_sub_category()
            self.retrieve_store_dict()
            self.fill_table_product()
            with open("config.json", "w") as file:
                file.write(json.dumps(self.config, ensure_ascii=False, indent=4))
        else:
            print("La base de données est déjà remplie")
            input("Appuyez sur 'Enter' pour être dirigé vers le menu")
        return True
