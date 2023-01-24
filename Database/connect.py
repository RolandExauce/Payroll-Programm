from tkinter import *
import sqlite3
from sqlite3 import Error
from datetime import *
from main import*


#db_file = r"C:\Users\cuxxl\OneDrive\Desktop\MetiSoft_Programm_TestVersion_1\LOHNVERRECHNUNG\Database\Loko.db"

# erstellt eine Verbindung zur Datenbank her
def create_connection(db_file):
    """create a database connection to the SQLITE database
    specified by db_file
    param db_file: database file
    Returns:
        Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
    return conn

# conn ist connection bzw. in welche datenbank zugegriffen
# query ist die sql-statement
# diese Funktion führt den sql-statement zu gegebennen datenbank


def execute_query(conn, query):
    try:
        c = conn.cursor()
        c.execute(query)
    except Error as e:
        print(e)

# Methode um Daten in die Tabellen einzusetzen
# Diese Methode wird hauptsächlich für die Tabelle PERS benutzt um Datensätze einzutragen
# Natürlich kann man diese Methode für andere SQL-Statements benutzen werden.


def insert_into(conn, sql_anweisung):
    """
    Füg den Datensatz in die Tabelle ein
    """
    try:
        c = conn.cursor()
        c.execute(sql_anweisung)
        conn.commit()
        c.close
        conn.close()
    except Error as e:
        print(e)

# dynamische einsetzen von Werten in die Tabelle PERS


def sql_insert_PERS(nn, vn, bd, strasse, ort, plz, beruf):
    statement = ""
    statement = """INSERT INTO PERS
                            (PERS_Nachname,PERS_Vorname , PERS_szvn, PERS_Strasse,PERS_Ort,PERS_Plz,PERS_Beruf) 
                            VALUES 
                            ('{}','{}','{}','{}','{}','{}','{}')""".format(nn, vn, bd, strasse, ort, plz, beruf)
    return statement

# bekommt die PERS_ID von der Tabelle PERS
# Sozialversicherungsnummer wird benutzt im sql statement


def get_ID(conn, szn):
    try:
        c = conn.cursor()
        c.execute("""Select PERS_ID from PERS
                where PERS_szvn="""+szn)
        conn.commit()
        return c.fetchone()[0]
    except Error as e:
        print(e)

# Fügt es in die Tabelle PERS ein
# Die Methode get_ID wird benutzt um den Fremdschlüssel zu erzeugen, somit wird eine Relation zwischen Tabelle PERS und Tabelle LOKO hergestellt.


def insert_loko(conn, szn, brutto, netto, szv, pndl=0, fabo=0, gwk=0, frb=0, ecar=0, pndleuro=0):
    today = date.today()
    try:
        c = conn.cursor()
        c.execute("""INSERT INTO LOKO
                            (PERS_ID,LOKO_DATE,LOKO_BRUTTO,LOKO_Netto,LOKO_Penderpauschale,LOKO_Familienbonus,LOKO_Gewerkschaftbetrag,LOKO_Sozialvers,LOKO_Freibetrag,LOKO_EcardGeb,LOKO_Pendlereuro) 
                            VALUES 
                            (?,?,?,?,?,?,?,?,?,?,?)""", (get_ID(conn, szn), today, brutto, netto, pndl, fabo, gwk, szv, frb, ecar, pndleuro))
        conn.commit()
    except Error as e:
        print(e)

# gibt die letzte LOKO_ID zur passenden Sozialversicherungsnummer aus


def get_loko_ID(conn, szn):
    try:
        c = conn.cursor()
        c.execute("""Select LOKO_ID from LOKO
                where PERS_ID=(select PERS_ID from PERS where PERS_szvn="""+szn+""") order by LOKO_ID DESC LIMIT 1""")
        conn.commit()
        return c.fetchone()[0]
    except Error as e:
        print(e)

# einfügen in Tabelle Steuerdaten


def insert_steuerdaten(conn, szn, sd_pndl=0, sd_gpp=0, sd_kpp=0, sd_pdkm=0, sd_fabo=0, sd_kun=0, sd_kue=0, sd_gwk=0, sd_vllb=0, sd_nov=0):
    today = date.today()
    try:
        c = conn.cursor()
        c.execute("""INSERT INTO Steuerdaten
                            (LOKO_ID,Steuerd_Pendlerpauschale,Steuerd_Große_PP ,Steuerd_Kleines_PP ,Steuerd_Pendlerkilometer ,Steuerd_Familienbonus ,Steuerd_Kinder_unter_18 ,Steuerd_Kinder_ueber_18 ,Steuerd_Gewerkschaft ,Steuerd_Voller_Bonus,Steuerd_November  ) 
                            VALUES 
                            (?,?,?,?,?,?,?,?,?,?,?)""", (get_loko_ID(conn, szn), sd_pndl, sd_gpp, sd_kpp, sd_pdkm, sd_fabo, sd_kun, sd_kue, sd_gwk, sd_vllb, sd_nov))
        conn.commit()
    except Error as e:
        print(e)

# Fügt die Daten in Tabelle SS ein


def insert_ss(conn, szn, ss_sach=0, ss_sonder=0):
    today = date.today()
    try:
        c = conn.cursor()
        c.execute("""INSERT INTO SS
                            (LOKO_ID,SS_Sachbez,SS_Sonderz  ) 
                            VALUES 
                            (?,?,?)""", (get_loko_ID(conn, szn), ss_sach, ss_sonder))
        conn.commit()
    except Error as e:
        print(e)


database = r"C:\Users\cuxxl\OneDrive\Desktop\MetiSoft_Programm_TestVersion_1\LOHNVERRECHNUNG\Database\Loko.db"


# LOKO_szvn ist unique und wird bei der Eingabe von einem Lohnzettel verlangt
sql_create_PERS_table = """ CREATE TABLE IF NOT EXISTS PERS(
                                PERS_ID integer PRIMARY KEY AUTOINCREMENT,
                                PERS_Nachname text NOT NULL,
                                PERS_Vorname text NOT NULL,
                                PERS_szvn text NOT NULL UNIQUE,
                                PERS_Strasse text NOT NULL,
                                PERS_Ort text NOT NULL,
                                PERS_Plz text not null,
                                PERS_Beruf text NOT NULL
    );
    """
sql_create_LOKO_table = """ CREATE TABLE IF NOT EXISTS LOKO(
                                LOKO_ID integer PRIMARY KEY AUTOINCREMENT,
                                PERS_ID integer NOT NULL,
                                LOKO_DATE datetime default current_timestamp,
                                LOKO_BRUTTO real NOT NULL,
                                LOKO_Netto real NOT NULL,
                                LOKO_Penderpauschale real,
                                LOKO_Familienbonus real,
                                LOKO_Gewerkschaftbetrag real,
                                LOKO_Sozialvers real not null,
                                LOKO_Freibetrag real,
                                LOKO_EcardGeb real,
                                LOKO_Pendlereuro real,
                                FOREIGN KEY (PERS_ID) REFERENCES PERS (PERS_ID)
        
    );
    """

# integer wird als ja(1) oder nein(0) benutzt
# BOOLEAN NOT NULL CHECK (Steuerd_Pendlerpauschale IN (0, 1)) -> da wird gecheckt, ob die Eingabe 0 oder 1 ist.
# Ebenfalls wird bei den meisten ein Default wird gesetzt, wenn man vergisst etwas eingetragen.
sql_create_Steuerdaten_table2 = """CREATE TABLE IF NOT EXISTS Steuerdaten(
                                Steuer_ID integer PRIMARY KEY AUTOINCREMENT,
                                LOKO_ID integer NOT NULL,
                                Steuerd_Pendlerpauschale BOOLEAN NOT NULL CHECK (Steuerd_Pendlerpauschale IN (0, 1)) DEFAULT 0 ,
                                Steuerd_Große_PP BOOLEAN NOT NULL CHECK (Steuerd_Große_PP IN (0, 1)) DEFAULT 0,
                                Steuerd_Kleines_PP BOOLEAN NOT NULL CHECK (Steuerd_Kleines_PP IN (0, 1)) DEFAULT 0,
                                Steuerd_Pendlerkilometer real DEFAULT 0,
                                Steuerd_Familienbonus BOOLEAN NOT NULL CHECK ( Steuerd_Familienbonus IN (0, 1)) DEFAULT 0,
                                Steuerd_Kinder_unter_18 Integer DEFAULT 0,
                                Steuerd_Kinder_ueber_18 Integer DEFAULT 0,
                                Steuerd_Gewerkschaft BOOLEAN NOT NULL CHECK (Steuerd_Gewerkschaft IN (0, 1)) DEFAULT 0,
                                Steuerd_Voller_Bonus BOOLEAN NOT NULL CHECK (Steuerd_Voller_Bonus IN (0, 1)) DEFAULT 0,
                                Steuerd_November BOOLEAN NOT NULL CHECK (Steuerd_November IN (0, 1)) DEFAULT 0,
                                FOREIGN KEY (LOKO_ID) REFERENCES LOKO (LOKO_ID)
        
    );
