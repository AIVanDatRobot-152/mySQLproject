import mysql.connector
mydb = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="SQLdat1502:3",
    database="new_database"
)
mycursor = mydb.cursor()
sql = "INSERT INTO robot_list (id, name) VALUES (%s, %s)"
val = (9," Micromouse",)
mycursor.execute(sql, val)
mydb.commit()
mycursor.execute("SELECT * FROM new_database.robot_list")

for row in mycursor:
    stt = row[1]
    print(row)

mydb.close()