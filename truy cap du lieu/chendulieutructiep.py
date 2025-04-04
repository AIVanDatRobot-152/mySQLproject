import mysql.connector

def them_du_lieu_moi():
    koi_id = int(input("Nhập ID của cá Koi: "))
    name = input("Nhập tên của cá Koi: ")
    color = input("Nhập màu của cá Koi: ")
    size = float(input("Nhập kích thước của cá Koi: "))
    birth_date = input("Nhập ngày sinh của cá Koi (YYYY-MM-DD): ")
    gender = input("Nhập giới tính của cá Koi (Male, Female, Unknown): ")
    health_status = input("Nhập tình trạng sức khỏe của cá Koi (Healthy, Sick, Recovering): ")
    origin = input("Nhập nguồn gốc của cá Koi: ")
    notes = input("Nhập ghi chú: ")
    return (koi_id, name, color, size, birth_date, gender, health_status, origin, notes)

mydb = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="SQLdat1502:3",
    database="new_database"
)

mycursor = mydb.cursor()

# Gọi hàm để lấy dữ liệu mới
val = them_du_lieu_moi()

sql = "INSERT INTO koi (koi_id, name, color, size, birth_date, gender, health_status, origin, notes) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
mycursor.execute(sql, val)
mydb.commit()

mycursor.execute("SELECT * FROM koi")

for row in mycursor:
    stt = row[1]
    print(row)

mydb.close()