"""

sql_create_SS_table = """ CREATE TABLE IF NOT EXISTS SS(
                                SS_ID integer PRIMARY KEY AUTOINCREMENT,
                                LOKO_ID integer NOT NULL,
                                SS_Sachbez real default 0,
                                SS_Sonderz real default 0,
                                FOREIGN KEY (LOKO_ID) REFERENCES LOKO (LOKO_ID)
    );
    """

conn = create_connection(database)
if conn is not None:
    """
    1. Schritt Tabellen erstellen
    execute_query(conn, sql_create_PERS_table)
    execute_query(conn,sql_create_LOKO_table)
    execute_query(conn,sql_create_Steuerdaten_table2)
    execute_query(conn,sql_create_SS_table)
    """
    """
    2. Schritt Personal anlegen
    insert_into(conn,sql_insert_PERS('Peter','Parker','25685','Entengasse 5','Wien','1010','Friseur'))
    insert_into(conn,sql_insert_PERS('Jerome','Boateng','21675','Mariagasse 15','Wien','1100','Logistiker'))
    insert_into(conn,sql_insert_PERS('Manuel','Feuer','23692','Josefgasse 12','Wien','1200','Farmer'))
    insert_into(conn,sql_insert_PERS('Niklas','Blume','28675','Blumengasse 13','Wien','1210','Müllmann'))
    insert_into(conn,sql_insert_PERS('Manfred','Krieger','27645','Lassergasse 55','Wien','1150','Postler'))
    insert_into(conn,sql_insert_PERS('Jeremy','Frag','87245','Lassergasse 65','Wien','1150','Tierarzt'))
    
    """
    """
    3.Schritt Lohnzettel anlegen. Die Sozialversicherungsnummer ersetzen durch die gewünschte Sozialversicherungsnummer des Mitarbeiters
    
    insert_loko(conn,'25685',3330.05,2448.94,1234.00)
    insert_steuerdaten(conn,'25685')
    insert_ss(conn,'25685')
    
    insert_loko(conn,'28675',5230.15,1348.94,1214.00)
    insert_steuerdaten(conn,'28675',1,1,0,65)
    insert_ss(conn,'28675',1622.12,1021.99)
    """

else:
    print("ERROR!cannot create the database connection.")
