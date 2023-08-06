#CalDB Documentation

##Cal ++

Cal++ is a key/value data storaging system. 

	variable = "a string"
	anotherVariable = 22
##CalDB

Have this code at the top:

	from calDB import CalDB, array
	db = CalDB(__name_)
	db.start("<Database Name>")
To get data:

	data = db.read()
To add data:

	db.write("<key>","<value>")
To delete data:

	db.kill("<key>")


