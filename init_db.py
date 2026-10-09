import sqlite3

conn = sqlite3.connect("restraunt.db")

cursor = conn.cursor()

cursor.executescript("CREATE TABLE users (id TEXT, name VARCHAR(50), password VARCHAR(50), role VARCHAR(10));")
cursor.executescript("CREATE TABLE orders (id TEXT, name VARCHAR(50));")
cursor.executescript("CREATE TABLE sessions (token TEXT(50), userid TEXT);")

conn.commit
conn.close()

