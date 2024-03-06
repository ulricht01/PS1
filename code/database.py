import mariadb
import hashlib
import app_logic
from app_logic import User

def otevri_spojeni():
    config = {
        'user': 'root',
        'password': 'secret',
        'host': 'mariadb',
        #'host': 'localhost',
        'port': 3306,
        'database': 'skoly',
    }
    connection = mariadb.connect(**config)
    cursor = mariadb.Cursor(connection)
    return connection, cursor
    

def vytvor_db():
    config = {
            'user': 'root',
            'password': 'secret',
            'host': 'mariadb',
            #'host': 'localhost',
            'port': 3306,
        }
    connection = mariadb.connect(**config)
    cursor = mariadb.Cursor(connection)
    cursor.execute("CREATE DATABASE IF NOT EXISTS skoly")

def vytvor_tabulky():
    connection, cursor = otevri_spojeni()
    cursor.execute("""CREATE TABLE IF NOT EXISTS skoly(
                                id_skola INT(6) NOT NULL AUTO_INCREMENT PRIMARY KEY,
                                nazev_skola VARCHAR(45) NOT NULL,
                                obec VARCHAR(45) NOT NULL,
                                dt_create TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                                active_flag VARCHAR(1) NOT NULL
                            ) ENGINE=InnoDB;""")
            
    cursor.execute("""CREATE TABLE IF NOT EXISTS ucitele(
                                id_ucitel INT(6) NOT NULL AUTO_INCREMENT PRIMARY KEY,
                                klic VARCHAR(8) NOT NULL UNIQUE,
                                id_skola INT(6) NOT NULL,
                                dt_create TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                                active_flag VARCHAR(1) NOT NULL,
                                CONSTRAINT `fk_ucitele_skoly`
                                    FOREIGN KEY (id_skola) REFERENCES skoly (id_skola)
                                    ON DELETE CASCADE
                                    ON UPDATE RESTRICT
                            ) ENGINE=InnoDB;""")
            
    cursor.execute("""CREATE TABLE IF NOT EXISTS studenti(
                                id_student INT(6) NOT NULL AUTO_INCREMENT PRIMARY KEY,
                                email VARCHAR(70) NOT NULL UNIQUE,
                                klic VARCHAR(8) NOT NULL,
                                id_skola INT(6) NOT NULL,
                                dt_create TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                                active_flag VARCHAR(1) NOT NULL,
                                CONSTRAINT `fk_studenti_skoly`
                                    FOREIGN KEY (id_skola) REFERENCES skoly (id_skola)
                                    ON DELETE CASCADE
                                    ON UPDATE RESTRICT
                            ) ENGINE=InnoDB;""")
            
    cursor.execute("""CREATE TABLE IF NOT EXISTS mistnosti(
                                id_mistnost INT(6) NOT NULL AUTO_INCREMENT PRIMARY KEY,
                                nazev_mistnosti VARCHAR(10) NOT NULL,
                                popis VARCHAR(125) CHARACTER SET utf8mb4 NOT NULL,
                                id_ucitel INT(6) NOT NULL,
                                dt_create TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                                active_flag VARCHAR(1) NOT NULL,
                                CONSTRAINT `fk_mistnosti_ucitele`
                                    FOREIGN KEY (id_ucitel) REFERENCES ucitele (id_ucitel)
                                    ON DELETE CASCADE
                                    ON UPDATE RESTRICT
                            ) ENGINE=InnoDB;""")

    cursor.execute("""CREATE TABLE IF NOT EXISTS ukoly(
                                id_ukol INT(6) NOT NULL AUTO_INCREMENT PRIMARY KEY,
                                nazev_ukol VARCHAR(25) NOT NULL,
                                popis VARCHAR(250),
                                typ ENUM('Samostatný projekt', 'Skupinová práce', 'Seminární práce', 'Test', 'Domácí práce', 'Školní práce') NOT NULL,
                                id_mistnost INT(6) NOT NULL,
                                dt_create TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                                active_flag VARCHAR(1) NOT NULL,
                                CONSTRAINT `fk_ukoly_mistnosti`
                                    FOREIGN KEY (id_mistnost) REFERENCES mistnosti (id_mistnost)
                                    ON DELETE CASCADE
                                    ON UPDATE RESTRICT
                            ) ENGINE=InnoDB;""")

    cursor.execute("""CREATE TABLE IF NOT EXISTS odevzdane_ukoly(
                                id_ode_ukol INT(6) NOT NULL AUTO_INCREMENT PRIMARY KEY,
                                file BLOB NOT NULL,
                                typ VARCHAR(18) NOT NULL,
                                id_ukol INT(6) NOT NULL,
                                id_mistnost INT(6) NOT NULL,
                                id_student INT(6) NOT NULL,
                                dt_create TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                                CONSTRAINT `fk_odevzdane_ukoly_ukoly`
                                    FOREIGN KEY (id_ukol) REFERENCES ukoly (id_ukol)
                                    ON DELETE CASCADE
                                    ON UPDATE RESTRICT,
                                CONSTRAINT `fk_odevzdane_ukoly_mistnosti`
                                    FOREIGN KEY (id_mistnost) REFERENCES mistnosti (id_mistnost)
                                    ON DELETE CASCADE
                                    ON UPDATE RESTRICT,
                                CONSTRAINT `fk_odevzdane_ukoly_studenti`
                                    FOREIGN KEY (id_student) REFERENCES studenti (id_student)
                                    ON DELETE CASCADE
                                    ON UPDATE RESTRICT
                            ) ENGINE=InnoDB;""")

    cursor.execute("""CREATE TABLE IF NOT EXISTS metadata(
                                id_meta INT(6) NOT NULL AUTO_INCREMENT PRIMARY KEY,
                                id_ode_ukol INT(6) NOT NULL,
                                velikost INT(8) NOT NULL,
                                dt_create TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                                CONSTRAINT `fk_metadata_odevzdane_ukoly`
                                    FOREIGN KEY (id_ode_ukol) REFERENCES odevzdane_ukoly (id_ode_ukol)
                                    ON DELETE CASCADE
                                    ON UPDATE RESTRICT
                            ) ENGINE=InnoDB;""")

    cursor.execute("""CREATE TABLE IF NOT EXISTS mistnosti_has_studenti(
                                id_student INT(6) NOT NULL,
                                id_mistnost INT(6) NOT NULL,
                                dt_create TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                                CONSTRAINT `fk_studenti_mistnosti_studenti`
                                    FOREIGN KEY (id_student) REFERENCES studenti (id_student)
                                    ON DELETE CASCADE
                                    ON UPDATE RESTRICT,
                                CONSTRAINT `fk_studenti_mistnosti_mistnosti`
                                    FOREIGN KEY (id_mistnost) REFERENCES mistnosti (id_mistnost)
                                    ON DELETE CASCADE
                                    ON UPDATE RESTRICT,
                                PRIMARY KEY (id_student, id_mistnost)
                            ) ENGINE=InnoDB;""")
    

    cursor.close()
    connection.close()
