from flask import Flask
from flask import render_template, redirect, jsonify
import mariadb
import database
app = Flask(__name__)

app.config['SECRET_KEY'] ="super secret key"

#Vytvoří první connection do mariaDB a vytvoří db
database.vytvor_db()

#Pro manuální testování odkomentovat localhost a zakomentovat mariadb tady i v database.py

config = {
        'user': 'root',
        'password': 'secret',
        'host': 'mariadb',
        #'host': 'localhost',
        'port': 3306,
        'database': 'skoly'
    }

connection = mariadb.connect(**config)
cursor = mariadb.Cursor(connection)
#Vytvoří druhý connection do mariaDB přímo do db a vytvoří tabulky
database.vytvor_tabulky(cursor)

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def page_not_found(e):
    return render_template('500.html'), 500


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)