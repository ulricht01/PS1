import mariadb

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
                                nazev_skola VARCHAR(45) NOT NULL
                            ) ENGINE=InnoDB;""")
            
    cursor.execute("""CREATE TABLE IF NOT EXISTS ucitele(
                                id_ucitel INT(6) NOT NULL AUTO_INCREMENT PRIMARY KEY,
                                klic VARCHAR(15) NOT NULL UNIQUE,
                                id_skola INT(6) NOT NULL,
                                CONSTRAINT `fk_ucitele_skoly`
                                    FOREIGN KEY (id_skola) REFERENCES skoly (id_skola)
                                    ON DELETE CASCADE
                                    ON UPDATE RESTRICT
                            ) ENGINE=InnoDB;""")
            
    cursor.execute("""CREATE TABLE IF NOT EXISTS studenti(
                                id_student INT(6) NOT NULL AUTO_INCREMENT PRIMARY KEY,
                                email VARCHAR(70) NOT NULL UNIQUE,
                                klic VARCHAR(15) NOT NULL,
                                id_skola INT(6) NOT NULL,
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
                                CONSTRAINT `fk_mistnosti_ucitele`
                                    FOREIGN KEY (id_ucitel) REFERENCES ucitele (id_ucitel)
                                    ON DELETE CASCADE
                                    ON UPDATE RESTRICT
                            ) ENGINE=InnoDB;""")

    cursor.execute("""CREATE TABLE IF NOT EXISTS ukoly(
                                id_ukol INT(6) NOT NULL AUTO_INCREMENT PRIMARY KEY,
                                nazev_ukol VARCHAR(25) NOT NULL,
                                popis VARCHAR(250),
                                id_mistnost INT(6) NOT NULL,
                                CONSTRAINT `fk_ukoly_mistnosti`
                                    FOREIGN KEY (id_mistnost) REFERENCES mistnosti (id_mistnost)
                                    ON DELETE CASCADE
                                    ON UPDATE RESTRICT
                            ) ENGINE=InnoDB;""")

    cursor.execute("""CREATE TABLE IF NOT EXISTS odevzdane_ukoly(
                                id_ode_ukol INT(6) NOT NULL AUTO_INCREMENT PRIMARY KEY,
                                file BLOB NOT NULL,
                                id_ukol INT(6) NOT NULL,
                                id_mistnost INT(6) NOT NULL,
                                id_student INT(6) NOT NULL,
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
    cursor.close()
    connection.close()
def pridej_skolu(nazev_skola):
    connection, cursor = otevri_spojeni()
    cursor.execute(""" INSERT INTO skoly (nazev_skola) VALUES (%s)""", (nazev_skola,))
    cursor.close()
    connection.commit()
    connection.close()

def pridej_ucitele(klic_ucitel, id_skoly):
    connection, cursor = otevri_spojeni()
    cursor.execute(""" INSERT INTO ucitele (klic, id_skola) VALUES (%s, %s)""", (klic_ucitel, id_skoly,))
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
    cursor.execute(""" INSERT INTO studenti (email, klic, id_skola) VALUES (%s, %s, %s)""", (email, klic, id_skola,))
    cursor.close() 
    connection.commit()
    connection.close()

def pridej_ukol(nazev_ukol, popis, id_mistnost):
    connection, cursor = otevri_spojeni()
    cursor.execute(""" INSERT INTO ukoly (nazev_ukol, popis, id_mistnost) VALUES (%s, %s, %s)""", (nazev_ukol, popis, id_mistnost,))
    cursor.close() 
    connection.commit()
    connection.close()

def pridej_mistnost(nazev_mistnosti, popis, id_ucitel):
    connection, cursor = otevri_spojeni()
    cursor.execute(""" INSERT INTO mistnosti (nazev_mistnosti, popis, id_ucitel) VALUES (%s, %s, %s)""", (nazev_mistnosti, popis, id_ucitel,))
    cursor.close() 
    connection.commit()
    connection.close()

def odevzdej_ukol(file, id_ukol, id_mistnost, id_student):
    connection, cursor = otevri_spojeni()
    cursor.execute(""" INSERT INTO odevzdane_ukoly (file, id_ukol, id_mistnost, id_student) VALUES (%s, %s, %s, %s)""", (file, id_ukol, id_mistnost, id_student,))
    cursor.close() 
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

def check_login_student(email, klic):
    connection, cursor = otevri_spojeni()
    try:
        # Dotaz na databázi
        dotaz = "SELECT * FROM studenti WHERE email = %s AND klic = %s"
        cursor.execute(dotaz, (email, klic))

        # Získání řádku
        radek = cursor.fetchone()

        if radek:
            return True  # Klíč a email odpovídají záznamu v databázi
        else:
            return False  # Klíč nebo email není platný
    finally:
        # Uzavření připojení
        connection.close()