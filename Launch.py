"""
Ceci est un module de docstring
"""
import Display as D
import BddIni as B

class Launch():
    """
    This class has the responsibility to manage the launching of program
    """

    def __init__(self):
        self.display = D.Display() # object of class Display
        self.bdd = B.BddIni() #object of class BDD_ini

    def main(self):
        """
        This method launch the program
        """
        self.display.welcome()
        success = self.bdd.complete_fill()
        if success: # if we have to fill the database
            self.display.menu() # display menu
