import sqlite3
from hashlib import sha256
import os

# Verbinding maken met de database (deze wordt aangemaakt als deze niet bestaat)
conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# Maak een tabel om gebruikersinformatie op te slaan
cursor.execute('''
    CREATE TABLE IF NOT EXISTS gebruikers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        gebruikersnaam TEXT NOT NULL ,
        wachtwoord_salt TEXT NOT NULL,
        wachtwoord_hash TEXT NOT NULL,
        rol TEXT NOT NULL
    )
''')
conn.close()