from typing import Literal
import tkinter as tk
from tkinter import*
import sqlite3
from sqlite3 import Error
from datetime import *
import datetime as dt
from tkinter import ttk
from tkinter import messagebox
from PIL import ImageTk, Image
from functools import partial
import time
import locale
locale.setlocale(locale.LC_ALL, 'de_DE')
import calendar


Fact = """Zugriffsdaten und Hosting
Sie können unsere Webseiten besuchen, ohne Angaben zu Ihrer Person zu machen. 
Bei jedem Aufruf einer Webseite speichert der Webserver lediglich automatisch ein sogenanntes Server-Logfile, 
das z.B. den Namen der angeforderten Datei, Ihre IP-Adresse, 
Datum und Uhrzeit des Abrufs, übertragene Datenmenge 
und den anfragenden Provider (Zugriffsdaten) enthält und den Abruf dokumentiert. 

2.Datenerhebung und -verwendung zur Vertragsabwicklung
Wir erheben personenbezogene Daten, wenn Sie uns diese im Rahmen 
Ihrer Bestellung oder bei einer Kontaktaufnahme mit uns (z.B. per Kontaktformular oder E-Mail) mitteilen. 
Pflichtfelder werden als solche gekennzeichnet, da wir in diesen Fällen die Daten zwingend zur Vertragsabwicklung, 
bzw. zur Bearbeitung Ihrer Kontaktaufnahme benötigen und Sie ohne deren Angabe die Bestellung nicht abschließen, 
bzw. die Kontaktaufnahme nicht versenden können. Welche Daten erhoben werden, 
ist aus den jeweiligen Eingabeformularen ersichtlich. Wir verwenden die von ihnen mitgeteilten Daten gemäß Art.

3.Datenweitergabe
Zur Vertragserfüllung gemäß Art. 6 Abs. 1 S. 1 lit. b DSGVO geben wir Ihre Daten an das mit der Lieferung 
beauftragte Versandunternehmen weiter, soweit dies zur Lieferung bestellter Waren erforderlich ist. 
Je nach dem, welchen Zahlungsdienstleister Sie im Bestellprozess auswählen, geben wir zur Abwicklung 
von Zahlungen die hierfür erhobenen Zahlungsdaten an das mit der Zahlung beauftragte Kreditinstitut und ggf. 
von uns beauftragte Zahlungsdienstleister weiter
        """


# Datenbankverbindung herstellen
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

# conn -> connection to database
# query -> sql-statement

# sql query to database
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

# Dynamisches einsetzen von Werten in die Tabelle PERS
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

#TODO: INSERT VALUES INTO DATABASE 
"""
    Um diese Methode insert_loko zu benutzen, sollte man diese Paramater ausfüllen

    insert_loko(conn,szn,Brutogehalt,der ausgerechnete Nettogehalt,ausgerechnete Sozialversicherung, ausgerechnete Pendlerpauschale, ausgerechnete Familienbonus,
    ausgerechnete Gewerkschaftbeitrag,Freibetrag,E-Card Gebühr,Pendlereuro)

    Pendlperpauschale(pndl),Familienbonus(fabo),Gewerkschaftsbeitrag(gwk), Freibetrag(frb), E-Card-Gebühr(ecar) und Pendlereuro(pndleuro) MÜSSEN NICHT ausgefühlt werden.
    Es wird einen DEFAULT werden für die WERTE gesetzt

    Paramter:

    conn: Connection der Database
    szn: String
    brutto: float
    netto: float
    szv: float
    pndl: float
    fabo: float
    gwk: float
    frb: float
    ecar: float
    pndleuro: float


    """

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


#TODO: Insert steuerdaten into database 
"""
    Um diese Methode insert_steuerdaten zu benutzen, sollte man diese Paramater ausfüllen

    insert_steuerdaten(conn,szn,
    gibt es eine Pendlerpauschale(0 ooder 1), 
    ist eine große PP?(0 ider 1), ist es eine kleine PP?(0 oder 1),gefahrene Kilomter, gibt es einen Familienbonus?(0 oder 1),
    wie viele kinder sind unter 18?, wie viele Kinder sind über 18?, Ist man bei der Gewerkschaft angemeldet?(0 oder 1), gibt es einen vollen Bonus?(0 oder 1), ist es Novemeber?(0 oder 1))

    0 steht für NEIN
    1 steht für JA


    Paramter:

    conn: Connection der Database
    szn: String
    sd_pndl: integer 0 oder 1
    sd_gpp: integer 0 oder 1
    sd_kpp: integer 0 oder 1
    sd_pdkm: float
    sd_fabo: integer 0 oder 1
    sd_kun: integer
    sd_kue: integer
    sd_gwk:integer 0 oder 1
    sd_vllb: integer 0 oder 1
    sd_nov: integer 0 oder 1


    """


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


#TODO: Insert into database 

"""
    Um diese Methode insert_ss zu benutzen, sollte man diese Paramater ausfüllen

     insert_ss(conn,szn,ausgerechnete Sachbezug,ausgerechnete Sonderzahlung)

    Sachbezug(ss_sach),Sonderbezug(ss_sonder), MÜSSEN NICHT ausgefühlt werden.
    Es wird einen DEFAULT werden für die WERTE gesetzt

    Paramter:

    conn: Connection der Database
    szn: String
    ss_sach: float
    ss_sonder: float
 


    """


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


# database file
# database = r"C:\Users\cuxxl\OneDrive\Desktop\MetiSoft\LOHNVERRECHNUNG\Database\Loko.db"


