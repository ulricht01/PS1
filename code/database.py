import mariadb

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

def vytvor_tabulky(cursor):   
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
                                popis VARCHAR(125) NOT NULL,
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