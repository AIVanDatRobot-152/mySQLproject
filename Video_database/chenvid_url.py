import mysql.connector

# Kết nối tới cơ sở dữ liệu MySQL
conn = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="SQLdat1502:3",
    database="imager_data"  # Tên cơ sở dữ liệu
)

cursor = conn.cursor()

# Thay thế phần đọc file video bằng URL video
video_url = 'https://www.youtube.com/watch?v=gFQZgwMC1As'  # Thay đổi URL tại đây

# Truy vấn chèn dữ liệu vào bảng
sql = """
INSERT INTO video_data (Video_Id, Video_name, Video_data, Description_Video) 
VALUES (%s, %s, %s, %s)
"""

# Thực thi truy vấn với dữ liệu cụ thể, lưu URL thay vì dữ liệu nhị phân
cursor.execute(sql, (3, 'Bleach', video_url, 'Bleach OP'))

# Lưu thay đổi vào cơ sở dữ liệu
conn.commit()

# Đóng cursor và kết nối
cursor.close()
conn.close()

print("Video URL đã được chèn thành công!")
