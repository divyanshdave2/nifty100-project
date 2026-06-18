import sqlite3

conn = sqlite3.connect("database/nifty100.db")

print("Database Created Successfully")

conn.close()