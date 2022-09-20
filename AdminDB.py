import sqlite3  
  
con = sqlite3.connect("admin.db")  
print("Database opened successfully")  
  
con.execute("create table Admin (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, email TEXT UNIQUE NOT NULL, password TEXT NOT NULL)")  
  
print("Table created successfully")  
  
con.close()  