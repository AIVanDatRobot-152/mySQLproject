import mysql.connector
import random

# Kết nối tới cơ sở dữ liệu MySQL
conn = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="SQLdat1502:3",
    database="orchid_database"  # Đổi tên nếu cần thiết
)

# Tạo đối tượng cursor để thực thi các truy vấn
cursor = conn.cursor()

# Tạo bảng cho hoa lan chưa chuẩn hóa (1NF)
create_table_query_1NF = """
CREATE TABLE IF NOT EXISTS orchids_1NF (
    OrchidID INT PRIMARY KEY AUTO_INCREMENT,
    Name VARCHAR(255),
    Properties_1NF VARCHAR(255)
)
"""
cursor.execute(create_table_query_1NF)

# Tạo bảng cho hoa lan chuẩn hóa 2NF
create_table_query_2NF = """
CREATE TABLE IF NOT EXISTS orchids_2NF (
    OrchidID INT PRIMARY KEY AUTO_INCREMENT,
    Name VARCHAR(255),
    Color VARCHAR(50),
    Size VARCHAR(50)
)
"""
cursor.execute(create_table_query_2NF)

# Tạo bảng cho hoa lan chuẩn hóa 3NF
create_table_query_3NF = """
CREATE TABLE IF NOT EXISTS orchids_3NF (
    OrchidID INT PRIMARY KEY AUTO_INCREMENT,
    Name VARCHAR(255),
    Color VARCHAR(50),
    Size VARCHAR(50),
    Fragrance VARCHAR(50)
)
"""
cursor.execute(create_table_query_3NF)

# Tạo dữ liệu mẫu cho các loại hoa lan
for i in range(1, 101):
    # Tạo tên hoa lan
    orchid_name = f"Orchid {i}"
    
    # Tạo các đặc tính (3 đặc tính)
    colors = ['Red', 'Blue', 'Yellow', 'Green', 'Pink', 'White', 'Purple']
    sizes = ['Small', 'Medium', 'Large']
    fragrances = ['Sweet', 'Strong', 'Faint', 'No fragrance']
    
    # Chọn ngẫu nhiên các đặc tính cho hoa lan
    color = random.choice(colors)
    size = random.choice(sizes)
    fragrance = random.choice(fragrances)
    
    # Chèn vào bảng chưa chuẩn hóa (1NF)
    properties_1NF = f"{color}, {size}, {fragrance}"
    cursor.execute("INSERT INTO orchids_1NF (Name, Properties_1NF) VALUES (%s, %s)", (orchid_name, properties_1NF))

    # Chèn vào bảng chuẩn hóa 2NF
    cursor.execute("INSERT INTO orchids_2NF (Name, Color, Size) VALUES (%s, %s, %s)", (orchid_name, color, size))

    # Chèn vào bảng chuẩn hóa 3NF
    cursor.execute("INSERT INTO orchids_3NF (Name, Color, Size, Fragrance) VALUES (%s, %s, %s, %s)", (orchid_name, color, size, fragrance))

# Lưu thay đổi vào cơ sở dữ liệu
conn.commit()

# Đóng cursor và kết nối sau khi hoàn thành
cursor.close()
conn.close()

print("Dữ liệu hoa lan đã được chèn thành công vào cơ sở dữ liệu MySQL.")
