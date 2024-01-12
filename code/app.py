from flask import Flask
from flask import render_template, redirect, jsonify, request, flash
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
cursor.close()

@app.route('/', methods=['GET', 'POST'])
@app.route('/pristup', methods=['GET', 'POST'])
def zadani_klice_student():
    if request.method == "POST":
        #Omezit v budoucnu SQL Injection
        klic_student = request.form['klic_student']
        mistnost = request.form['mistnost']
        flash(f'{klic_student} | {mistnost}', category='info')
    return render_template('index.html')

@app.route('/rooms', methods=['GET', 'POST'])
def rooms():
    rooms = [{"name":"Pavel Beránek", "link":"https://github.com/pavelberanek91"}, {"name":"Pavel Jaššo", "link":"fividfub"}, 
            {"name":"Adam Heger", "link":"fividfub"}, {"name":"Místnost 1", "link":"fividfub"}]
    return render_template('rooms.html', rooms= reversed(rooms))

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def page_not_found(e):
    return render_template('500.html'), 500


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)