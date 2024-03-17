from flask import Flask, url_for, render_template, redirect, jsonify, request, flash, session
import mariadb
import database, app_logic
from flask_login import LoginManager, login_user, logout_user, login_required, current_user 
from werkzeug.utils import secure_filename

app = Flask(__name__)

app.config['SECRET_KEY'] ="super secret key"

loginManager = LoginManager(app)
loginManager.login_view = 'zadani_klice_student'

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

#root endpoint sloužící pro přihlášení
@app.route('/', methods=['GET', 'POST'])
@app.route('/pristup', methods=['GET', 'POST'])
def zadani_klice_student():
    if request.method == "POST":
        email = request.form['email_student']
        klic_student = request.form['klic_student']
        # metoda se koukne jestli je v databázi email, který uživatel zadal a případně vrátí i id
        isUser, id = database.check_login_student(email, klic_student) 
        if isUser:
            flash("Login Successfull", category="success")
            login_user(app_logic.User(id=id, ucitel=False))
            session['type'] = 'student' # parametrem metody login_user musí být instance třídy, co dědí UserMixin  
            return redirect(url_for('rooms'))
        else:
            flash("Wrong password or email", category="mess_error")
    return render_template('index.html')

@app.route('/teacher', methods=['GET', 'POST'])
def teacher_login():
    if request.method == "POST":
        klic_ucitel = request.form['klic_ucitel']
        # metoda se koukne jestli je v databázi email, který uživatel zadal a případně vrátí i id
        isUser, id = database.check_login_teacher(klic_ucitel) 
        if isUser:
            flash("Login Successfull", category="success")
            login_user(app_logic.User(id=id, ucitel=True))
            session['type'] = 'teacher' # parametrem metody login_user musí být instance třídy, co dědí UserMixin  
            return redirect(url_for('rooms'))
        else:
            flash("Neexistující klíč", category="mess_error")
    return render_template('teacher.html')

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        if 'pridat_skolu' in request.form:
            nazev_skoly = request.form['nazev_skoly']
            obec = request.form['obec']
            database.pridej_skolu(nazev_skoly,obec)
            flash("Škola byla úspěšně přidána!", 'mess_success')
        elif 'pridat_ucitel' in request.form:
            klic_ucitel = app_logic.generate_random_key()
            max_pokusy = 10
            pokusy = 0
            while pokusy < max_pokusy:
                check = database.check_keys_ucitel(klic_ucitel)
                if check is None:
                    # Klíč je unikátní, můžeš pokračovat
                    id_skoly = int(request.form['id_skola'])
                    if database.check_ids_skola(id_skoly) is not None:
                        database.pridej_ucitele(klic_ucitel, id_skoly)
                        flash("Učitel byl úspěšně přidán!", 'mess_success')
                        break
                    else:
                        flash("ID školy je neplatné!", 'mess_error')
                        break
                else:
                    # Klíč byl nalezen, vygeneruj nový a zkus znovu
                    klic_ucitel = app_logic.generate_random_key()
                    pokusy += 1
            else:
                flash("Nepodařilo se vygenerovat unikátní klíč učitele!", 'mess_error')
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
    if current_user.jeUcitel:
        return render_template('create_room.html')
    else:
        return render_template('404.html')

@app.route('/create-assignment', methods=['GET', 'POST'])
@app.route("/create-assignment")
@login_required
def create_assignment():
    if request.method == 'POST':
        nazev_ukolu = request.form['taskName']
        popis_ukolu = request.form['taskDescription']
        typ = request.form['taskType']
        current_mistnost = 1
        database.pridej_ukol(nazev_ukolu, popis_ukolu, typ, current_mistnost) # Current mistnost bude hodnota mistnosti, pro teď nastavena hodnota testovaci mistnosti
    if current_user.jeUcitel:
        return render_template('create_assignment.html')
    else:
        return render_template('404.html')

# endpoint pro zobrazení místností
@app.route("/rooms")
@login_required
def rooms():
    return render_template('rooms.html')

# endpoint pro jednotlivé úkoly, zde by měl být název, info a možnost odevzdat soubor
@app.route('/assignment')
@app.route('/assignment', methods=['GET', 'POST'])
@login_required
def assignment():
    if request.method == 'POST':
        if 'fileInput' in request.files:
            file = request.files['fileInput']

            if file and app_logic.allowed_file(file.filename):
                filename = file.filename
                velikost = len(file.stream.read())
                typ = app_logic.ziskat_typ_souboru(filename)

                file.stream.seek(0)

                ukol_content = file.stream.read().decode('utf-8')

                id_ukol = 1
                id_mistnost = 1
                id_student = 1
                database.odevzdej_ukol(ukol_content, typ, id_ukol, id_mistnost, id_student)
                database.zapis_metadata(id_ukol, velikost)

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
        
        # Omez počet pokusů na zabránění zacyklení
        max_pokusy = 10
        pokusy = 0
        
        while pokusy < max_pokusy:
            check_klic = database.check_keys_student(klic)
            
            if check_klic is None:
                # Klíč je unikátní, můžeš pokračovat
                if database.check_email(email) is not None:
                    flash('Email již existuje!', 'mess_error')
                    break
                elif database.check_ids_skola(id_skoly) is not None:
                    database.pridej_zaka(email, klic, id_skoly)
                    flash('Student byl úspěšně přidán!', 'mess_success')
                    break
                else:
                    flash('ID školy je neplatné!', 'mess_error')
                    break
            else:
                # Klíč byl nalezen, vygeneruj nový a zkus znovu
                klic = app_logic.generate_random_key()
                pokusy += 1
        else:
            # Pokud byly vyčerpány všechny pokusy, vrátit chybovou zprávu
            flash('Nepodařilo se vygenerovat unikátní klíč studenta!', 'mess_error')
            
    return render_template('new_student.html')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def page_not_found(e):
    return render_template('500.html'), 500

# Tahle metoda by měla nějak udržovat uživatele v sessionu ale úplně tomu nerozumím
@loginManager.user_loader
def load_user(user_id):
    if session['type'] == 'teacher':
        return app_logic.User(id=user_id, ucitel=True)
    if session['type'] == 'student':
        return app_logic.User(id=user_id, ucitel=False)
    return None

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('zadani_klice_student'))

@app.route('/get_schools')
def get_schools():
    all_schools = database.vypis_skoly()
    return jsonify(all_schools)

# Funkce pro získání seznamu učitelů
@app.route('/get_teachers')
def get_teachers():
    all_teachers = database.vypis_ucitele()
    return jsonify(all_teachers)

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)