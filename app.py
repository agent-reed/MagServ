from flask import Flask, jsonify, request, redirect
import psycopg2
from prettytable import PrettyTable

app = Flask(__name__)

class User:

    def __init__(self, name, psswrd, email, distributor, salesperson):
        self.name = name
        self.psswrd = psswrd
        self.email = email
        self.distributor = distributor
        self.salesperson = salesperson
        self.favorites = [] 

        print ("new user created: " + self.name)

    def add_favorite(self, trick):
        self.favorites.append(favorite)

con = None
def createDBConnection():

	try:
		con = psycopg2.connect(database='gentryar', user='gentryar', password='ginger whale station')

	except psycopg2.DatabaseError as e:
	    print "Connection Error." + e
	    sys.exit(1)

	finally:
		return con

def addUserToDB(newUser):
	con = createDBConnection()

	try:
		cur = con.cursor()
		cur.execute("INSERT INTO users VALUES(%s,%s,%s,%s,%s)", (newUser.name, newUser.psswrd, newUser.email, newUser.distributor, newUser.salesperson))
		con.commit()
		print ("Added '" + name + " to the database.")

	except psycopg2.DatabaseError as e:

		print "Error adding a user." + e

		if con:
			con.rollback
		sys.exit(1)

	finally:
		if con:
			con.close

		return


@app.route('/create/', methods=['POST'])
def createUser():
	if request.method == 'POST':

		name = request.form['username']
		psswrd = request.form['psswrd']
		email = request.form['email']
		distributor = request.form['distributor']
		salesperson = request.form['salesperson']
		print "processed form"

		newUser = User(name,psswrd,email,distributor,salesperson)
		addUserToDB(newUser)

		return redirect('/data')

	else:
		return redirect('/')

@app.route('/bug/', methods=['POST'])
def bugReport():
	if request.method == 'POST':

		report = request.form['report']
		with open("bugs.txt","a") as fo:
  			fo.write(report + '\n@@@@@@@@@@@@@@@@\n')
		return report

	else:
		return redirect('/')
 

@app.route('/')
def index():
	print "Accessed the server"
	return send_file('magswitch-logo.png')


@app.route('/data')
def names():
	
	con = createDBConnection()

	try:
		cur = con.cursor()
		cur.execute("SELECT * FROM users")
		t = PrettyTable(['|______.Name.______|', '|______.Password.______|', '|________.Email._________|', '|___.Distributor.___|', '|___.Salesperson.__|'])
		for record in cur:
			t.add_row([record[0],record[1],record[2],record[3],record[4]])
		return t.get_html_string()
		 

	except psycopg2.DatabaseError as e:

		if con:
			con.rollback

		print "Error displaying the users." + e
		sys.exit(1)



if __name__ == '__main__':
	app.debug = True
	app.run()