database = r"C:\Users\cuxxl\OneDrive\Desktop\MetiSoft\LOHNVERRECHNUNG\Database\loko_filip.db"
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
    3.Schritt  anlegen. Die Sozialversicherungsnummer ersetzen durch die gewünschte Sozialversicherungsnummer des Mitarbeiters
    
    insert_loko(conn,'25685',3330.05,2448.94,1234.00)
    insert_steuerdaten(conn,'25685')
    insert_ss(conn,'25685')
    
    insert_loko(conn,'28675',5230.15,1348.94,1214.00)
    insert_steuerdaten(conn,'28675',1,1,0,65)
    insert_ss(conn,'28675',1622.12,1021.99)
    """
else:
    print("ERROR!cannot create the database connection.")
    
    
    
    
# Class managing all the application and the menus
class Application:
    def __init__(self):
        self.window = Tk()
        self.window.config(bg='#009ee0')
        self.window_width = 620
        self.window_height = 600
        self.window.geometry("1200x700")
        self.window.resizable(width=True, height=False)

        # Create all the classes/menus
        self.main_menu = MainMenu(self)
        self.worker_menu = WorkerMenu(self)
        self.payroll_login_menu = PayrollLoginMenu(self)
        self.payroll_menu = PayrollMenu(self)
        self.lohnzettel_menu = Lohnzettel(self)
        self.show_pers = Personal(self)

        # Show the main menu
        self.main_menu.show()
        self.window.mainloop()


# welcome window class/menu
class MainMenu:
    def __init__(self, app):
        self.app = app
        self.frame = Frame(self.app.window, relief=SOLID, padx=10, pady=10)
        self.frame.place(x=440, y=50, width=app.window_width,
                         height=app.window_height)

        self.img = ImageTk.PhotoImage(Image.open("./LOHNVERRECHNUNG/tgm.jpg"))
        # reading the image
        panel = tk.Label(self.frame, image=self.img,
                         borderwidth=3, relief="groove")
        panel.place(x=10, y=10)

        self.left_frame = Frame(self.frame, bd=2, relief=SOLID, padx=10,
                                pady=10, highlightbackground='grey', highlightthickness='3')
        self.left_frame.grid(row=0, column=0, pady=1,
                             padx=300, ipadx=130, ipady=110)
        # welcome label
        wd = Label(self.frame, text="Willommen bei", font="Verdana 20 bold")
        wd.place(x=310, y=7)

        w = Label(self.frame, wd, text=" MetiSoft!",
                  font="Verdana 20 bold ").place(x=320, y=50)
        wf = Label(self.frame, wd, text=" Filip Petrovic",
                   font="Verdana 10  ").place(x=360, y=100)

        wl = Label(self.frame, wd, text=" Long Wang",
                   font="Verdana 10 ").place(x=370, y=130)

        wr = Label(self.frame, wd, text=" Roland Loulengo",
                   font="Verdana 10 ").place(x=360, y=160)

        wt = Label(self.frame, wd, text=" Tanzhu Yuseinov",
                   font="Verdana 10 ").place(x=350, y=190)

        ww = Label(self.frame,  text="Wähle deine Option aus!",
                   font="Verdana 20 bold ").place(y=300, x=100)

        # Create Worker button
        worker_btn = Button(self.frame, text="Neuen Mitarbeiter anlegen",
                            command=lambda: self.app.worker_menu.show())
        worker_btn.place(x=120, y=390, width=160, height=30)

        # Create Payroll button
        payroll_btn = Button(self.frame, text="Mit szv-nummer anmelden",
                             command=lambda: self.app.payroll_login_menu.show())
        payroll_btn.place(x=120, y=450, width=160, height=30)

        # Lohnzettel Menü
        lohnzt_btn = Button(self.frame, text="Lohnzettel anzeigen",
                            command=lambda: self.app.lohnzettel_menu.show())
        lohnzt_btn.place(x=300, y=390, width=160, height=30)

        personal_btn = Button(self.frame, text="Alle Mitarbeiter anzeigen",
                              command=lambda: self.app.show_pers.show())
        personal_btn.place(x=300, y=450, width=160, height=30)

        # Beenden button
        quit_button = tk.Button(self.frame, command=quit,
                                height=2, width=10, text="Programm beenden")
        quit_button.place(x=220, y=500, width=160, height=30)

    def show(self):
        self.frame.tkraise()
        


# register a new worker
class WorkerMenu:
    def __init__(self, app):
        self.app = app
        self.frame = Frame(self.app.window, bd=2,
                           relief=SOLID, padx=10, pady=70)
        self.frame2 = Frame(self.app.window)
        self.frame.place(x=440, y=50, width=app.window_width,
                         height=app.window_height)

        # datenschutz label und textbox mit scrollbar
        dataProtect = Label(self.frame, text="Datenschutzerklärung ",
                            font="Verdana 15 bold ").place(x=5, y=-50)
        textBox_datenschutz = Text(self.frame, width=60, height=8, bg="white", highlightthickness=1, foreground="black",
                                   insertbackground="black", wrap="word")
        textScrollbar = Scrollbar(self.frame, orient=VERTICAL,)
        textScrollbar.config(command=textBox_datenschutz.yview)
        textBox_datenschutz["yscrollcommand"] = textScrollbar.set

        textBox_datenschutz.grid(column=1, row=4, columnspan=2)
        textScrollbar.grid(column=2, row=4, sticky="nse")
        textBox_datenschutz.insert(tk.END, Fact)

        # PERS_DATA = StringVar()
        # PERS_DATA.set(PERS[j])
        # e = Entry(self.frame, textvariable=PERS_DATA,  width=13, fg='black',borderwidth=2,relief='ridge', state=DISABLED)
        # e.grid(row=i, column=j)

        # datenschutz yes or no
        self.agreenmentButton = IntVar()
        agreeButton = Radiobutton(self.frame, text=" Ich habe die datenschutzerklärung \ngelesen und akzeptiert",
                                  value=1, variable=self.agreenmentButton, command=self.agreeMethod).place(x=20, y=150)
        disagreeButton = Radiobutton(self.frame, text="nicht akzeptieren",
                                     value=2, variable=self.agreenmentButton, command=self.agreeMethod).place(x=305, y=150)

        formular = Label(self.frame, text="Bitte geben Sie ihre Daten ein ",
                         font="Verdana 15 bold ").place(x=15, y=240)

        # Damit manche Felder nur Zahlen eingegeben werden kann, error checking wird erleichert
        def onlyNumbers(text):
            return text.isdigit()
        validationForNumbers = self.frame.register(onlyNumbers)

        # Damit manche Felder nur string eingegeben werden kann, error checking wird erleichert
        def only_strings(text):
            return text.isalpha()
        validation = self.frame.register(only_strings)

        # Firstname Field
        nb_nachname_label = Label(self.frame, text="Nachname")
        nb_nachname_label.place(x=5, y=300, width=70, height=20)
        self.nb_nachname_input = Entry(
            self.frame, validate="key", validatecommand=(validation, '%S'))
        self.nb_nachname_input.place(x=100, y=300, width=100)

        # Surname Field
        nb_vorname_label = Label(self.frame, text="Vorname")
        nb_vorname_label.place(x=240, y=300, width=70, height=20)
        self.nb_vorname_input = Entry(
            self.frame, validate="key", validatecommand=(validation, '%S'))
        self.nb_vorname_input.place(x=320, y=300, width=100)

        #  Adress Field
        nb_adresse_label = Label(self.frame, text="Adresse")
        nb_adresse_label.place(x=5, y=330, width=70, height=20)
        self.nb_adresse_input = Entry(
            self.frame, validate="key", validatecommand=(validation, '%S'))
        self.nb_adresse_input.place(x=100, y=330, width=100)

        # H/S/T Field
        nb_hst_label = tk.Label(self.frame, text="H/St/T")
        nb_hst_label.place(x=240, y=330, width=100, height=20)
        self.nb_hst_input = tk.Entry(self.frame)
        self.nb_hst_input.place(x=320, y=330, width=100)

        # Postleitzahl Field
        nb_plz_label = tk.Label(self.frame, text="Postleitzahl")
        nb_plz_label.place(x=5, y=360, width=85, height=20)
        self.nb_plz_input = tk.Entry(
            self.frame, validate="key", validatecommand=(validationForNumbers, '%S'))
        self.nb_plz_input.place(x=100, y=360, width=100)

        # location Field
        nb_ort_label = tk.Label(self.frame, text="Ort")
        nb_ort_label.place(x=260, y=360, width=70, height=20)
        self.nb_ort_input = tk.Entry(
            self.frame, validate="key", validatecommand=(validation, '%S'))
        self.nb_ort_input.place(x=320, y=360, width=100)

        # Beruf Field
        nb_beruf_label = tk.Label(self.frame, text="Beruf")
        nb_beruf_label.place(x=5, y=390, width=70, height=20)
        self.nb_beruf_input = tk.Entry(
            self.frame, validate="key", validatecommand=(validation, '%S'))
        self.nb_beruf_input.place(x=100, y=390, width=100)

        # Svz Field
        self.szvEintrag = StringVar()
        nb_svz_label = tk.Label(self.frame, text="Svz")
        nb_svz_label.place(x=260, y=390, width=70, height=20)
        #self.nb_szvn_input = tk.Entry(self.frame,validate="key", validatecommand=(validation, '%S'))
        self.nb_szvn_input = tk.Entry(self.frame, textvariable=self.szvEintrag)
        self.nb_szvn_input.place(x=320, y=390, width=100)

        # mitarbeiter anlegen
        create_worker_button = tk.Button(
            self.frame, command=self.create_worker, height=2, width=10, text="Mitarbeiter anlegen")
        create_worker_button.place(x=90, y=440, width=120, height=30)

        # Menu button
        menu_button = tk.Button(
            self.frame, command=self.back_to_menu, height=2, width=10, text="Startbildschirm")
        menu_button.place(x=330, y=440, width=90, height=30)

        # Szv auf 10 Stellen begrenzen

        def limit_entry(str_var):
            def callback(str_var):
                c = str_var.get()[0:10]
                str_var.set(c)
            str_var.trace("w", lambda name, index, mode,
                          str_var=str_var: callback(str_var))
        limit_entry(self.szvEintrag)

    # Funktion to check if Datenschutzerklärung akzeptiert wurde

    def agreeMethod(self):
        agreeOrNot = self.agreenmentButton.get()
        agreed = bool()
        if(agreeOrNot == 1):
            agreed = True
        elif(agreeOrNot == 2):
            agreed = False
        return agreed

    # function to check if there is szvn duplicate, if there isn't
    # check if values are in correct format and strings or ints are passed,

    def create_worker(self):
        conn = create_connection(database)
        data = None
        agreed = self.agreeMethod()
        # data=None
        try:
            # alle felder müssen gefüllt sein, auf bool speichern entweder leer == True oder nicht leer == False
            vornameVorhanden = self.nb_vorname_input.get() == ""
            nachnameVorhanden = self.nb_nachname_input.get() == ""
            adresseVorhanden = self.nb_adresse_input.get() == ""
            hstVorhanden = self.nb_hst_input.get() == ""
            plzVorhanden = self.nb_plz_input.get() == ""
            ortVorhanden = self.nb_ort_input.get() == ""
            berufVorhanden = self.nb_beruf_input.get() == ""
            szvnVorhanden = self.nb_szvn_input.get() == ""

            # überprüfen ob die sozialversicherungsnummer bereits vorhanden ist oder nicht,
            # duplikate mit dem selben namen, vornamen, beruf, etc... werden ignored, else: too much code
            cur = conn.cursor()
            szvn = self.nb_szvn_input.get()
            cur.execute(
                "select PERS_szvn from PERS where PERS_szvn=?", (szvn,))
            data = cur.fetchall()

            # wenn felder leer sind, warning
            if vornameVorhanden or nachnameVorhanden or adresseVorhanden or hstVorhanden or plzVorhanden or ortVorhanden or berufVorhanden or szvnVorhanden:
                messagebox.showwarning(
                    title="Incomplete Data", message="Bitte alle Felder ausfüllen!")

            # wenn szvn schon vorhanden dann warning
            elif conn is not None and data:
                messagebox.showerror(
                    title="Duplikat!", message="Diese SZV-Nummer existiert bereits \nbitte geben Sie eine andere SZV-Nummer!")

            elif not agreed:
                messagebox.showinfo(title="Datenschutz akzeptieren",
                                    message="Sie müssen die \nDatenschutzerklärungen akzeptieren!")

            # wenn szvn ist noch nicht vorhanden, datenschutz akzeptiert, felder nicht leer dann hinzufügen
            elif agreed and conn is not None and not data and not vornameVorhanden or not nachnameVorhanden or not adresseVorhanden or not hstVorhanden or not plzVorhanden or not ortVorhanden or not berufVorhanden or not szvnVorhanden:
                insert_into(conn, sql_insert_PERS(str(self.nb_nachname_input.get()), str(self.nb_vorname_input.get()), str(self.nb_szvn_input.get()), str(
                    self.nb_adresse_input.get())+' '+str(self.nb_hst_input.get()), str(self.nb_plz_input.get()), str(self.nb_ort_input.get()), str(self.nb_beruf_input.get())))

                self.back_to_menu()
                messagebox.showinfo(
                    title="Successfull!", message="Mitarbeiter wurde \nerfolgreich angelegt!")
        except Error as e:
            print(e)

    # Go back to menu
    def back_to_menu(self):
        self.app.main_menu.show()
        self.clear_inputs()

    # Clear field inputs

    def clear_inputs(self):
        self.nb_nachname_input.delete(0, "end")
        self.nb_vorname_input.delete(0, "end")
        self.nb_adresse_input.delete(0, "end")
        self.nb_hst_input.delete(0, "end")
        self.nb_plz_input.delete(0, "end")
        self.nb_ort_input.delete(0, "end")
        self.nb_beruf_input.delete(0, "end")
        self.nb_szvn_input.delete(0, "end")
    def show(self):
        self.frame.tkraise()
        


# Class/Menu to login if you are successfully registered you can create a new payroll erstellen
class PayrollLoginMenu:

    def __init__(self, app):
        self.app = app
        window = app.window
        self.frame = Frame(self.app.window, bd=2,
                           relief=SOLID, padx=10, pady=10)
        self.frame.place(x=440, y=50, width=app.window_width,
                         height=app.window_height,)
        
        q = Label(self.frame, text="Mit Sozialversicherungsnummer anmelden",
                  font="Verdana 15 bold ").pack()

        # Vorname Label und Nachname Label werden mit isalpha() methode von Python so eingestellt dass nur str akzeptiert wird
        # weil mit isInstance validiert er zwar ob input ein str ist aber selbst wenn man eine zahl eingeben würde dann würde er das
        # akzeptieren weil alles STANDDARDMÄßIG EIN STRING  ist in python
        validation = self.frame.register(self.onlyAlpha)

        # vorname
        self.vorname = StringVar()
        nb_vorname_label = Label(self.frame, text="Vorname")
        nb_vorname_label.place(x=180, y=150, width=70, height=20)
        nb_vorname_label.place(x=180, y=150, width=70, height=20)
        self.nb_vorname_input = Entry(
            self.frame, textvariable=self.vorname, validate="key", validatecommand=(validation, '%S'))

        self.nb_vorname_input.place(x=260, y=150, width=85)

        # nachname
        self.nachname = StringVar()
        nb_nachname_label = Label(self.frame, text="Nachname")
        nb_nachname_label.place(x=180, y=180, width=70, height=20)
        self.nb_nachname_input = Entry(
            self.frame, textvariable=self.nachname, validate="key", validatecommand=(validation, '%S'))
        self.nb_nachname_input.place(x=260, y=180, width=85)

        # Svz Field und Entry
        self.szvEintrag = StringVar()
        nb_svz_label = tk.Label(self.frame, text="Svz")
        nb_svz_label.place(x=180, y=210, width=70, height=20)
        self.nb_szvn_input = tk.Entry(self.frame, textvariable=self.szvEintrag)
        self.nb_szvn_input.place(x=260, y=210, width=85)

        # Payroll start button
        payroll_start_button = tk.Button(
            self.frame, command=self.payroll_start, height=2, width=10, text="Lohnabrechnung erstellen")
        payroll_start_button.place(x=370, y=150, width=160, height=30)

        # Menu button
        menu_button = tk.Button(
            self.frame, command=self.back_to_menu, height=2, width=10, text="Menu")
        menu_button.place(x=370, y=200, width=160, height=30)


#Funktionen für diese Klasse beginnen hier beginnen hier#####################################################################################################################################################################################

        # Szv auf 10 Stellen begrenzen
        def limit_entry(str_var):
            def callback(str_var):
                c = str_var.get()[0:10]
                str_var.set(c)
            str_var.trace("w", lambda name, index, mode,
                            str_var=str_var: callback(str_var))
        limit_entry(self.szvEintrag)

    # mit dieser Methode werden nur strings akzepiert, wir legne Vor und Nachname als String fest
    def onlyAlpha(self, char):
        return char.isalpha()
    
    
    # def combineFunc(self, *funcs):
    #     # print(funcs) 
    #     def combinedFunc(*args, **kwargs):
    #         for f in funcs:
    #             f(*args, **kwargs)
    #             #print(f(*args, **kwargs))
    #     return combinedFunc

    # to start a payroll first we check if the worker exists in the database
    # by searching for the inputed data
    def payroll_start(self):
        conn= sqlite3.Connection
        data: list = []
        try:
            if self.nb_nachname_input.get() == "" or self.nb_vorname_input.get() == "" or self.nb_szvn_input.get() == "":
                messagebox.showwarning(
                    title="Daten fehlen", message="Bitte gib deine Login Daten um \ndeine Lohnabrechnung zu erstellen")

            else:
                szvn = str(self.szvEintrag.get())
                nachname = self.nachname.get()
                vorname = self.vorname.get()
                conn = create_connection(database)
                cur = conn.cursor()
                cur.execute(
                    "select PERS_ID, PERS_szvn, PERS_vorname, PERS_nachname from PERS where PERS_szvn=? AND PERS_Nachname=? AND PERS_Vorname=?", (szvn, nachname, vorname))
                data = cur.fetchall()
                #print(data)
                conn.commit()
                
                # Falls die eingegebenen Daten nicht stimmen, wobei hier wird nicht geachtet was genau falsch ist, die Implementierung war schwierig
                if not data:
                    messagebox.showerror(
                        title="Ungültige Daten", message="Mitarbeiter nicht vorhanden,\nbitte versuchen Sie erneut!")

                else:
                    self.app.payroll_menu.show()
                    self.clear_inputs()
                    messagebox.showinfo(
                        title="Logged in", message="Mitarbeiter erfolgreich eingeloggt!")
                    
        # Falls ein Value Error vorhanden ist, also die SZV wird nicht als int eingegeben
        except ValueError:
            messagebox.showerror(title="Üngültiger Datentyp",
                                        message="Sozialverischerungsfeld darf nicht leer ein und muss ein Integer sein!")
            
        
    def show(self):
        self.frame.tkraise()
    # Go back to menu
    def back_to_menu(self):
        self.app.main_menu.show()
        self.clear_inputs()

    # Reset every field
    def clear_inputs(self):
        self.nb_nachname_input.delete(0, "end")
        self.nb_vorname_input.delete(0, "end")
        self.nb_szvn_input.delete(0, "end")

    def show(self):
        self.frame.tkraise()

#klasse lohnzettel
class Lohnzettel:
    def __init__(self, app):
        self.app = app
        window = app.window
        self.frame = Frame(self.app.window, bd=2,
                            relief=SOLID, padx=10, pady=10)
        self.frame.place(x=440, y=50, width=app.window_width,
                            height=app.window_height)
        d = Label(self.frame, text="Bitte geben Sie eine Sozialversicherungsnummer ein.",
                    font="Verdana 10 bold ")
        #lookup_label=Label(self.frame,text="")
        
        #  Sozialversicherungsnummer
        szvn_label = Label(self.frame, text="Sozialversicherungsnummer:")
        szvn_label.place(x=70, y=350, width=300, height=20)
        self.szvn_input = Entry(self.frame)
        self.szvn_input.place(x=300, y=350, width=200)
        
        #Lohnzettel anzeigen
        show_lohnzettel_button = tk.Button(self.frame, command=self.show_lohnzettel, height=2, width=10, text="Lohnzettel anzeigen")
        show_lohnzettel_button.place(x=90, y=440, width=120, height=30)
        
        menu_button = tk.Button(
            self.frame, command=self.goBackandClear, height=2, width=10, text="Startbildschirm")
        menu_button.place(x=300, y=440, width=90, height=30)
    
    
    #Methode vom Herrn Professor Ratschiner.
    def change_tuple_list(self,arg):
        temp_li = []        # new temp. list object
        for tup in arg:     # loop list of tuples
            li = list(tup)  # tuple to list
            new_li = [i if isinstance(i,float) else 'ja' if i == 1 else 'nein' if i == 0 else i for i in li]  # list comprehension:i if ob es ein float ist, ja if 1, nein if 0, else do nothing
            temp_li.append(tuple(new_li))   # append tuple (of new_list) to temp_list
        return temp_li      # return list of tuples
    
    def goBackandClear(self, event=None): 
        self.back_to_menu()
        self.lookup_label.config(text = "")
        self.lookup_label1.config(text = "")
        
    def show_lohnzettel(self):
        szvn = self.szvn_input.get()

        conn= create_connection(database)
        c = conn.cursor()
    
        #if conn is not None:
            #try:
        c.execute("""SELECT LOKO_DATE,LOKO_BRUTTO,LOKO_Netto,LOKO_Penderpauschale,LOKO_Familienbonus,LOKO_Sozialvers,LOKO_Freibetrag,LOKO_EcardGeb,LOKO_Pendlereuro, Steuerd_Pendlerpauschale,Steuerd_Große_PP,Steuerd_Kleines_PP,Steuerd_Pendlerkilometer,Steuerd_Familienbonus,Steuerd_Kinder_unter_18,Steuerd_Kinder_ueber_18,Steuerd_Gewerkschaft,Steuerd_Voller_Bonus,Steuerd_November, SS_Sachbez,SS_Sonderz
                        from LOKO
                        JOIN Steuerdaten on LOKO.LOKO_ID=Steuerdaten.LOKO_ID
                        JOIN SS on Loko.LOKO_ID=SS.LOKO_ID
                        WHERE LOKO.PERS_ID=(SELECT PERS.PERS_ID from PERS WHERE PERS.PERS_szvn="""+szvn+")")
        result=c.fetchall()
        final_result=self.change_tuple_list(result)

        e=Label(self.frame,width=9,text='Erstelldatum',borderwidth=2, relief='ridge',anchor='w',bg='#00FF00')
        e.grid(row=0,column=0)
        e=Label(self.frame,width=9,text='Bruttogehalt',borderwidth=2, relief='ridge',anchor='w',bg='#00FF00')
        e.grid(row=0,column=1)
        e=Label(self.frame,width=9,text='Nettogehalt',borderwidth=2, relief='ridge',anchor='w',bg='#00FF00')
        e.grid(row=0,column=2)
        e=Label(self.frame,width=9,text='Pendlerpauschale',borderwidth=2, relief='ridge',anchor='w',bg='#00FF00')
        e.grid(row=0,column=3)
        e=Label(self.frame,width=9,text='Familienbonus',borderwidth=2, relief='ridge',anchor='w',bg='#00FF00')
        e.grid(row=0,column=4)
        e=Label(self.frame,width=9,text='Sozialversicherung',borderwidth=2, relief='ridge',anchor='w',bg='#00FF00')
        e.grid(row=0,column=5)
        e=Label(self.frame,width=9,text='Freibetrag',borderwidth=2, relief='ridge',anchor='w',bg='#00FF00')
        e.grid(row=0,column=6)
        e=Label(self.frame,width=9,text='E-Card Gebühr',borderwidth=2, relief='ridge',anchor='w',bg='#00FF00')
        e.grid(row=0,column=7)
        e=Label(self.frame,width=9,text='Pendlereuro',borderwidth=2, relief='ridge',anchor='w',bg='#00FF00')
        e.grid(row=0,column=8)  
        i=1   
        
        #FIXME: 
        for LOKO in final_result:
            for j in range(len(LOKO)):
                data = LOKO[j]
                data = StringVar()
                data.set(LOKO[j])
                
                e = Entry(self.frame, text=data, width=9, state=DISABLED)
                e.grid(row=i,column=j)
                #e.insert(END, LOKO[j])
            i=i+1
            print()
            
            

    def show(self):
        pass
        self.frame.tkraise()
        
    def clear_inputs(self):
        self.szvn_input.delete(0, "end")

    def back_to_menu(self):
        self.app.main_menu.show()
        self.clear_inputs()
    def show(self):
        pass
        self.frame.tkraise()


#TODO: 
# Um die Mitarbeiter anzuzeigen
class Personal:
    def __init__(self, app):
        self.app = app
        window = app.window
        self.frame = Frame(self.app.window, bd=2,
                           relief=SOLID, padx=10, pady=10)
        self.frame.place(x=440, y=50, width=app.window_width,
                         height=app.window_height)
        d = Label(self.frame, text="Alle Personen",
                  font="Verdana 28 bold ")

        conn = create_connection(database)
        c = conn.cursor()
        c.execute(
            "Select PERS_Nachname, PERS_Vorname, PERS_szvn, PERS_Strasse,PERS_Ort, PERS_Plz,PERS_Beruf from PERS")
        e = Label(self.frame, width=11, text='Name', borderwidth=2,
                  relief='ridge', anchor='w', bg='#00FF00')
        e.grid(row=0, column=0)
        e = Label(self.frame, width=11, text='Nachname',
                  borderwidth=2, relief='ridge', anchor='w', bg='#00FF00')
        e.grid(row=0, column=1)
        e = Label(self.frame, width=11, text='mark', borderwidth=2,
                  relief='ridge', anchor='w', bg='#00FF00')
        e.grid(row=0, column=2)
        e = Label(self.frame, width=11, text='Adresse', borderwidth=2,
                  relief='ridge', anchor='w', bg='#00FF00')
        e.grid(row=0, column=3)
        e = Label(self.frame, width=11, text='Ort', borderwidth=2,
                  relief='ridge', anchor='w', bg='#00FF00')
        e.grid(row=0, column=4)
        e = Label(self.frame, width=11, text='Bezirk', borderwidth=2,
                  relief='ridge', anchor='w', bg='#00FF00')
        e.grid(row=0, column=5)
        e = Label(self.frame, width=11, text='Beruf', borderwidth=2,
                  relief='ridge', anchor='w', bg='#00FF00')
        e.grid(row=0, column=6)
        i = 1

        try:
            for PERS in c:
                for j in range(len(PERS)):

                    PERS_DATA = StringVar()
                    PERS_DATA.set(PERS[j])
                    e = Entry(self.frame, textvariable=PERS_DATA, width=13,
                              fg='black', borderwidth=2, relief='ridge', state=DISABLED)
                    e.grid(row=i, column=j)

                i = i+1
                # print()

                #result=c.fetchall()#
                #for x in result:#
                # lookup_label=Label(self.frame,text=x)
                #lookup_label.pack()#
        except Error as e:
            print(e)

        # else:
            #print("ERROR!cannot create the database connection.")

        menu_button = tk.Button(
            self.frame, command=self.back_to_menu, height=2, width=10, text="Startbildschirm")
        menu_button.place(x=30, y=530, width=90, height=30)

    def show(self):
        pass
        self.frame.tkraise()

    def back_to_menu(self):
        self.app.main_menu.show()

    def show(self):
        pass
        self.frame.tkraise()
  
#TODO: 
        
        
#class payroll to calculate the net pay
class PayrollMenu():
    def __init__(self, app):
        self.app = app
        window = app.window
        self.frame = Frame(self.app.window, bd=2,
                            relief=SOLID, padx=10, pady=10)
        self.frame.place(x=440, y=50, width=app.window_width,
                            height=app.window_height)

        #because some widgets are hidden we need to initialize them as empty ones so that
        #they are recognized as part of the PayrollMenu, because some labels are hidden when you start the payroll interface
        self.stundenlohn = StringVar(value=0)
        self.nb_sb_label = tk.Label()
        self.stdl_input = tk.Entry()
        self.euroSTD = tk.Label()
        self.Oderlabel = tk.Label()
        self.ueT = StringVar(value=0)
        self.nb_ueberstundenTeiler_label = tk.Label()
        self.ueberstundenTeiler_input = tk.Entry()
        self.ueberstunden_100_Prozent = StringVar(value=0)
        self.nb_us100_label = tk.Label()
        self.nb_us100_input = tk.Entry()
        self.ue100hours = tk.Label()
        self.ueberstunden_50_Prozent = StringVar(value=0)
        self.nb_us50_label = tk.Label()
        self.ue50hours = tk.Label()
        self.nb_us50_input = tk.Entry()
        self.selectedPauschale = StringVar(value=0)
        self.keyvalue_pendler = tuple [Literal, Literal]
        self.pendlerComboBox = ttk.Combobox()
        self.km = StringVar(value=0)
        self.nb_km_label = tk.Label()
        self.maxKm = tk.Label()
        self.nb_km_input = tk.Entry()
        self.selectedBonus = StringVar(value=0)
        self.keyvalue_FB = tuple [Literal, Literal]
        self.familienBonusComboBox = ttk.Combobox()
        self.urlaubsbeihilfeLabel = tk.Label()
        self.urlaubsbeihilfe = StringVar(value=0)
        self.nb_urlaubsbeihilfe_input = tk.Entry()
        self.euroUB = tk.Label()
        self.sonstSZLabel = tk.Label()
        self.sonstigeSonderzahlung = StringVar(value=0)
        self.sonstigeSonderzahlung_input = tk.Entry()
        self.euroSZ = tk.Label()
        self.kinderAnzahlLabel = Label()
        self.kinderAnzahlgesamt = IntVar(value=0)
        self.kinderAnzahlEntry = tk.Entry()
        self.kinderOver18Label = Label()
        self.kind_0_over18 = Button()
        self.kind_1_over18 = Button()
        self.kind_2_over18 = Button()
        self.kind_3_over18 = Button()
        self.kind_4_over18 = Button()
        self.kind_5_over18 = Button()
        self.kinderUnder18Label = Label()
        self.kind_0_under18 = Button()
        self.kind_1_under18 = Button()
        self.kind_2_under18 = Button()
        self.kind_3_under18 = Button()
        self.kind_4_under18 = Button()
        self.kind_5_under18 = Button()
########## GUI FELDER #########################################################################################
        # urlaub bereits bezogen label
        self.urlaubBezogenLabel = Label(
            self.frame, text="Urlaub schon bezogen?", font="Verdana 10 bold ")
        self.urlaubBezogenLabel.place(x=30, y=190, width=180, height=80)
        
        # Sonderzahlung vorhanden label
        self.sonderZahlungLabel = Label(
            self.frame, text="Sonderzahlungen vorhanden?", font="Verdana 10 bold ")
        self.sonderZahlungLabel.place(x=30, y=268, width=220, height=80)

        # label für Ueberstunden
        self.UeberstundenLabel = Label(
            self.frame, text="Überstunden vorhanden?", font="Verdana 10 bold ")
        self.UeberstundenLabel.place(x=30, y=-10, width=190, height=80)

        # label für pendlerpauschale
        self.pendlerLabel = Label(
            self.frame, text="Pendlerpauschale", font="Verdana 10 bold ")
        self.pendlerLabel.place(x=260, y=-10, width=140, height=80)

        # AVAB/AEAB Label
        self.avab_aeabLabel = Label(
            self.frame, text="AVAB/AEAB", font="Verdana 10 bold ")
        self.avab_aeabLabel.place(x=455, y=230, width=100, height=80)
        
        # FB Label
        self.familienBonusLabel = Label(
            self.frame, text="Familienbonus", font="Verdana 10 bold ")
        self.familienBonusLabel.place(x=435, y=-10, width=110, height=80)

        # Gewerkschaftsbeitrag label, entry und euro label
        self.gwBeitrag = StringVar()
        nb_gwBeitrag_label = tk.Label(
            self.frame, text="Gewerkschaftsbeitrag", font="Arial 10 bold")
        nb_gwBeitrag_label.place(x=260, y=200, width=150, height=20)
        euroGW = tk.Label(self.frame, text="€", font="Arial 12 bold")
        euroGW.place(x=350, y=231, width=15, height=15)
        self.nb_gwBeitrag_label_input = tk.Entry(
            self.frame, textvariable=self.gwBeitrag)
        self.nb_gwBeitrag_label_input.place(x=280, y=230, width=60)
        self.nb_gwBeitrag_label_input.insert(END, float(0))
        
        # Freibetrag Label, entry und euro label
        self.freibetrag = StringVar()
        nb_fb_label = tk.Label(
            self.frame, text="Freibetrag", font="Arial 10 bold")
        nb_fb_label.place(x=260, y=270, width=100, height=20)
        euroFB = tk.Label(self.frame, text="€", font="Arial 12 bold")
        euroFB.place(x=350, y=302, width=15, height=15)
        self.nb_fb_input = tk.Entry(self.frame, textvariable=self.freibetrag)
        self.nb_fb_input.place(x=280, y=300, width=60)
        self.nb_fb_input.insert(END, float(0))

        # Reisekosten Label, entry und euro label
        self.reisekosten = StringVar()
        reisekostenlabel = tk.Label(
            self.frame, text="Reisekosten", font="Arial 10 bold")
        reisekostenlabel.place(x=260, y=340, width=100, height=20)
        euroRK = tk.Label(self.frame, text="€", font="Arial 12 bold")
        euroRK.place(x=350, y=371, width=15, height=15)
        self.reisekostenInput = tk.Entry(
            self.frame, textvariable=self.reisekosten)
        self.reisekostenInput.place(x=280, y=370, width=60)
        self.reisekostenInput.insert(END, float(0))

        # Sachbezug label, entry, euro label
        self.sachbezug = StringVar()
        nb_sb_label = tk.Label(
            self.frame, text="Sachbezugswert", font="Arial 10 bold")
        nb_sb_label.place(x=30, y=430, width=130, height=20)
        self.nb_sb_input = tk.Entry(self.frame, textvariable=self.sachbezug)
        self.nb_sb_input.place(x=50, y=460, width=60)
        self.nb_sb_input.insert(END, float(0))
        euroSB = tk.Label(self.frame, text="€", font="Arial 14 bold")
        euroSB.place(x=120, y=462, width=15, height=15)
        
        # Brutto label
        self.bruttoLohn = StringVar()
        nb_brutto_label = tk.Label(self.frame, text="Bruttogehalt", font="Arial 15 bold")
        nb_brutto_label.place(x=240, y=430, width=150, height=25)
        self.nb_brutto_input = tk.Entry(
            self.frame, textvariable=self.bruttoLohn)
        self.nb_brutto_input.insert(END, float(0))
        self.nb_brutto_input.place(x=260, y=470, width=80, height = 25)
        euroBL = tk.Label(self.frame, text="€", font="Arial 18 bold")
        euroBL.place(x=348, y=472, width=18, height=18)

        #Monat auswählen Label
        monatLabel = tk.Label(self.frame, text="Monat auswählen!", font="Arial 11 bold")
        monatLabel.place(x=440, y=430, width=140, height=25)
        
        #Jahr Label
        year_now = str(dt.date.today().year)
        # Jahr label plus option Menu
        nb_year_label = tk.Label(self.frame, text=year_now, font="Arial 11 bold")
        nb_year_label.place(x=520, y=465, width=40, height=20)
        
        #current month
        today = date.today()
        self.month = today.strftime("%B")
        # create a combobox for month
        self.selected_month = tk.StringVar(value=self.month)
        self.month_cb = ttk.Combobox(
            self.frame, width=6, textvariable=self.selected_month)

        # get first 3 letters of every month name
        self.month_cb['values'] = [calendar.month_name[m][0:3] for m in range(1, 13)]
        # prevent typing a value
        self.month_cb['state'] = 'readonly'
        self.month_cb.place(x=450, y=465)
        self.month_cb.bind('<<ComboboxSelected>>',
                            self.combineFunc)

        # hat avab/aeab ja oder nein 
        self.hatKinderOderNicht = IntVar(value=1)
        avab_aeabJa = Radiobutton(
            self.frame, text="ja", variable=self.hatKinderOderNicht, value=0, command=lambda: [self.showKinder_avab(), self.combineFunc()])
        avab_aeabJa.place(x=525, y=285)
        avab_aeabNein = Radiobutton(
            self.frame, text="nein", variable=self.hatKinderOderNicht, value=1, command=lambda: [self.showKinder_avab(), self.combineFunc()])
        avab_aeabNein.place(x=455, y=285)
        

        # überstunden vorhanden oder nicht
        self.ueberstunden_JaNein = IntVar(value=1)
        ueberstundenJa = Radiobutton(self.frame, text="ja", variable=self.ueberstunden_JaNein, value=0, command=lambda: [
                                        self.showUeberStundenLabels(), self.combineFunc()])
        ueberstundenJa.place(x=115, y=51)
        ueberstundenNein = Radiobutton(self.frame, text="nein", variable=self.ueberstunden_JaNein, value=1, command=lambda: [
                                        self.showUeberStundenLabels(), self.combineFunc()])
        ueberstundenNein.place(x=50, y=50)
        
        # pendl. ja oder nein
        self.pendler_JaNein = IntVar(value=1)
        pendlerJa = Radiobutton(self.frame, text="ja", variable=self.pendler_JaNein,
                                value=0, command=lambda: [self.showComboPS(), self.combineFunc()])
        pendlerJa.place(x=335, y=51)
        pendlerNein = Radiobutton(self.frame, text="nein", variable=self.pendler_JaNein,
                                    value=1, command=lambda: [self.showComboPS(), self.combineFunc()])
        pendlerNein.place(x=270, y=50)

        # bezieht Familienbonus oder nicht
        self.beziehtFB = IntVar(value=1)
        bonusJa = Radiobutton(self.frame, text="ja", variable=self.beziehtFB,
                                value=0,  command=lambda: [self.showComboFB(), self.combineFunc()])
        bonusJa.place(x=505, y=50)
        bonusNein = Radiobutton(self.frame, text="nein", variable=self.beziehtFB, value=1, command=lambda: [
                                self.showComboFB(), self.combineFunc()])
        bonusNein.place(x=440, y=50)

        # urlaubsbeihilfe bereits bezogen oder nicht
        self.ub_bezogenOdernicht = IntVar(value=1)
        hatteUrlaubJa = Radiobutton(
            self.frame, text="ja", variable=self.ub_bezogenOdernicht, value=0,  command=self.combineFunc)
        hatteUrlaubJa.place(x=105, y=250)
        hatteUrlaubNein = Radiobutton(
            self.frame, text="nein", variable=self.ub_bezogenOdernicht, value=1, command=self.combineFunc)
        hatteUrlaubNein.place(x=40, y=250)

        # urlaubsbeihilfe oder Sonderzahlungen vorhanden oder nicht
        self.ubVorhandenOderNicht = IntVar(value=1)
        urlaubVorhandenJa = Radiobutton(self.frame, text="ja", variable=self.ubVorhandenOderNicht, value=0, command=lambda: [
                                        self.showUrlaubLabel(), self.combineFunc()])
        urlaubVorhandenJa.place(x=105, y=330)
        urlaubVorhandenNein = Radiobutton(self.frame, text="nein", variable=self.ubVorhandenOderNicht, value=1, command=lambda: [
                                            self.showUrlaubLabel(), self.combineFunc()])
        urlaubVorhandenNein.place(x=40, y=330)

        # Start button
        start_button = tk.Button(
            self.frame, command=self.combineFunc(self.brutto_netto_berechnen, self.create_payroll),
            height=2, width=10, text="Lohn berechnen")
        start_button.place(x=50, y=540, width=160, height=30)

        # Menu button
        menu_button = tk.Button(
            self.frame, command=self.back_to_menu, height=2, width=10, text="Menu")
        menu_button.place(x=220, y=540, width=160, height=30)

        # Quit button
        quit_button = tk.Button(self.frame, command=quit,
                                height=2, width=10, text="Programm beenden")
        quit_button.place(x=390, y=540, width=160, height=30)


#GetValue Funktionen beginnen hier ################################################################################################################################################
    # will take other functions as arguments, so we can use more than one function on the button: lohn berechnen, to trigger the createpayroll function at the same time
    #other buttons are used to show labels and hide them, we need to get those values also to other functions, they are bind with combineFunc also 
    # multiple events at the same time
    def combineFunc(self, *funcs):
        # print(funcs) 
        def combinedFunc(*args, **kwargs):
            for f in funcs:
                f(*args, **kwargs)
                #print(f(*args, **kwargs))
        return combinedFunc

    #funktion um die Überstunden input felder anzeigen oder ausblenden
    def showUeberStundenLabels(self) -> None:
        try:
            if int(self.ueberstunden_JaNein.get()) == 0:
                # Stundenlohn
                self.stundenlohn = StringVar()
                self.nb_sb_label = tk.Label(
                    self.frame, text="std Lohn", font="Arial 9 bold")
                self.nb_sb_label.place(x=18, y=84, width=100, height=20)

                # stundenlohn entry
                self.stdl_input = tk.Entry(
                    self.frame, textvariable=self.stundenlohn)
                self.stdl_input.place(x=40, y=110, width=40)
                self.stdl_input.insert(END, float(0))

                # €/h Label für stundenlohn
                self.euroSTD = tk.Label(
                    self.frame, text="€/h", font="Arial 11")
                self.euroSTD.place(x=85, y=113, width=30, height=15)

                # Oder Optionstext
                self.Oderlabel = tk.Label(
                    self.frame, text="Oder", font="Arial 11 bold")
                self.Oderlabel.place(x=122, y=109, width=45, height=20)

                # Überstundenteiler lt. Kollektivvertrag
                self.ueT = StringVar()
                self.nb_ueberstundenTeiler_label = tk.Label(
                    self.frame, text="*ÜT", font="Arial 9 bold")
                self.nb_ueberstundenTeiler_label.place(
                    x=140, y=87, width=100, height=20)

                # Überstundenteilerinput
                self.ueberstundenTeiler_input = tk.Entry(
                    self.frame, textvariable=self.ueT)
                self.ueberstundenTeiler_input.place(x=180, y=110, width=40)
                self.ueberstundenTeiler_input.insert(END, float(0))

                # Überstunden mit 100% vergütung
                self.ueberstunden_100_Prozent = StringVar()
                self.nb_us100_label = tk.Label(
                    self.frame, text="Überstunden mit 100%", font="Arial 10")
                self.nb_us100_label.place(x=40, y=145, width=135, height=20)

                # entry für ue 100%
                self.nb_us100_input = tk.Entry(
                    self.frame, textvariable=self.ueberstunden_100_Prozent)
                self.nb_us100_input.place(x=180, y=145, width=25)
                self.nb_us100_input.insert(END, float(0))

                # /h Label für überstunden mit 100%
                self.ue100hours = tk.Label(
                    self.frame, text="Std", font="Arial 10")
                self.ue100hours.place(x=210, y=149, width=20, height=15)

                # Überstunden mit 50% vergütung
                self.ueberstunden_50_Prozent = StringVar()
                self.nb_us50_label = tk.Label(
                    self.frame, text="Überstunden mit 50%", font="Arial 10")
                self.nb_us50_label.place(x=37, y=180, width=135, height=20)

                # /h Label für überstunden mit 50%
                self.ue50hours = tk.Label(
                    self.frame, text="Std", font="Arial 10")
                self.ue50hours.place(x=210, y=184, width=20, height=15)

                # entry ue 50%
                self.nb_us50_input = tk.Entry(
                    self.frame, textvariable=self.ueberstunden_50_Prozent)
                self.nb_us50_input.place(x=180, y=180, width=25)
                self.nb_us50_input.insert(END, float(0))

            # Widgets erstören falls auf nein geclickt wird
            elif int(self.ueberstunden_JaNein.get()) == 1:
                self.nb_sb_label.destroy()
                self.stdl_input.destroy()
                self.euroSTD.destroy()
                self.Oderlabel.destroy()
                self.nb_ueberstundenTeiler_label.destroy()
                self.ueberstundenTeiler_input.destroy()
                self.nb_us100_label.destroy()
                self.nb_us100_input.destroy()
                self.nb_us50_label.destroy()
                self.nb_us50_input.destroy()
                self.ue100hours.destroy()
                self.ue50hours.destroy()
        except ValueError as e:
            print(e)


    #Familienbonus dynamisch anzeigen falls Sie vorhanden ist oder nicht 
    def showComboFB(self) -> None:
        try:
            if int(self.beziehtFB.get()) == 0:
                self.selectedBonus = StringVar(value="auswählen")
                self.keyvalue_FB = ("Voller Bonus", "Halber Bonus")
                self.familienBonusComboBox = ttk.Combobox(
                    self.frame, textvariable=self.selectedBonus, width=15, values=self.keyvalue_FB)
                self.familienBonusComboBox.place(relx="0.735", rely="0.145")
                self.familienBonusComboBox['state'] = 'readonly'
                self.familienBonusComboBox.bind(
                    '<<ComboboxSelected>>', self.combineFunc)
                
                # kinder über 18
                self.kinderOver18Label = Label(
                    self.frame, text="**Kinder über 18 Jahre", font="Verdana 7 bold ")
                self.kinderOver18Label.place(
                    x=435, y=118, width=120, height=20)
                
                #wir binden die buttons an 2 verschiedene Funktionen, einmal für kinder unter 18 
                # und für kinder über 18, die id wird mit übergeben
                self.kind_0_over18 = Button(
                    self.frame, text='0', bg='white',  command=partial(self.getKinderAnzahlOver18, 0))
                self.kind_0_over18.place(x=445, y=145)
                self.kind_1_over18 = Button(
                    self.frame, text='1', bg='white',  command=partial(self.getKinderAnzahlOver18, 1))
                self.kind_1_over18.place(x=465, y=145)
                self.kind_2_over18 = Button(
                    self.frame, text='2', bg='white',  command=partial(self.getKinderAnzahlOver18, 2))  
                self.kind_2_over18.place(x=485, y=145)
                self.kind_3_over18 = Button(
                    self.frame, text='3', bg='white',  command=partial(self.getKinderAnzahlOver18, 3))
                self.kind_3_over18.place(x=505, y=145)
                self.kind_4_over18 = Button(
                    self.frame, text='4', bg='white', command=partial(self.getKinderAnzahlOver18, 4))
                self.kind_4_over18.place(x=525, y=145)
                self.kind_5_over18 = Button(
                    self.frame, text='5', bg='white', command=partial(self.getKinderAnzahlOver18, 5))
                self.kind_5_over18.place(x=545, y=145)
                
                # ##########################################
                self.kinderUnder18Label = Label(
                    self.frame, text="**Kinder unter 18 Jahre", font="Verdana 7 bold ")
                self.kinderUnder18Label.place(
                    x=435, y=185, width=120, height=20)
                self.kind_0_under18 = Button(
                    self.frame, text='0', bg='white', command=partial(self.getKinderAnzahlUnder18, 0))
                self.kind_0_under18.place(x=445, y=210)
                self.kind_1_under18 = Button(
                    self.frame, text='1', bg='white', command=partial(self.getKinderAnzahlUnder18, 1))
                self.kind_1_under18.place(x=465, y=210)
                self.kind_2_under18 = Button(
                    self.frame, text='2', bg='white', command=partial(self.getKinderAnzahlUnder18, 2))
                self.kind_2_under18.place(x=485, y=210)
                self.kind_3_under18 = Button(
                    self.frame, text='3', bg='white', command=partial(self.getKinderAnzahlUnder18, 3))
                self.kind_3_under18.place(x=505, y=210)
                self.kind_4_under18 = Button(
                    self.frame, text='4', bg='white', command=partial(self.getKinderAnzahlUnder18, 4))
                self.kind_4_under18.place(x=525, y=210)
                self.kind_5_under18 = Button(
                    self.frame, text='5', bg='white', command=partial(self.getKinderAnzahlUnder18, 5))
                self.kind_5_under18.place(x=545, y=210)
                
            #labels zerstören
            elif int(self.beziehtFB.get()) == 1:
                self.kinderOver18Label.destroy()
                self.kinderUnder18Label.destroy()
                self.kind_0_over18.destroy()
                self.kind_1_over18.destroy()
                self.kind_2_over18.destroy()
                self.kind_3_over18.destroy()
                self.kind_4_over18.destroy()
                self.kind_5_over18.destroy()
                self.kind_0_under18.destroy()
                self.kind_1_under18.destroy()
                self.kind_2_under18.destroy()
                self.kind_3_under18.destroy()
                self.kind_4_under18.destroy()
                self.kind_5_under18.destroy() 
                # self.familienBonusComboBox.set('')
                self.familienBonusComboBox.destroy()
        except ValueError as e:
            print(e)
            

    #Sonderzahlung dynamisch anzeigen falls sie vorhanden sind oder nicht
    def showUrlaubLabel(self) -> None:
        try:
            if int(self.ubVorhandenOderNicht.get()) == 0:
                # urlaubsbeihilfe label
                self.urlaubsbeihilfeLabel = tk.Label(
                    self.frame, text="Urlaubsbeihilfe", font="Arial 9 bold")
                self.urlaubsbeihilfeLabel.place(
                    x=28, y=366, width=100, height=20)
                # Urlaubsbeihilfe field
                self.urlaubsbeihilfe = StringVar()
                self.nb_urlaubsbeihilfe_input = tk.Entry(
                    self.frame, textvariable=self.urlaubsbeihilfe)
                self.nb_urlaubsbeihilfe_input.place(x=45, y=390, width=60)
                self.nb_urlaubsbeihilfe_input.insert(END, float(0))
                # € Label für UB
                self.euroUB = tk.Label(
                    self.frame, text="€", font="Arial 12 bold")
                self.euroUB.place(x=110, y=391, width=15, height=15)
                # sonstige sonderzahlungen label
                self.sonstSZLabel = tk.Label(
                    self.frame, text="Sonst. SZ", font="Arial 9 bold")
                self.sonstSZLabel.place(x=135, y=366, width=100, height=20)
                # sonstige Sonderzahlungen
                self.sonstigeSonderzahlung = StringVar()
                self.sonstigeSonderzahlung_input = tk.Entry(
                    self.frame, textvariable=self.sonstigeSonderzahlung)
                self.sonstigeSonderzahlung_input.place(x=155, y=390, width=60)
                self.sonstigeSonderzahlung_input.insert(END, float(0))
                # € Label für SZ
                self.euroSZ = tk.Label(
                    self.frame, text="€", font="Arial 12 bold")
                self.euroSZ.place(x=220, y=391, width=15, height=15)
                
            elif int(self.ubVorhandenOderNicht.get()) == 1:
                self.urlaubsbeihilfeLabel.destroy()
                self.nb_urlaubsbeihilfe_input.destroy()
                self.euroUB.destroy()
                self.sonstSZLabel.destroy()
                self.sonstigeSonderzahlung_input.destroy()
                self.euroSZ.destroy()
        except ValueError as e:
            print(e)
            
            
    #PendlerCombo mit km labels anzeigen oder ausblenden 
    def showComboPS(self) -> None:
        try:
            if int(self.pendler_JaNein.get()) == 0:
                self.selectedPauschale = StringVar(value="auswählen")
                self.keyvalue_pendler = (
                    "Klein (zumutbar)", "Groß (unzumutbar)")
                self.pendlerComboBox = ttk.Combobox(
                    self.frame, textvariable=self.selectedPauschale, width=17, values=self.keyvalue_pendler)
                self.pendlerComboBox.place(relx="0.45", rely="0.15")
                self.pendlerComboBox['state'] = 'readonly'
                self.pendlerComboBox.bind(
                    '<<ComboboxSelected>>', self.combineFunc)
                # fahrstrecke in km
                self.km = StringVar()
                self.nb_km_label = tk.Label(
                    self.frame, text="Wegstrecke in Km", font="Arial 8")
                self.nb_km_label.place(x=250, y=115, width=125, height=30)
                self.maxKm = tk.Label(
                    self.frame, text="*Max. 60 km", font=" Verdana 7 bold")
                self.maxKm.place(x=305, y=147, width=120, height=20)
                self.nb_km_input = tk.Entry(self.frame, textvariable=self.km)
                self.nb_km_input.place(x=270, y=150, width=50)
                self.nb_km_input.insert(END, float(0))
            elif int(self.pendler_JaNein.get()) == 1:
                # self.familienBonusComboBox.set('')
                self.pendlerComboBox.destroy()
                self.nb_km_label.destroy()
                self.nb_km_input.destroy()
                self.maxKm.destroy()
        except ValueError as e:
            print(e)
            
    #welcher abzug betrag berücksichtigt werden soll, wenn auf ja dann bezieht er avab
    def showKinder_avab(self)->None:
        if int(self.hatKinderOderNicht.get()) == 0:
            self.kinderAnzahlLabel = Label(
                self.frame, text="*Kinderanzahl", font="Verdana 8 bold ")
            self.kinderAnzahlLabel.place(
                    x=435, y=330, width=120, height=20)
            # kinderanzahlgesamt
            self.kinderAnzahlgesamt = IntVar()
            self.kinderAnzahlEntry = tk.Entry(
                    self.frame, textvariable=self.kinderAnzahlgesamt)
            self.kinderAnzahlEntry.place(x=560, y=330, width=20, height=20)
            self.kinderAnzahlEntry.insert(END, int(0))
        elif int(self.hatKinderOderNicht.get()) == 1:
            self.kinderAnzahlLabel.destroy()
            self.kinderAnzahlEntry.destroy()

    #Kinder dynamisch durch buttons anzeigen lassen
    def showKinderFamilienBonus(self) -> None:
        try:
            if int(self.hatKinderOderNicht.get()) == 0:
                # kinder über 18
                self.kinderOver18Label = Label(
                    self.frame, text="**Kinder über 18 Jahre", font="Verdana 7 bold ")
                self.kinderOver18Label.place(
                    x=435, y=270, width=120, height=20)
                #wir binden die buttons an 2 verschiedene Funktionen, einmal für kinder unter 18 
                # und für kinder über 18, die id wird mit übergeben
                self.kind_0_over18 = Button(
                    self.frame, text='0', bg='white',  command=partial(self.getKinderAnzahlOver18, 0))
                self.kind_0_over18.place(x=445, y=295)
                self.kind_1_over18 = Button(
                    self.frame, text='1', bg='white',  command=partial(self.getKinderAnzahlOver18, 1))
                self.kind_1_over18.place(x=465, y=295)
                self.kind_2_over18 = Button(
                    self.frame, text='2', bg='white',  command=partial(self.getKinderAnzahlOver18, 2))  
                self.kind_2_over18.place(x=485, y=295)
                self.kind_3_over18 = Button(
                    self.frame, text='3', bg='white',  command=partial(self.getKinderAnzahlOver18, 3))
                self.kind_3_over18.place(x=505, y=295)
                self.kind_4_over18 = Button(
                    self.frame, text='4', bg='white', command=partial(self.getKinderAnzahlOver18, 4))
                self.kind_4_over18.place(x=525, y=295)
                self.kind_5_over18 = Button(
                    self.frame, text='5', bg='white', command=partial(self.getKinderAnzahlOver18, 5))
                self.kind_5_over18.place(x=545, y=295)
                # ##########################################
                self.kinderUnder18Label = Label(
                    self.frame, text="**Kinder unter 18 Jahre", font="Verdana 7 bold ")
                self.kinderUnder18Label.place(
                    x=435, y=335, width=120, height=20)
                self.kind_0_under18 = Button(
                    self.frame, text='0', bg='white', command=partial(self.getKinderAnzahlUnder18, 0))
                self.kind_0_under18.place(x=445, y=360)
                self.kind_1_under18 = Button(
                    self.frame, text='1', bg='white', command=partial(self.getKinderAnzahlUnder18, 1))
                self.kind_1_under18.place(x=465, y=360)
                self.kind_2_under18 = Button(
                    self.frame, text='2', bg='white', command=partial(self.getKinderAnzahlUnder18, 2))
                self.kind_2_under18.place(x=485, y=360)
                self.kind_3_under18 = Button(
                    self.frame, text='3', bg='white', command=partial(self.getKinderAnzahlUnder18, 3))
                self.kind_3_under18.place(x=505, y=360)
                self.kind_4_under18 = Button(
                    self.frame, text='4', bg='white', command=partial(self.getKinderAnzahlUnder18, 4))
                self.kind_4_under18.place(x=525, y=360)
                self.kind_5_under18 = Button(
                    self.frame, text='5', bg='white', command=partial(self.getKinderAnzahlUnder18, 5))
                self.kind_5_under18.place(x=545, y=360)

            #labels zerstören
            elif int(self.hatKinderOderNicht.get()) == 1:
                self.kinderOver18Label.destroy()
                self.kinderUnder18Label.destroy()
                self.kind_0_over18.destroy()
                self.kind_1_over18.destroy()
                self.kind_2_over18.destroy()
                self.kind_3_over18.destroy()
                self.kind_4_over18.destroy()
                self.kind_5_over18.destroy()
                self.kind_0_under18.destroy()
                self.kind_1_under18.destroy()
                self.kind_2_under18.destroy()
                self.kind_3_under18.destroy()
                self.kind_4_under18.destroy()
                self.kind_5_under18.destroy()
        except ValueError as e:
            print(e)
            

    # Kinderanzahl über 18 ermitteln und falls ein button angeclickt ist dann sind die anderen gegraut, 
    # eine variable self.kidsOver18 wird auf das gecklickte initialisiert und kann überall mit self verwendet werden
    def getKinderAnzahlOver18(self, kinderAnzahl):
        self.kidsOver18= int
        if kinderAnzahl == 0:
            self.kind_0_over18.config(bg='blue')
            self.kind_1_over18.config(bg='white')
            self.kind_2_over18.config(bg='white')
            self.kind_3_over18.config(bg='white')
            self.kind_4_over18.config(bg='white')
            self.kind_5_over18.config(bg='white')
            self.kidsOver18 = 0
        
        if kinderAnzahl == 1:
            self.kind_1_over18.config(bg='blue')
            self.kind_0_over18.config(bg='white')
            self.kind_2_over18.config(bg='white')
            self.kind_3_over18.config(bg='white')
            self.kind_4_over18.config(bg='white')
            self.kind_5_over18.config(bg='white')
            self.kidsOver18 = 1

        elif kinderAnzahl == 2:
            self.kind_2_over18.config(bg='blue')
            self.kind_0_over18.config(bg='white')
            self.kind_1_over18.config(bg='white')
            self.kind_3_over18.config(bg='white')
            self.kind_4_over18.config(bg='white')
            self.kind_5_over18.config(bg='white')
            self.kidsOver18 = 2
            
        elif kinderAnzahl == 3:
            self.kind_3_over18.config(bg='blue')
            self.kind_0_over18.config(bg='white')
            self.kind_2_over18.config(bg='white')
            self.kind_1_over18.config(bg='white')
            self.kind_4_over18.config(bg='white')
            self.kind_5_over18.config(bg='white')
            self.kidsOver18 = 3
            
        elif kinderAnzahl == 4:
            self.kind_4_over18.config(bg='blue')
            self.kind_0_over18.config(bg='white')
            self.kind_2_over18.config(bg='white')
            self.kind_3_over18.config(bg='white')
            self.kind_1_over18.config(bg='white')
            self.kind_5_over18.config(bg='white')
            self.kidsOver18 = 4
            
        elif kinderAnzahl == 5:
            self.kind_5_over18.config(bg='blue')
            self.kind_0_over18.config(bg='white')
            self.kind_2_over18.config(bg='white')
            self.kind_3_over18.config(bg='white')
            self.kind_4_over18.config(bg='white')
            self.kind_1_over18.config(bg='white')
            self.kidsOver18 = 5
        return self.kidsOver18


    # Kinderanzahl unter 18 ermitteln und falls ein button angeclickt ist dann sind die anderen gegraut, 
    # eine variable self.kidsUnder18 wird auf das gecklickte initialisiert und kann überall mit self verwendet werden
    def getKinderAnzahlUnder18(self, kinderAnzahl):
        self.kidsUnder18 = int
        if kinderAnzahl == 0:
            self.kind_0_under18.config(bg='blue')
            self.kind_1_under18.config(bg='white')
            self.kind_2_under18.config(bg='white')
            self.kind_3_under18.config(bg='white')
            self.kind_4_under18.config(bg='white')
            self.kind_5_under18.config(bg='white')
            self.kidsUnder18 = 0
        elif kinderAnzahl == 1:
            self.kind_1_under18.config(bg='blue')
            self.kind_0_under18.config(bg='white')
            self.kind_2_under18.config(bg='white')
            self.kind_3_under18.config(bg='white')
            self.kind_4_under18.config(bg='white')
            self.kind_5_under18.config(bg='white')
            self.kidsUnder18 = 1
        elif kinderAnzahl == 2:
            self.kind_2_under18.config(bg='blue')
            self.kind_0_under18.config(bg='white')
            self.kind_1_under18.config(bg='white')
            self.kind_3_under18.config(bg='white')
            self.kind_4_under18.config(bg='white')
            self.kind_5_under18.config(bg='white')
            self.kidsUnder18 = 2
        elif kinderAnzahl == 3:
            self.kind_3_under18.config(bg='blue')
            self.kind_0_under18.config(bg='white')
            self.kind_2_under18.config(bg='white')
            self.kind_1_under18.config(bg='white')
            self.kind_4_under18.config(bg='white')
            self.kind_5_under18.config(bg='white')
            self.kidsUnder18 = 3
        elif kinderAnzahl == 4:
            self.kind_4_under18.config(bg='blue')
            self.kind_0_under18.config(bg='white')
            self.kind_2_under18.config(bg='white')
            self.kind_3_under18.config(bg='white')
            self.kind_1_under18.config(bg='white')
            self.kind_5_under18.config(bg='white')
            self.kidsUnder18 = 4
        elif kinderAnzahl == 5:
            self.kind_5_under18.config(bg='blue')
            self.kind_0_under18.config(bg='white')
            self.kind_2_under18.config(bg='white')
            self.kind_3_under18.config(bg='white')
            self.kind_4_under18.config(bg='white')
            self.kind_1_under18.config(bg='white')
            self.kidsUnder18 = 5
            
    # Der Monat holen
    def monatAndEcard(self, event=None) -> tuple[int, float]:
        monat = self.selected_month.get()
        monatConverted = int(0)
        eCard = float(0)
        if monat == 'April':
            monatConverted = 4
        elif monat == 'Jan':
            monatConverted = 1
            eCard = 0
        elif monat == 'Feb':
            monatConverted = 2
            eCard = 0
        elif monat == 'Mär':
            monatConverted = 3
            eCard = 0
        elif monat == 'Apr':
            monatConverted = 4
            eCard = 0
        elif monat == 'Mai':
            monatConverted = 5
            eCard = 0
        elif monat == 'Jun':
            monatConverted = 6
            eCard = 0
        elif monat == 'Jul':
            monatConverted = 7
            eCard = 0
        elif monat == 'Aug':
            monatConverted = 8
            eCard = 0
        elif monat == 'Sep':
            monatConverted = 9
            eCard = 0
        elif monat == 'Okt':
            monatConverted = 10
            eCard = 0
        elif monat == 'Nov':
            monatConverted = 11
            eCard = 12.95
        elif monat == 'Dez':
            monatConverted = 12
            eCard = 0
        return monatConverted, eCard
    
    
    #Pendlerpauschale ausrechnen 
    def pendlerArt(self) -> int:
        # km variable definieren, und bools, diese bool werte werden aber nicht mit return gerendert
        km = float(0)
        pendlerKlein = bool
        pendlerGroß = bool
        beziehtPS = bool
        pendlerBetrag = int(0)
        try:
            pendlerPauschale = str(self.selectedPauschale.get())
            beziehtPendlerpauschale = int(self.pendler_JaNein.get())
            if(beziehtPendlerpauschale == 0) and pendlerPauschale == "Klein (zumutbar)":
                km = float(self.km.get())
                pendlerKlein = True
                beziehtPS = True
                if pendlerKlein and beziehtPS and (20 < km < 40):
                    pendlerBetrag = 58
                elif pendlerKlein and beziehtPS and (40 < km < 60):
                    pendlerBetrag = 113
                elif pendlerKlein and beziehtPS and (km > 60):
                    pendlerBetrag = 168
                elif pendlerKlein and beziehtPS and (km < 20):
                    pendlerBetrag = 0
            if(beziehtPendlerpauschale == 0) and pendlerPauschale == "Groß (unzumutbar)":
                km = float(self.km.get())
                pendlerGroß = True
                beziehtPS = True
                if pendlerGroß and beziehtPS and 2 < km < 20:
                    pendlerBetrag = 31
                elif pendlerGroß and beziehtPS and 20 < km < 40:
                    pendlerBetrag = 123
                elif pendlerGroß and beziehtPS and 40 < km < 60:
                    pendlerBetrag = 214
                elif pendlerGroß and beziehtPS and km > 60:
                    pendlerBetrag = 306
                elif pendlerGroß and beziehtPS and km < 2:
                    pendlerBetrag = 0
            if(beziehtPendlerpauschale == 1) and pendlerPauschale == "Kein Bezug":
                pendlerBetrag = 0
        except ValueError as e:
            print(e)
        finally:
            return pendlerBetrag

    # Familienbonus ausrechnen
    def Familienbonus(self) -> float:
        FamilienBonusBetrag = float
        over18 = int(0)
        under18 = int(0)
        fabö_under18_voll = 125
        fabö_over18_voll = 54.18
        fabö_under18_halb = 62.50
        fabö_over18_halb = 27.09
        #wieder auf 0 setzen wenn nein gedrückt wird
        if int(self.hatKinderOderNicht.get()) == 1:
            self.kidsOver18 = 0
            self.kidsUnder18 = 0
        else:
                over18 = self.kidsOver18
                under18 = self.kidsUnder18
        try:
            if str(self.selectedBonus.get()) == "Voller Bonus" and int(self.hatKinderOderNicht.get()) == 0:
                FamilienBonusBetrag = under18*fabö_under18_voll + over18*fabö_over18_voll
            elif str(self.selectedBonus.get()) == "Halber Bonus" and  int(self.hatKinderOderNicht.get()) == 0:
                FamilienBonusBetrag = under18*fabö_under18_halb + over18*fabö_over18_halb
                print(FamilienBonusBetrag)
            else:
                FamilienBonusBetrag = 0
        except ValueError as e:
            print(e)
        finally:
            return FamilienBonusBetrag


    # spzialversicherungsfunktion
    def calc_szBrutto(self, brutto, first_szSon, second_szSon, third_szSon, fourth_szSon) -> float:
        br_grenze_first = 1828
        br_grenze_second_start = 1828.01
        br_grenze_second_end = 1994
        br_grenze_third_start = 1994.01
        br_grenze_third_end = 2161
        br_grenze_fourth_start = 2161.01
        br_grenze_fourth_end = 5670
        try:
            if brutto <= br_grenze_first:
                return round(brutto*first_szSon, 2)
            elif brutto >= br_grenze_second_start and brutto <= br_grenze_second_end:
                return round(brutto*second_szSon, 2)
            elif brutto >= br_grenze_third_start and brutto <= br_grenze_third_end:
                return round(brutto * third_szSon, 2)
            elif brutto >= br_grenze_fourth_start and brutto < br_grenze_fourth_end:
                return round(brutto * fourth_szSon, 2)
            else:
                brutto = br_grenze_fourth_end
        except ValueError as e:
            print(e)
        return brutto

    # Gewerkschaftsbeitrag ausrechnen
    def gewerkbtrg(self) -> float:
        gewerkschaftsbeitrag_limit = 35.30
        gewerkschaftsbeitrag_prozentsatz = 1/100
        betrag = float(0)
        bruttoLohn = float(self.bruttoLohn.get())
        try:
            if float(self.gwBeitrag.get()) == 0:
                betrag = bruttoLohn*gewerkschaftsbeitrag_prozentsatz
            else:
                betrag = float(self.gwBeitrag.get())
                if betrag > gewerkschaftsbeitrag_limit:
                    betrag = gewerkschaftsbeitrag_limit
                    
        except ValueError as e:
            print(e)
        finally:
            return betrag
        

    # Die Überstunden ausrechnen
    def ueberstunden(self) -> tuple[float, float]:
        ueberstunden_50_Prozent = float(self.ueberstunden_50_Prozent.get())
        ueberstunden_100_Prozent = float(self.ueberstunden_100_Prozent.get())
        ueT = float(self.ueT.get())
        stundenlohn = float(self.stundenlohn.get())
        bruttoLohn = float(self.bruttoLohn.get())
        ueberstundenSteuerfrei = float
        ueberstundenEntgelt = float
        stdLohn = float
        
        try:
            # wenn das Überstunden Feld nicht leer ist, und ungleich null ist, dann std berechnen
            # aber mit der funktion validateEntries() wird sowieso darauf geachtet dass die Felder nicht leer sind weil
            
            if int(self.ueberstunden_JaNein.get()) == 0:
                if ueT != 0.0 and ueT != "":
                    stdLohn = bruttoLohn / ueT
                # hier wird die Division durch 0 umgangen
                elif ueT == 0:
                    stdLohn = stundenlohn
                # und wenn das Feld leer ist
                elif ueT == "":
                    stdLohn = stundenlohn

                # überstundengrundlage ausrechnen
                ueberstundenGrundlage = ueberstunden_50_Prozent * \
                    stdLohn + ueberstunden_100_Prozent*stdLohn
                ueberstundenZuschlag_50_Prozent = ueberstunden_50_Prozent*stdLohn / 2
                ueberstundenZuschlag_100_Prozent = ueberstunden_100_Prozent*stdLohn
                ueberstundenEntgelt = ueberstundenGrundlage + \
                    ueberstundenZuschlag_50_Prozent + ueberstundenZuschlag_100_Prozent

                # auf den steuerfreien Betrag achten
                if ueberstunden_50_Prozent <= 10 and ueberstundenZuschlag_50_Prozent <= 86:
                    ueberstundenSteuerfrei = ueberstundenZuschlag_50_Prozent
                elif ueberstunden_50_Prozent > 10 and ueberstundenZuschlag_50_Prozent <= 86:
                    ueberstundenSteuerfrei = stdLohn*10*0.5
                elif ueberstunden_50_Prozent < 10 and ueberstundenZuschlag_50_Prozent > 86:
                    ueberstundenSteuerfrei = 86
                elif ueberstunden_50_Prozent > 10 and ueberstundenZuschlag_50_Prozent > 86:
                    ueberstundenSteuerfrei = 86
                if ueberstundenZuschlag_100_Prozent <= 360:
                    ueberstundenSteuerfrei = ueberstundenSteuerfrei + ueberstundenZuschlag_100_Prozent
                elif ueberstundenZuschlag_100_Prozent > 360:
                    ueberstundenSteuerfrei = ueberstundenSteuerfrei + 360
            else:
                ueberstundenEntgelt = 0
                ueberstundenSteuerfrei = 0
        except ValueError as e:
            print(e)
        finally:
            return ueberstundenEntgelt, ueberstundenSteuerfrei


    # Bemessungsgrundlage für die Lohnsteuer berechnen
    def Bemessung(self) -> tuple[float, float, int]:
        # werte aus der gui
        bruttoLohn = float(self.bruttoLohn.get())
        sachbezug = float(self.sachbezug.get())
        freibetrag = float(self.freibetrag.get())
        # to avoid error: referenced before assignment
        ueberstundenSteuefreiBetrag = float(0)
        Bemessung_fuer_Lohnsteuer = float(0)
        eCard = float(0)
        pendlerBetrag = int(0)
        svBeitragBrutto = float(0)

        # monat aus monatAndEcard()
        eCard: float = self.monatAndEcard()[1]
        gewerkschaftsbeitrag = self.gewerkbtrg()
        familienBonus = self.Familienbonus()
        pendlerBetrag: int = self.pendlerArt()

        # Überstundenfreibetrag mithilfe der funktion ueberstunden holen
        ueberstundenSteuefreiBetrag: float = round((self.ueberstunden()[1]), 2)
        # sozialversicherung mithilfe der funktion calc_szBrutto
        first_sz = (15.12/100)
        second_sz = (16.12/100)
        third_sz = (17.12/100)
        fourth_sz = (18.12/100)
        
        try:
                svBeitragBrutto: float = round((self.calc_szBrutto(bruttoLohn,  first_sz, second_sz, third_sz, fourth_sz)), 2)
                Bemessung_fuer_Lohnsteuer = bruttoLohn + sachbezug - svBeitragBrutto - freibetrag - \
                familienBonus - eCard - gewerkschaftsbeitrag - \
                pendlerBetrag - ueberstundenSteuefreiBetrag
        except ValueError as e:
            print(e)
        finally:
            return Bemessung_fuer_Lohnsteuer, svBeitragBrutto, pendlerBetrag



    #FIXME: VALUE IS CHACHED, IF YOU PASS SOMETHING THAN YOU SWITCH BACK TO NO 
    def sonderzahlungLohnsteuer(self) -> tuple[float, float, float]:
        monat: int = self.monatAndEcard()[0]
        bemessungSonderzahlung = float(0)
        lohnsteuerSonderzahlung = float(0)
        szvSonderzahlung = float(0)
        sonderZahlungUrlaub = float(0)
        restbetrag = float(0)
        summeBezügeLaufend = float(0)
        jahressechstelBetrag = float(0)
        sonderSteuerSatz = 6/100
        
        try:
            bruttoLohn = float(self.bruttoLohn.get())
            sonstigeSonderzahlung = float(self.sonstigeSonderzahlung.get())
            sonderZahlungUrlaub = float(self.urlaubsbeihilfe.get())
            szvSonderzahlung = round((self.calc_szBrutto(sonderZahlungUrlaub, (14.12/100), (15.12/100), (16.12/100), (17.12/100))), 2)
            summeBezügeLaufend = bruttoLohn*monat
            jahressechstelBetrag = summeBezügeLaufend/monat * 2
            
            if int(self.ub_bezogenOdernicht.get()) == 1 and int(self.ubVorhandenOderNicht.get()) == 0:
                bemessungSonderzahlung = sonderZahlungUrlaub - szvSonderzahlung
            elif int(self.ub_bezogenOdernicht.get()) == 0 and int(self.ubVorhandenOderNicht.get()) == 1:
                bemessungSonderzahlung = sonderZahlungUrlaub - szvSonderzahlung - 620
            if bruttoLohn < jahressechstelBetrag:
                lohnsteuerSonderzahlung = bemessungSonderzahlung*sonderSteuerSatz
            else: 
                restbetrag = sonderZahlungUrlaub - jahressechstelBetrag
        except ValueError as e:
            print(e)
        finally:
            return lohnsteuerSonderzahlung, szvSonderzahlung, jahressechstelBetrag


    # Mithilfe der Bemessungsgrundlage die Lohnsteuer berechnen
    def lohnsteuerBemessung(self) -> float:
        lohnsteuerBetrag = float(0)
        Bemessung_fuer_Lohnsteuer = float(0)
        Bemessung_fuer_Lohnsteuer = round((self.Bemessung()[0]), 2)
        try:
            if 0 < Bemessung_fuer_Lohnsteuer < 927.67:
                lohnsteuerBetrag = 0
            elif 927.67 < Bemessung_fuer_Lohnsteuer < 1511.00:
                lohnsteuerBetrag = Bemessung_fuer_Lohnsteuer*0.2
                
            elif 1511.00 < Bemessung_fuer_Lohnsteuer < 2594.33:
                lohnsteuerBetrag = Bemessung_fuer_Lohnsteuer*0.325
                
            elif 2594.33 < Bemessung_fuer_Lohnsteuer < 5011.00:
                lohnsteuerBetrag = Bemessung_fuer_Lohnsteuer*0.42
            elif 5011.00 < Bemessung_fuer_Lohnsteuer < 7511.00:
                lohnsteuerBetrag = Bemessung_fuer_Lohnsteuer*0.48
                
            elif 7511.00 < Bemessung_fuer_Lohnsteuer < 83344.33:
                lohnsteuerBetrag = Bemessung_fuer_Lohnsteuer*0.5
            elif Bemessung_fuer_Lohnsteuer > 83344.33:
                lohnsteuerBetrag = Bemessung_fuer_Lohnsteuer*0.55
        except ValueError as e:
            print(e)
        finally:
            return lohnsteuerBetrag


    # Abzugsbetrag ohne alleinverdiener/erzieher zu sein
    def abzugOhnAB(self) -> float:
        Bemessung_fuer_Lohnsteuer = float(0)
        Bemessung_fuer_Lohnsteuer = round((self.Bemessung()[0]), 2)
        abzugOhneAB = float(0)
        try:
            if 0 < Bemessung_fuer_Lohnsteuer < 927.67:
                abzugOhneAB = 0
            elif 927.67 < Bemessung_fuer_Lohnsteuer < 1511.00:
                abzugOhneAB = 218.86
            elif 1511.00 < Bemessung_fuer_Lohnsteuer < 2594.33:
                abzugOhneAB = 407.74
            elif 2594.33 < Bemessung_fuer_Lohnsteuer < 5011.00:
                abzugOhneAB = 654.20
            elif 5011.00 < Bemessung_fuer_Lohnsteuer < 7511.00:
                abzugOhneAB = 954.86
            elif 7511.00 < Bemessung_fuer_Lohnsteuer < 83344.33:
                abzugOhneAB = 1105.08
            elif Bemessung_fuer_Lohnsteuer > 83344.33:
                abzugOhneAB = 5272.30
        except ValueError as e:
            print(e)
        finally:
            return abzugOhneAB

    #Alleinverdiener/erzieher -absetzbeträge
    def abzugMitAB(self) -> float:

        try:
            kinderAnzahl = int(self.kinderAnzahlgesamt.get())
            Bemessung_fuer_Lohnsteuer = float(0)
            Bemessung_fuer_Lohnsteuer = round((self.Bemessung()[0]), 2)
            abzugMitAb = float(0)
            # steuerklasse 0%
            if int(self.hatKinderOderNicht.get()) == 0:
                    
                if 0 < Bemessung_fuer_Lohnsteuer < 927.67:
                    abzugMitAb = 0

                # steuerklasse 20%
                if 927.67 < Bemessung_fuer_Lohnsteuer < 1511.00 and kinderAnzahl == 1:
                    abzugMitAb = 260.03
                elif 927.67 < Bemessung_fuer_Lohnsteuer < 1511.00 and kinderAnzahl == 2:
                    abzugMitAb = 274.61
                elif 927.67 < Bemessung_fuer_Lohnsteuer < 1511.00 and kinderAnzahl == 3:
                    abzugMitAb = 292.94
                elif 927.67 < Bemessung_fuer_Lohnsteuer < 1511.00 and kinderAnzahl == 4:
                    abzugMitAb = 311.27
                elif 927.67 < Bemessung_fuer_Lohnsteuer < 1511.00 and kinderAnzahl == 5:
                    abzugMitAb = 329.60
                elif kinderAnzahl > 5:
                    abzugMitAb = 329.60

                # steuerklasse 32.5%
                if 1511.00 < Bemessung_fuer_Lohnsteuer < 2594.33 and kinderAnzahl == 1:
                    abzugMitAb = 448.91
                elif 1511.00 < Bemessung_fuer_Lohnsteuer < 2594.33 and kinderAnzahl == 2:
                    abzugMitAb = 463.49
                elif 1511.00 < Bemessung_fuer_Lohnsteuer < 2594.33 and kinderAnzahl == 3:
                    abzugMitAb = 481.82
                elif 1511.00 < Bemessung_fuer_Lohnsteuer < 2594.33 and kinderAnzahl == 4:
                    abzugMitAb = 500.15
                elif 1511.00 < Bemessung_fuer_Lohnsteuer < 2594.33 and kinderAnzahl == 5:
                    abzugMitAb = 518.48
                elif kinderAnzahl > 5:
                    abzugMitAb = 518.48

                # steuerklasse 42%
                if 2594.33 < Bemessung_fuer_Lohnsteuer < 5011.00 and kinderAnzahl == 1:
                    abzugMitAb = 695.37
                elif 2594.33 < Bemessung_fuer_Lohnsteuer < 5011.00 and kinderAnzahl == 2:
                    abzugMitAb = 709.95
                elif 2594.33 < Bemessung_fuer_Lohnsteuer < 5011.00 and kinderAnzahl == 3:
                    abzugMitAb = 728.28
                elif 2594.33 < Bemessung_fuer_Lohnsteuer < 5011.00 and kinderAnzahl == 4:
                    abzugMitAb = 746.61
                elif 2594.33 < Bemessung_fuer_Lohnsteuer < 5011.00 and kinderAnzahl == 5:
                    abzugMitAb = 764.94
                elif kinderAnzahl > 5:
                    abzugMitAb = 764.94

                # steuerklasse 48%
                if 5011.00 < Bemessung_fuer_Lohnsteuer < 7511.00 and kinderAnzahl == 1:
                    abzugMitAb = 996.03
                elif 5011.00 < Bemessung_fuer_Lohnsteuer < 7511.00 and kinderAnzahl == 2:
                    abzugMitAb = 1010.61
                elif 5011.00 < Bemessung_fuer_Lohnsteuer < 7511.00 and kinderAnzahl == 3:
                    abzugMitAb = 1028.94
                elif 5011.00 < Bemessung_fuer_Lohnsteuer < 7511.00 and kinderAnzahl == 4:
                    abzugMitAb = 1047.27
                elif 5011.00 < Bemessung_fuer_Lohnsteuer < 7511.00 and kinderAnzahl == 5:
                    abzugMitAb = 1065.60
                elif kinderAnzahl > 5:
                    abzugMitAb = 1065.60

                # steuerklasse 50%
                if 7511.00 < Bemessung_fuer_Lohnsteuer < 83344.33 and kinderAnzahl == 1:
                    abzugMitAb = 1146.25
                elif 7511.00 < Bemessung_fuer_Lohnsteuer < 83344.33 and kinderAnzahl == 2:
                    abzugMitAb = 1160.83
                elif 7511.00 < Bemessung_fuer_Lohnsteuer < 83344.33 and kinderAnzahl == 3:
                    abzugMitAb = 1179.16
                elif 7511.00 < Bemessung_fuer_Lohnsteuer < 83344.33 and kinderAnzahl == 4:
                    abzugMitAb = 1197.49
                elif 7511.00 < Bemessung_fuer_Lohnsteuer < 83344.33 and kinderAnzahl == 5:
                    abzugMitAb = 1215.82
                elif kinderAnzahl > 5:
                    abzugMitAb = 1215.82

                # steuerklasse 55%
                if Bemessung_fuer_Lohnsteuer > 83344.33 and kinderAnzahl == 1:
                    abzugMitAb = 5313.47
                elif Bemessung_fuer_Lohnsteuer > 83344.33 and kinderAnzahl == 2:
                    abzugMitAb = 5328.05
                elif Bemessung_fuer_Lohnsteuer > 83344.33 and kinderAnzahl == 3:
                    abzugMitAb = 5346.38
                elif Bemessung_fuer_Lohnsteuer > 83344.33 and kinderAnzahl == 4:
                    abzugMitAb = 5364.71
                elif Bemessung_fuer_Lohnsteuer > 83344.33 and kinderAnzahl == 5:
                    abzugMitAb = 5383.04
                elif kinderAnzahl > 5:
                    abzugMitAb = 5383.04
            else:
                
                abzugMitAb = 0
                
            #print("Das ist abzugMitAb aus AbzugMit: " +str(abzugMitAb))
            
        except ValueError as e:
            print(e)
        finally:
            return abzugMitAb


    # Nettolohn berechnen
    def brutto_netto_berechnen(self) -> tuple[float, float, float, float, float, float, float, float, float]:
        
        # Define variable to avoid assignment error/also get some other variables from other functions
        km = float(self.km.get())
        bruttoLohn = float(self.bruttoLohn.get())
        urlaubsbeihilfe = float(self.urlaubsbeihilfe.get())
        freibetrag = float(self.freibetrag.get())

        pendlerEuro = float(0)
        familienBonus = float(0)
        LohnsteuerBetrag = float(0)
        netto_ergebnis = float(0)

        svBeitrag = round((self.Bemessung()[1]), 2)
        lstSonderzahlung = round((self.sonderzahlungLohnsteuer()[0]), 2)
        svSonderzahlung = round((self.sonderzahlungLohnsteuer()[1]), 2)
        gewerkschaftsbeitrag = round((self.gewerkbtrg()), 2)
        eCard = self.monatAndEcard()[1]

        pendlerEuro = km*2
        familienBonus = self.Familienbonus()
        LohnsteuerBetrag = round((self.lohnsteuerBemessung()), 2) 
        abzugsbetrag_ohneKinder = self.abzugOhnAB()
        abzugsbetrag_mitKinder = self.abzugMitAB()
        pendlerpauschaleBetrag=self.Bemessung()[2]
        
        
        
        Over18 = int(0)
        Under18 = int(0)
        self.kidsOver18 
        self.kidsUnder18 
        kinderAnzahl = int(0)
        Over18 = self.kidsOver18
        Under18 = self.kidsUnder18
        kinderAnzahl = Over18 + Under18

        try:
            if int(self.hatKinderOderNicht.get()) == 1 and int(self.kinderAnzahlgesamt.get()) == 0:
                LohnsteuerBetrag = LohnsteuerBetrag - \
                    abzugsbetrag_ohneKinder - familienBonus - pendlerEuro

            elif int(self.hatKinderOderNicht.get()) == 0 and  int(self.kinderAnzahlgesamt.get()) > 0:
                LohnsteuerBetrag = LohnsteuerBetrag - \
                    abzugsbetrag_mitKinder - familienBonus - pendlerEuro

            if int(self.ub_bezogenOdernicht.get()) == 0:
                netto_ergebnis = bruttoLohn + urlaubsbeihilfe - svBeitrag - \
                    svSonderzahlung - LohnsteuerBetrag - \
                    lstSonderzahlung - gewerkschaftsbeitrag - eCard
                    
            elif int(self.ub_bezogenOdernicht.get()) == 1:
                netto_ergebnis = bruttoLohn - svBeitrag - \
                    LohnsteuerBetrag - gewerkschaftsbeitrag - eCard
            print("Das ist das Nettoergebnis: " + str(netto_ergebnis))
            
            119,33
            
            
            insert_loko(conn,"12312", bruttoLohn, netto_ergebnis, svBeitrag, pendlerpauschaleBetrag, familienBonus, gewerkschaftsbeitrag, freibetrag, eCard, pendlerEuro)
            # insert_ss(conn, szn, ss_sach=0, ss_sonder=0)
            # insert_steuerdaten(conn, szn, sd_pndl=0, sd_gpp=0, sd_kpp=0, sd_pdkm=0, sd_fabo=0, sd_kun=0, sd_kue=0, sd_gwk=0, sd_vllb=0, sd_nov=0)
        

        except ValueError as e:
            print(e)
        finally:
            return netto_ergebnis, LohnsteuerBetrag, svBeitrag, gewerkschaftsbeitrag, familienBonus, eCard, pendlerEuro, abzugsbetrag_ohneKinder, abzugsbetrag_mitKinder



    #create a payroll to show all the calculated values 
    def create_payroll(self):
        ws = Tk()
        ws.title('Lohnzettel')
        ws.geometry('1350x800')
        
        classPayRollLoginInstance = PayrollLoginMenu(self.app)
        vorname = classPayRollLoginInstance.nb_vorname_input.get()
        nachname = classPayRollLoginInstance.nb_nachname_input.get()
        print("vorname test: " + str(vorname))
        
        
        ppArt = str()
        if str(self.selectedPauschale.get()) == "Groß (unzumutbar)":
            ppArt = "G. Pauschale"
        elif str(self.selectedPauschale.get()) == "Klein (zumutbar)":
            ppArt = "K. Pauschale"
        if int(self.pendler_JaNein.get()) == 1:
            ppArt = "Keine"

        nettoLohn = round((self.brutto_netto_berechnen()[0]), 2)
        szvbeitrag= self.brutto_netto_berechnen()[2]
        pendlerpauschaleBetrag=self.Bemessung()[2]
        freiBetrag = float(self.freibetrag.get())
        familyBonus = float(self.brutto_netto_berechnen()[4])
        
        
        gwBeitrag = float(self.brutto_netto_berechnen()[3])
        
        eCard =  float(self.brutto_netto_berechnen()[5])
        pendlerEuro = float(self.brutto_netto_berechnen()[6])

        
        

        
        bemessung_lohnsteuer = round((self.Bemessung()[0]), 2)
        abzugsbetrag_ohneKinder = str(self.brutto_netto_berechnen()[7])
        abzugsbetrag_mitKinder = str(self.brutto_netto_berechnen()[8])
        abzügeBeträge = abzugsbetrag_ohneKinder + "/" + abzugsbetrag_mitKinder
        ub = str(self.urlaubsbeihilfe.get())
        sonstSonderzahlung = str(self.sonstigeSonderzahlung.get())
        ueberstundenEntgelt = self.ueberstunden()[0]
        ueberstundenFreibetrag = self.ueberstunden()[1]
        
        lohnsteuerSonderzahlung = self.sonderzahlungLohnsteuer()[0]
        lohnsteuerSV = self.sonderzahlungLohnsteuer()[1]
        jahressechstelBetrag = self.sonderzahlungLohnsteuer()[2]
        lohnsteuerBetrag = self.lohnsteuerBemessung()
        
        
        
        
    # Um diese Methode insert_steuerdaten zu benutzen, sollte man diese Paramater ausfüllen
    
    # insert_steuerdaten(conn,szn,
    # gibt es eine Pendlerpauschale(0 ooder 1), 
    # ist eine große PP?(0 ider 1), ist es eine kleine PP?(0 oder 1),gefahrene Kilomter, gibt es einen Familienbonus?(0 oder 1),
    # wie viele kinder sind unter 18?, wie viele Kinder sind über 18?, Ist man bei der Gewerkschaft angemeldet?(0 oder 1), gibt es einen vollen Bonus?(0 oder 1), ist es Novemeber?(0 oder 1))
    
    # 0 steht für NEIN
    # 1 steht für JA
    
    
   
        # insert_steuerdaten(conn,'12312')
        # insert_ss(conn,'12312')

        datum = time.strftime("%a, %d %b %Y %H:%M")
        wd=Label(ws,text="Lohn/Gehaltabrechnung ", font="Verdana 20 bold",relief = "solid",width = 50 , height = 2)
        wd.place(x=310,y=7)
        ms = Label(wd, text="MetiSoft",
                            font="Verdana 15 bold ")
        ms.place(x=10,y=10)
        ms2 = Label(wd, text="GmbH",
                            font="Verdana 15 bold ")
        ms2.place(x=10,y=35)
        st=Label(ws,text="", font="Verdana 20 bold",relief = "solid",width = 50 , height = 2)
        st.grid(row=0,column=0,pady=75,padx=310)
        wt = Label(st, text=" Klient:", font="Verdana 8 ")
        wt.place(x=30,y=7)
        dt1 = Label(st, text=datum, font="Verdana 8 ")
        dt1.place(x=800,y=7)
        pe = Label(st, text=" Person:",
                            font="Verdana 8 ")
        pe.place(x=26,y=40)
        bt=Label(ws,text="",font="Verdana 20 bold",relief = "solid",width = 50 , height = 6)
        bt.place(x=310,y=140)
        n = Label(bt, text=" Vorname:",
                            font="Verdana 8 ")
        n.place(x=30,y=60)
        nn = Label(bt, text=" Nachname:",
                            font="Verdana 8 ")
        nn.place(x=30,y=80)
        a = Label(bt, text=" Adresse:",
                            font="Verdana 8 ")
        a.place(x=30,y=100)
        o = Label(bt, text=" Ort:",
                            font="Verdana 8 ")
        o.place(x=30,y=120)
        s = Label(bt, text=" Stadt:",
                            font="Verdana 8 ")
    
        ueEntgelt = Label(bt, text=" Überstundenentgelt: " + str(ueberstundenEntgelt) + " €",
                            font="Verdana 8 ")
        ueEntgelt.place(x=660,y=20)
        steuerfreieUeberstunden = Label(bt, text=" Davon steuerfrei: " + str(ueberstundenFreibetrag) + " €",
                            font="Verdana 8 ")
        steuerfreieUeberstunden.place(x=660,y=50)
        bemessunglohnsteuer = Label(bt, text="Bemessung für Lohnsteuer: " + str(bemessung_lohnsteuer) + " €",
                            font="Verdana 8 ")
        bemessunglohnsteuer.place(x=660,y=80)
        sts = Label(bt, text= "Lohnsteuerbetrag: " + str(lohnsteuerBetrag) + " €",
                            font="Verdana 8 ")
        sts.place(x=660,y=110)
        fmb = Label(bt, text= "Familienbonus: " + str(familyBonus)+ " €",
                            font="Verdana 8 ")
        fmb.place(x=660,y=140)
        lt=Label(ws,text= "Jahressechstel", font="Verdana 8 bold",relief = "solid",width = 20 , height = 3)
        lt.place(x=310,y=336)
        sv=Label(ws,text="SV - Brutto",font="Verdana 8 bold",relief = "solid",width = 20 , height = 3)
        sv.place(x=460,y=336)
        fb=Label(ws,text="Freibetrag",font="Verdana 8 bold",relief = "solid",width = 20 , height = 3)
        fb.place(x=720,y=336)
        avab=Label(ws,text="AVAB/AEAB ",font="Verdana 8 bold",relief = "solid",width = 20 , height = 3)
        avab.place(x=610,y=336)
        pe=Label(ws,text="Pendlerpauschale",font="Verdana 8 bold",relief = "solid",width =25 , height = 3)
        pe.place(x=750,y=336)
        tt=Label(ws,text="",font="Verdana 20 bold",relief = "solid",width = 50 , height = 1)
        tt.place(x=310,y=370)
        
        b1 = Label(ws, text= str(jahressechstelBetrag) + " €",
                            font="Verdana 8 ")
        b1.place(x=360,y=380)
        
        
        svBrutto = Label(ws, text= str(szvbeitrag) + " €",
                            font="Verdana 8 ")
        svBrutto.place(x=530,y=380)
        avab = Label(ws, text=abzügeBeträge + " €",
                            font="Verdana 8 ")
        avab.place(x=650,y=380)
        pendlerBetrag = Label(ws, text= ppArt + ": " + str(pendlerpauschaleBetrag) + " €",
                            font="Verdana 8 ")
        pendlerBetrag.place(x=780,y=380)
        sachbezuege = Label(ws, text=" Sachbezüge: " + self.sachbezug.get() + " €",
                            font="Verdana 8 ")
        sachbezuege.place(x=965,y=380)
        freibetrag = Label(ws, text=" Freibetrag: " + str(freiBetrag) + " €",
                            font="Verdana 8 ")
        freibetrag.place(x=1130,y=380)

        kt=Label(ws,text="",font="Verdana 20 bold",relief = "solid",width = 50 , height = 2)
        kt.place(x=310,y=400)
        bn=Label(ws,text="",font="Verdana 20 bold",relief = "solid",width = 50 , height = 4)
        bn.place(x=310,y=440)
        
        brt=Label(ws,text="Brutto: " + self.bruttoLohn.get() + " €", font="Verdana 10 bold",bg="yellow",width = 50 , height = 1)
        brt.place(x=800,y=442)
        urlaubsbeihilfeLabel = Label(ws, text= "Urlaubsbeihilfe: " + ub + " €",
                            font="Verdana 8 ", width = 30 , height = 2)
        urlaubsbeihilfeLabel.place(x=315,y=442)
        sonstSonderzahlungLabel = Label(ws, text="Sonstige Sonderzahlungen: " + sonstSonderzahlung + " €",
                            font="Verdana 8 ", width = 30 , height = 2)
        sonstSonderzahlungLabel.place(x=350,y=472)
        szvSonder = Label(ws, text=" Lohnsteuer - Sonderzahlung: " + str(lohnsteuerSonderzahlung) + " €",
                            font="Verdana 8 ", width = 30 , height = 2)
        szvSonder.place(x=360,y=502)
        svSonderzahlung= Label(ws, text=" SV - Beitrag Sonderzahlung: " + str(lohnsteuerSV) + " €",
                            font="Verdana 8 ", width = 30 , height = 2)
        svSonderzahlung.place(x=360,y=534)
        net=Label(ws,text="Netto: " + str(nettoLohn) + " €",font="Verdana 10 bold",bg="yellow",width = 50 , height = 1)
        net.place(x=800,y=550)
        lb=Label(ws,text="Laufender Bezug",font="Verdana 20 bold",relief = "solid",width = 40 , height = 1)
        lb.place(x=400,y=600)
        ws.mainloop()
        
    # Go back to menu
    def back_to_menu(self):
        self.app.main_menu.show()
        #self.clear_inputs()

    #Reset every field
    def clear_inputs(self):
        self.nb_fb_input.delete(0, "end")
        self.stdl_input.delete(0, "end")
        self.ueberstundenTeiler_input.delete(0, "end")
        self.nb_us100_input.delete(0, "end")
        self.nb_us50_input.delete(0, "end")
        self.nb_km_input.delete(0, "end")
        self.nb_urlaubsbeihilfe_input.delete(0, "end")
        self.sonstigeSonderzahlung_input.delete(0, "end")
        self.nb_gwBeitrag_label_input.delete(0, "end")
        self.nb_fb_input.delete(0, "end")
        self.reisekostenInput.delete(0, "end")
        self.nb_sb_label.delete(0, "end")
        self.nb_brutto_input.delete(0, "end")
        
    def show(self):
        self.frame.tkraise()
if __name__ == "__main__":
    application = Application()
