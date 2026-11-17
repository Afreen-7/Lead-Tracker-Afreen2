
from database import Database

db = Database()

connection = db.connect()

cursor = connection.cursor()

cursor.execute("SELECT current_database();")

result = cursor.fetchone()

print("Connected database:", result[0])

cursor.close()
connection.close()