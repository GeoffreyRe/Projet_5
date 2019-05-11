"""
Ceci est une docstring de module
"""
class ProductClassifier():
    """ Class that will verify values from Openfoodfacts API"""
    def __init__(self):
        self.variables_list = ["_id", "nutrition_grades", "product_name",
                               "url", "stores", "brands", "nutriments"]

        self.stores_list = ["Carrefour", "Carrefour Market", "Carrefour Planet",
                            "Carrefour Express", "Carrefour GB", "Colruyt", "Spa",
                            "Delhaize", "Delhaize City", "Proxy Delhaize",
                            "AD Delhaize", "Shop\'n Go", "Albert Heijn", "Intermarché",
                            "Cora", "Match", "Smatch", "Louis Delhaize", "Aldi", "Lidl",
                            "Magasins U", "Super U", "Hyper U", "Auchan", "Noz", "Casino",
                            "Leclerc", "Géant", "Dia", "Edeka", "magasins diététiques"]
    @staticmethod
    def capital_letter(str_list):
        """
        method that put capital letter at
        the beginning of each word of a list
         """
        title_list = []
        for string in str_list:
            title_list.append(string.title())
        return title_list
    @staticmethod
    def separate_stores(stores):
        """
        method that separate and isolate each store of a product.
        it transforms a string of store into a list of "formatted"
        stores.
        """
        stores_list_formatted = []
        stores_list = stores.split(",")
        for store in stores_list:
            stores_list_formatted.append(store.strip())
        return stores_list_formatted

    def verify_stores(self, stores):
        """
        method that verify if a store is known or not
        """
        verified_stores = []
        stores = self.separate_stores(stores)
        for store in stores:
            if store == "":
                return ""
            elif store in self.stores_list:
                verified_stores.append(store)
        if len(verified_stores) >= 1:
            return verified_stores
        return ""

    def remove_bad_products(self, list_products):
        """
        method that removes products that don't satisfy conditions.
        If a characteristic of a product is missing, then the product
        is removed.
        """
        good_products = []
        for product in list_products:
            if "" in product:
                pass
            else:
                good_products.append(product)
        return good_products

    def separate_brands(self, brands):
        """
        method that returns the first brand of a product
        """
        if "," in brands:
            brands_list = brands.split(",")
            return brands_list[0].strip()
        return brands

    def complete_check(self, list_products):
        """
        Method wich completely checks product from a sub_category with other
        methods.
        """
        verified_products = []
        for product in list_products: # for each product
            verified_product = []
            for i, variable in enumerate(product):
                if i == self.variables_list.index("stores"):
                    variable = self.verify_stores(variable)
                elif i == self.variables_list.index("brands"):
                    variable = self.separate_brands(variable)
                verified_product.append(variable)
            verified_products.append(verified_product)
        verified_products = self.remove_bad_products(verified_products)
        return verified_products
