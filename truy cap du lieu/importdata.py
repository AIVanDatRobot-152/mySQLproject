import mysql.connector

mydb = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="SQLdat1502:3",
    database="new_database"
)

mycursor = mydb.cursor()
sql = "INSERT INTO koi (koi_id, name, color, size, birth_date, gender, health_status, origin, notes) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
val = (5, "Koi E", "nau", 26.40, "2023-11-05", "Male", "Sick", "Uc", "Cum dep")
mycursor.execute(sql, val)
mydb.commit()

mycursor.execute("SELECT * FROM koi")

for row in mycursor:
    stt = row[1]
    print(row)

mydb.close()