def pridej_skolu(nazev_skola, obec):
    connection, cursor = otevri_spojeni()
    cursor.execute(""" INSERT INTO skoly (nazev_skola, obec, active_flag) VALUES (%s, %s, "Y")""", (nazev_skola,obec,))
    cursor.close()
    connection.commit()
    connection.close()

def pridej_ucitele(klic_ucitel, id_skoly):
    connection, cursor = otevri_spojeni()
    cursor.execute(""" INSERT INTO ucitele (klic, id_skola, active_flag) VALUES (%s, %s, "Y")""", (klic_ucitel, id_skoly,))
    cursor.close()
    connection.commit()
    connection.close()

def odstran_ucitele(id_ucitel):
    connection, cursor = otevri_spojeni()
    cursor.execute(""" DELETE FROM ucitele WHERE id_ucitel = (%s)""", (id_ucitel,))
    cursor.close()
    connection.commit()
    connection.close()

def odstran_skolu(id_skola):
    connection, cursor = otevri_spojeni()
    cursor.execute(""" DELETE FROM skoly WHERE id_skola = (%s)""", (id_skola,))
    cursor.close()
    connection.commit()
    connection.close()

def pridej_zaka(email, klic, id_skola):
    connection, cursor = otevri_spojeni()
    cursor.execute(""" INSERT INTO studenti (email, klic, id_skola, active_flag) VALUES (%s, %s, %s, "Y")""", (email, klic, id_skola,))
    cursor.close() 
    connection.commit()
    connection.close()

