"""
Ceci est un docstring de module
"""
import requests # 'requests' allows to send requests to an API
import ProductClassifier as productC

class Api():
    """
    This class has the responsibility to manage calls with API
    OpenFoodfact and to retrieve different needed informations
    of each product.
    """
    def __init__(self):
        # list that contains informations of each product
        self.products_list = []
        # names of different keys we need
        self.variables_list = ["_id", "nutrition_grades", "product_name", "url",
                               "stores", "brands", "nutriments"]
        self.variables_list_2 = [0, 0, 0, 0, 0, 0, "nutrition-score-fr"]
        self.checker = productC.ProductClassifier() # a checker we are going to use
        self.products = None # products is going to be initialize in method "get_request_product"

    def get_request_product(self, categorie):
        """
        Method that allows to get products from a category thanks to API
        OpenFoodFacts. This method returns a list of products.
         """
        http_link = ("https://be-fr.openfoodfacts.org/cgi/search.pl?search_simple=1&action=process&"
                     "tagtype_0=categories&tag_contains_0=contains&tag_0={}"
                     "&sort_by=unique_scans_n&page_size=200&json=1")

        try:
            request = requests.get(http_link.format(categorie))
        except: # if we can't get response from API (problem of connection,...)
            self.products = {}
            return self.products
        request = request.json()
        self.products = request["products"]
        return self.products # returns all the products API has given

    @staticmethod
    def find_value(dictionary, key, key_2):
        """
        This method allows to find a specific value of a product thanks
        to a key. Sometimes, we need two keys
        """
        if key_2 == 0: # if we only need one key
            try:
                dictionary_value = dictionary[key]
            except KeyError: # if key doesn't exist
                dictionary_value = ""
        elif key_2 != 0: # if we need two keys
            try:
                dictionary_value = dictionary[key][key_2]
            except KeyError:
                dictionary_value = ""

        return str(dictionary_value)

    def find_informations(self, categorie):
        """
        Method that allows to find informations we need (barcode,...) for each product
        found in a given sub_category. Then, this method add to 'products list' each
        processed product.
        """
        self.get_request_product(categorie)
        for product in self.products: # we process each product with a loop
            variables_of_a_product = [] # list that will contain value of a product
            # second loop that will use each key in self.variables_list
            for i, variable_name in enumerate(self.variables_list):
                value = self.find_value(product, variable_name, self.variables_list_2[i]).strip()
                variables_of_a_product.append(value)
            self.products_list.append(variables_of_a_product) # we add the processed product
        # at the end, we check each product in this list (see class ProductClassifier)
        self.use_the_checker()

    def use_the_checker(self):
        """
        Method that use ProductClassifier object. It allows to analyse collected datas
        with class method 'complete_check'
        """
        self.products_list = self.checker.complete_check(self.products_list)

    def reset_products_list(self):
        """
        Method that reset attribute 'products_list'. We use this method
        wbefore we want to get products of an other category.
        """
        self.products_list = []
