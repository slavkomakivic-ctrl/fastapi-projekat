import sqlite3

konekcija = sqlite3.connect("biblioteka_api.db", check_same_thread=False)
kursor = konekcija.cursor()

kursor.execute("""
    CREATE TABLE IF NOT EXISTS korisnici (
        id INTEGER PRIMARY KEY,
        korisnicko_ime TEXT UNIQUE,
        lozinka_hash TEXT
    )
""")
konekcija.commit()

kursor.execute("""
    CREATE TABLE IF NOT EXISTS knjige (
        id INTEGER PRIMARY KEY,
        naslov TEXT,
        godina INTEGER,
        ocjena INTEGER
    )
""")
konekcija.commit()