def pridej_ukol(nazev_ukol, popis, typ, id_mistnost):
    connection, cursor = otevri_spojeni()
    cursor.execute(""" INSERT INTO ukoly (nazev_ukol, popis, typ, id_mistnost, active_flag) VALUES (%s, %s, %s, %s, "Y")""", (nazev_ukol, popis, typ, id_mistnost,))
    cursor.close() 
    connection.commit()
    connection.close()

def pridej_mistnost(nazev_mistnosti, popis, id_ucitel):
    connection, cursor = otevri_spojeni()
    cursor.execute(""" INSERT INTO mistnosti (nazev_mistnosti, popis, id_ucitel, active_flag) VALUES (%s, %s, %s, "Y")""", (nazev_mistnosti, popis, id_ucitel,))
    cursor.close() 
    connection.commit()
    connection.close()

def odevzdej_ukol(file, typ, id_ukol, id_mistnost, id_student):
    connection, cursor = otevri_spojeni()
    cursor.execute("""INSERT INTO odevzdane_ukoly (file, typ, id_ukol, id_mistnost, id_student) VALUES (%s, %s, %s, %s, %s)""", (file, typ, id_ukol, id_mistnost, id_student))
    connection.commit()
    connection.close()


def check_email(email):
    connection, cursor = otevri_spojeni()
    cursor.execute(""" SELECT email FROM studenti WHERE email = %s LIMIT 1""", (email,))
    result = cursor.fetchone()
    connection.commit()
    connection.close()
    return result

def check_keys_ucitel(klic):
    connection, cursor = otevri_spojeni()
    cursor.execute(""" SELECT klic FROM ucitele WHERE klic = %s """, (klic,))
    result = cursor.fetchone()
    connection.commit()
    connection.close()
    return result

def check_keys_student(klic):
    connection, cursor = otevri_spojeni()
    cursor.execute(""" SELECT klic FROM studenti WHERE klic = %s """, (klic,))
    result = cursor.fetchone()
    connection.commit()
    connection.close()
    return result

def check_ids_skola(id):
    connection, cursor = otevri_spojeni()
    cursor.execute(""" SELECT id_skola FROM skoly WHERE id_skola = %s """, (id,))
    result = cursor.fetchone()
    connection.commit()
    connection.close()
    return result

def vypis_skoly():
    connection, cursor = otevri_spojeni()
    cursor.execute(""" SELECT * FROM skoly""")
    result = cursor.fetchall()
    connection.close()
    return result

def vypis_ucitele():
    connection, cursor = otevri_spojeni()
    cursor.execute("""SELECT * FROM ucitele""")
    result = cursor.fetchall()
    connection.close()
    return result

def vypis_studenty():
    connection, cursor = otevri_spojeni()
    cursor.execute(""" SELECT * FROM studenti""")
    result = cursor.fetchall()
    connection.close()
    return result

def zapis_metadata(id_ode_ukol, velikost):
    connection, cursor = otevri_spojeni()
    cursor.execute("""INSERT INTO metadata (id_ode_ukol, velikost) VALUES (%s, %s)""", (id_ode_ukol, velikost,))
    connection.commit()
    connection.close()

# primitivní metoda pro nalezení hashe mailu a porovnání hesla
def check_login_student(email, klic):
    connection, cursor = otevri_spojeni()
    try:
        dotaz = "SELECT * FROM studenti WHERE email = %s"
        cursor.execute(dotaz, (hashlib.sha256(email.encode('utf-8')).hexdigest(),))

        # Získání řádku
        radek = cursor.fetchone()


        if radek:   # pokud řádek není None
            if klic == radek[2]: # pokud se klic = klic
                return (True, radek[0]) # return True pro správně přihlášení a id pro pozdější vytvoření uživatele     
        return (False, None)  # Klíč nebo email není platný
    finally:
        # Uzavření připojení
        connection.close()

def check_login_teacher(klic):
    connection, cursor = otevri_spojeni()
    try:
        dotaz = "SELECT * FROM ucitele WHERE klic = %s"
        cursor.execute(dotaz, (klic,))

        # Získání řádku
        radek = cursor.fetchone()


        if radek:   # pokud řádek není None
            return (True, radek[0]) # return True pro správně přihlášení a id pro pozdější vytvoření uživatele     
        return (False, None)  # Klíč nebo email není platný
    finally:
        # Uzavření připojení
        connection.close()