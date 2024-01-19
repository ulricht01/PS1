from flask import Flask
from flask import render_template, redirect, jsonify, request, flash
import mariadb
import database, app_logic
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

connection, cursor = database.otevri_spojeni()
#Vytvoří druhý connection do mariaDB přímo do db a vytvoří tabulky
database.vytvor_tabulky(cursor)
cursor.close()
connection.close()

@app.route('/', methods=['GET', 'POST'])
@app.route('/pristup', methods=['GET', 'POST'])
def zadani_klice_student():
    if request.method == "POST":
        #Omezit v budoucnu SQL Injection
        klic_student = request.form['klic_student']
        mistnost = request.form['mistnost']
        flash(f'{klic_student} | {mistnost}', category='info')
    return render_template('index.html')

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method=='POST':
        if 'pridat_skolu' in request.form:
            nazev_skoly = request.form['nazev_skoly']
            connection, cursor = database.otevri_spojeni()
            database.pridej_skolu(cursor, nazev_skoly)
            connection.commit()
            connection.close()
        elif 'pridat_ucitel' in request.form:
            klic_ucitel = app_logic.generate_random_key()
            id_skoly = int(request.form['id_skola'])
            connection, cursor = database.otevri_spojeni()
            database.pridej_ucitele(cursor, klic_ucitel, id_skoly)
            connection.commit()
            connection.close()
    return render_template('admin.html')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def page_not_found(e):
    return render_template('500.html'), 500


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)