import mysql.connector

# Kết nối tới cơ sở dữ liệu MySQL
conn = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="SQLdat1502:3",
    database="orchid_database"
)

# Tạo đối tượng cursor để thực thi các truy vấn
cursor = conn.cursor()

# Tạo bảng mới cho màu sắc
create_colors_table = """
CREATE TABLE IF NOT EXISTS colors (
    ColorID INT AUTO_INCREMENT PRIMARY KEY,
    Color VARCHAR(50) UNIQUE
)
"""
cursor.execute(create_colors_table)

# Tạo bảng mới cho kích thước
create_sizes_table = """
CREATE TABLE IF NOT EXISTS sizes (
    SizeID INT AUTO_INCREMENT PRIMARY KEY,
    Size VARCHAR(50) UNIQUE
)
"""
cursor.execute(create_sizes_table)

# Tạo bảng mới cho hoa lan
create_orchids_table = """
CREATE TABLE IF NOT EXISTS orchids (
    OrchidID INT PRIMARY KEY,
    Name VARCHAR(50),
    ColorID INT,
    SizeID INT,
    FOREIGN KEY (ColorID) REFERENCES colors(ColorID),
    FOREIGN KEY (SizeID) REFERENCES sizes(SizeID)
)
"""
cursor.execute(create_orchids_table)

# Dữ liệu gốc từ bảng
orchids_data = [
    (1, "Orchid 1", "Yellow", "Medium"),
    (2, "Orchid 2", "White", "Small"),
    (3, "Orchid 3", "Pink", "Medium"),
    (4, "Orchid 4", "Red", "Medium"),
    (5, "Orchid 5", "Pink", "Large"),
    (6, "Orchid 6", "Blue", "Medium"),
    (7, "Orchid 7", "Pink", "Large"),
    # Thêm các hàng khác nếu cần
]

# Chèn dữ liệu màu sắc và kích thước vào bảng tương ứng
for color in set(row[2] for row in orchids_data):  # Lấy danh sách màu sắc duy nhất
    cursor.execute("INSERT IGNORE INTO colors (Color) VALUES (%s)", (color,))

for size in set(row[3] for row in orchids_data):  # Lấy danh sách kích thước duy nhất
    cursor.execute("INSERT IGNORE INTO sizes (Size) VALUES (%s)", (size,))

# Lưu thay đổi vào cơ sở dữ liệu
conn.commit()

# Chèn dữ liệu vào bảng orchids
for orchid in orchids_data:
    cursor.execute("""
    INSERT INTO orchids (OrchidID, Name, ColorID, SizeID) 
    VALUES (%s, %s, (SELECT ColorID FROM colors WHERE Color = %s), (SELECT SizeID FROM sizes WHERE Size = %s))
    ON DUPLICATE KEY UPDATE Name = VALUES(Name)
    """, (orchid[0], orchid[1], orchid[2], orchid[3]))

# Lưu thay đổi vào cơ sở dữ liệu
conn.commit()

# Truy vấn và hiển thị dữ liệu từ bảng orchids
query = """
SELECT o.OrchidID, o.Name, c.Color, s.Size
FROM orchids o
JOIN colors c ON o.ColorID = c.ColorID
JOIN sizes s ON o.SizeID = s.SizeID
"""
cursor.execute(query)

# Lấy tất cả các dòng dữ liệu từ truy vấn
rows = cursor.fetchall()

# Lấy tiêu đề của bảng (tên các cột)
column_names = [i[0] for i in cursor.description]

# Hiển thị tiêu đề của bảng
print(f"| {' | '.join(column_names)} |")
print("-" * 50)

# Hiển thị các dòng dữ liệu
for row in rows:
    print(f"| {' | '.join(str(value) for value in row)} |")

# Đóng cursor và kết nối
cursor.close()
conn.close()
