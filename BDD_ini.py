import records
class BDD_ini(object):
	def __init__(self):
		pass

	def connection(self,utilisateur,mdp):
		self.database = records.Database("mysql+mysqlconnector://{}:{}@localhost".format(utilisateur,mdp))

	def find_database(self):
		request = self.database.query("SET NAMES 'utf8mb4'")
		request = self.database.query("USE mysql")

	def create_user(self):
		request = self.database.query("CREATE USER IF NOT EXISTS 'projet_5'@'localhost' IDENTIFIED BY ''")
		#request = self.database.query("GRANT ALL PRIVILEGES ON elevage.* TO 'projet_5'@'localhost'")
		return request
		

	def pull_requests(self):
		request = self.database.query("SHOW WARNINGS")

		return request
		


if __name__ == "__main__":
	initialisation = BDD_ini()
	initialisation.connection("root","Geof4589")
	initialisation.find_database()
	initialisation.create_user()
	#initialisation.pull_requests()

