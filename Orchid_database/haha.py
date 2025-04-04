import mysql.connector

# Kết nối tới cơ sở dữ liệu MySQL
conn = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="SQLdat1502:3",
    database="orchid_database"  # Thay bằng tên cơ sở dữ liệu của bạn
)

# Tạo đối tượng cursor để thực thi các truy vấn
cursor = conn.cursor()

# Tạo bảng orchids
create_table_query = """
CREATE TABLE IF NOT EXISTS orchidssss (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255),
    color VARCHAR(100),
    size VARCHAR(100),
    bloom_season VARCHAR(100),
    height VARCHAR(100),
    watering VARCHAR(100),
    type VARCHAR(100)
)
"""

cursor.execute(create_table_query)

# Đóng cursor và kết nối
cursor.close()
conn.close()
