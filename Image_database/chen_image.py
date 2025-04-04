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
with open('Corgi.jpg', 'rb') as file:
    binary_data = file.read()
# Truy vấn chèn dữ liệu vào bảng
sql = """
INSERT INTO image_data (Image_Id, Image_name, Image_data, Description_image) 
VALUES (%s, %s, %s, %s)
"""

# Thực thi truy vấn với dữ liệu cụ thể
cursor.execute(sql, (4, 'Corgi', binary_data, 'Chó Corgi'))

# Lưu thay đổi vào cơ sở dữ liệu
conn.commit()

# Đóng cursor và kết nối
cursor.close()
conn.close()

print("Hình ảnh đã được chèn thành công!")
