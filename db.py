import pyodbc

conn = pyodbc.connect(
    "DRIVER={SQL Server};"
    "SERVER=MANYAMOULYA\\SQLEXPRESS;"
    "DATABASE=BankingSystem;"
    "Trusted_Connection=yes;"
)

cursor = conn.cursor()

print("Connected successfully!")