import mysql.connector

# Kết nối tới cơ sở dữ liệu MySQL
conn = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="SQLdat1502:3",
    database="imager_data"  # Tên cơ sở dữ liệu
)
    
cursor = conn.cursor()

# Mở file ảnh và đọc dữ liệu nhị phân (binary)
with open('dandandan.mp4', 'rb') as file:
    binary_data = file.read()
# Truy vấn chèn dữ liệu vào bảng
sql = """
INSERT INTO video_data (Video_Id, Video_name, Video_data, Description_Video) 
VALUES (%s, %s, %s, %s)
"""

# Thực thi truy vấn với dữ liệu cụ thể
cursor.execute(sql, (2, 'Dandandan', binary_data, 'Dandandan OP'))

# Lưu thay đổi vào cơ sở dữ liệu
conn.commit()

# Đóng cursor và kết nối
cursor.close()
conn.close()

print("Video đã được chèn thành công!")
