import sqlite3  
  
con = sqlite3.connect("employee.db")  
print("Database opened successfully")  
  
con.execute("create table emp (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, contact INTEGER NOT NULL, email TEXT UNIQUE NOT NULL, salary INTEGER NOT NULL)")  
  
print("Table created successfully")  
  
con.close()  