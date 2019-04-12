import records

class BDD_ini(object):
	def __init__(self):
		pass

	def connection(self,utilisateur,mdp):
		self.database = records.Database("mysql+mysqlconnector://{}:{}@localhost".format(utilisateur,mdp))





"""
db = records.Database("mysql+mysqlconnector://{}:{}@localhost".format("root","mdp"))
with db.transaction() as conn:
    conn.query("CREATE USER  IF NOT EXISTS 'student'@'localhost' IDENTIFIED BY 'mdp'")
    warnings = conn.query("SHOW WARNINGS").all(as_dict=True)
print(warnings)

"""

		

