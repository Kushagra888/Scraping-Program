import mysql.connector

db = mysql.connector.connect(host='localhost', user='Kushagra', passwd='kushagrasql123pass')

cursor = db.cursor()

cursor.execute('CREATE DATABASE scraping_project')
