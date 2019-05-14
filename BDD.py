"""
Ceci est un docstring de module
"""
import json
import records
class BDD():
    """
    This class has the responsibility to manage recovery of
    datas (inside database) under user's choices.
    """
    def __init__(self):
        """
        Initialize connection with database
        """
        self.import_json_data()
        self.connection()
        self.go_to_database()

    def import_json_data(self):
        """
        Method that import file 'config.json' and transform it into
        python object
        """
        with open("config.json", "r") as file:
            self.config = json.load(file)

    def connection(self):
        """
        Method that allows connection to database thanks to user and
        password of this user.
        """
        sentence = "mysql+mysqlconnector://{}:{}@localhost"
        query = sentence.format(self.config["User"], self.config["Pw"])
        try:
            self.database = records.Database(query) # send query to database
        except:
            pass

    def go_to_database(self):
        """
        Method that allows to go to the right database
        """
        try:
            self.database.query("SET NAMES 'utf8mb4'")
            self.database.query("USE {}".format(self.config["Database"]))
        except:
            pass

    def find_substitute(self):
        """
        Method that send a big request for the purpose of retrieve all the informations
        of products in table 'user' (recorded by user itself).
        """
        sub_query_1 = "SELECT GROUP_CONCAT(name SEPARATOR ', ') FROM Assoc_product_store \
        INNER JOIN Store ON Store.id = Assoc_product_store.id_store \
        WHERE barcode_product = prod.barcode" # find all stores of a product

        sub_query_2 = "SELECT GROUP_CONCAT(name SEPARATOR ', ') FROM Assoc_product_store \
        INNER JOIN Store ON Store.id = Assoc_product_store.id_store \
        WHERE barcode_product = sub.barcode" # find all stores of a substitute
        # Big query that retrieves all informations of products and substitutes
        query = "SELECT User.id_product, prod.product_name AS name_product,prod.brand \
        AS brand_product, prod.url AS url_product, prod.nutrition_grade \
        AS nutrition_grade_product, prod.nutrition_score AS nutrition_score_product, \
        ({}) AS stores_product, User.id_substitute, sub.product_name AS name_substitute, \
        sub.brand AS brand_substitute, sub.url AS url_substitute, sub.nutrition_grade \
        AS nutrition_grade_sub, sub.nutrition_score AS nutrition_score_sub, \
        ({}) AS stores_substitute, Category.name AS name_category, Sub_category.name \
        AS name_sub_category FROM User \
        INNER JOIN Product AS prod ON prod.barcode = User.id_product \
        INNER JOIN Product AS sub ON sub.barcode = User.id_substitute \
        INNER JOIN Sub_category ON Sub_category.id = prod.id_sub_category\
        INNER JOIN Category \
        ON Category.id = Sub_category.id_category".format(sub_query_1, sub_query_2)
        sub_list = self.database.query(query).all(as_dict=True) # we change it into dict
        return sub_list

    def find_products(self, sub_category, nutrition_score=""):
        """
        Method that allows to get 10 random products of a sub_category.
        Sometimes, theses products must have a lower nutriscore than a given
        nutriscore (as a parameter).
        """
        # We retrieve id of a sub_category
        query_id_sub_cat = "SELECT id FROM Sub_category \
                            WHERE name = {}".format("'" + sub_category + "'")

        id_sub_cat = self.database.query(query_id_sub_cat).all(as_dict=True)[0]["id"]
        # We retrieve names of different stores associated to a product
        sub_query = "SELECT GROUP_CONCAT(name SEPARATOR ', ') FROM Assoc_product_store \
                     INNER JOIN Store ON Store.id = Assoc_product_store.id_store \
                     WHERE barcode_product = barcode"

        if nutrition_score == "":
            # query to retrieve 10 products of a sub_category
            query = "SELECT barcode, product_name, brand, nutrition_score, url, \
            nutrition_grade, ({}) as stores FROM Product WHERE id_sub_category = {} \
            ORDER BY RAND() LIMIT 10".format(sub_query, id_sub_cat)

        else:
            # there is an aditionnal condition
            query = "SELECT barcode, product_name, brand, url, nutrition_score, \
                     nutrition_grade, ({}) as stores FROM Product WHERE id_sub_category = {}\
                     AND nutrition_score < {} \
                     ORDER BY RAND() LIMIT 10".format(sub_query, id_sub_cat, nutrition_score)

        products_list = self.database.query(query)

        products_list = products_list.all(as_dict=True)

        return products_list

    def record_table_user(self, product, substitute):
        """
        Method that allows to record datas into table 'user'
        """
        id_product, id_substitute = product[0], substitute[0]
        query = "INSERT INTO User VALUES({},{})".format(id_product, id_substitute)
        try:
            self.database.query(query)
            print("votre enregistrement a bien été effectué")
        except:
            print("Il semblerait qu'un problème soit survenu" + ", l'enregistrement a donc échoué")

if __name__ == "__main__":
    BDD = BDD()
    print(BDD.find_substitute())
        