import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="Baotram1999@"
)

mycursor = mydb.cursor()

mycursor.execute("CREATE DATABASE mydatabase")