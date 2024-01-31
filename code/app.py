from flask import Flask
from flask import render_template, redirect, jsonify, request, flash
import database, app_logic
from werkzeug.utils import secure_filename

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

#Vytvoří druhý connection do mariaDB přímo do db a vytvoří tabulky
database.vytvor_tabulky()


@app.route('/', methods=['GET', 'POST'])
@app.route('/pristup', methods=['GET', 'POST'])
def zadani_klice_student():
    if request.method == "POST":
        klic_student = request.form['klic_student']
        mistnost = request.form['mistnost']
        flash(f'{klic_student} | {mistnost}', category='mess_success')
    return render_template('index.html')

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        if 'pridat_skolu' in request.form:
            nazev_skoly = request.form['nazev_skoly']
            obec = request.form['obec']
            database.pridej_skolu(nazev_skoly,obec)
        elif 'pridat_ucitel' in request.form:
            klic_ucitel = app_logic.generate_random_key()
            id_skoly = int(request.form['id_skola'])
            database.pridej_ucitele(klic_ucitel, id_skoly)
        elif 'odstran_skolu' in request.form:
            id_skoly = int(request.form['id_skoly_odstr'])
            database.odstran_skolu(id_skoly)
        elif 'odstran_ucitel' in request.form:
            id_ucitel = int(request.form['id_ucitel_odstr'])
            database.odstran_ucitele(id_ucitel)

        if 'zobrazit_skoly' in request.form:
            schools = database.vypis_skoly()
            print(schools)
            return render_template('admin.html', schools=schools)
        
        if 'zobrazit_ucitele' in request.form:
            teachers = database.vypis_ucitele()
            print(teachers)
            return render_template('admin.html', teachers=teachers)

    return render_template('admin.html')

@app.route('/create-room', methods=['GET', 'POST'])
@app.route("/create-room")
def create_room():
    if request.method == 'POST':
        nazev_mistnosti = request.form['roomName']
        popis_mistnosti = request.form['roomDescription']
        current_ucitel = 1
        database.pridej_mistnost(nazev_mistnosti, popis_mistnosti, current_ucitel) # Current ucitel bude hodnota ucitele, pro teď nastavena hodnota testovaciho ucitele
    return render_template('create_room.html')

@app.route('/create-assignment', methods=['GET', 'POST'])
@app.route("/create-assignment")
def create_assignment():
    if request.method == 'POST':
        nazev_ukolu = request.form['taskName']
        popis_ukolu = request.form['taskDescription']
        current_mistnost = 2
        database.pridej_ukol(nazev_ukolu, popis_ukolu, current_mistnost) # Current mistnost bude hodnota mistnosti, pro teď nastavena hodnota testovaci mistnosti
    return render_template('create_assignment.html')

@app.route("/rooms")
def rooms():
    return render_template('rooms.html')

@app.route('/assignment')
@app.route('/assignment', methods=['GET', 'POST'])
def assignment():
    if request.method == 'POST':
        if 'fileInput' in request.files:
            file = request.files['fileInput']
            if file and app_logic.allowed_file(file.filename):
                ukol = file.read()
                id_ukol = 1
                id_mistnost = 2
                id_student = 1
                database.odevzdej_ukol(ukol, id_ukol, id_mistnost, id_student)
                flash("Soubor byl úspěšně nahrán a odevzdán.", 'mess_success')
            else:
                flash("Chybný formát souboru. Povoleny jsou pouze soubory s příponou .py.", 'mess_error')
        else:
            flash("Soubor nebyl nahrán.", 'mess_error')

    return render_template('assignment.html')

@app.route('/new_student', methods=['GET', 'POST'])
@app.route("/new_student")
def new_student():
    if request.method == 'POST':
        email = request.form['email']
        email = app_logic.hash_email(email)
        id_skoly = int(request.form['idSkoly'])
        klic = app_logic.generate_random_key()
        if database.check_email(email) == None:
            database.pridej_zaka(email, klic, id_skoly)
        else:
            flash('Email již existuje!', category='error')
    return render_template('new_student.html')

@app.route

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def page_not_found(e):
    return render_template('500.html'), 500

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)