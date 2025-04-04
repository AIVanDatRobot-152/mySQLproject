import mysql.connector

# Kết nối tới cơ sở dữ liệu MySQL
conn = mysql.connector.connect(
    host="127.0.0.1",        # Địa chỉ máy chủ MySQL
    user="root",             # Tên đăng nhập MySQL
    password="SQLdat1502:3",   # Mật khẩu MySQL
    database="orchid_database"  # Tên cơ sở dữ liệu
)

# Tạo đối tượng cursor để thực thi các truy vấn
cursor = conn.cursor()

# Tạo bảng mới để lưu dữ liệu chuẩn hóa 1NF
create_table_query = """
CREATE TABLE IF NOT EXISTS orchid_1nf_normalized (
    OrchidID INT PRIMARY KEY,
    Name VARCHAR(255),
    Color VARCHAR(50),
    Size VARCHAR(50),
    Fragrance VARCHAR(50)
)
"""
cursor.execute(create_table_query)

# Thực hiện truy vấn để lấy tất cả dữ liệu từ bảng orchids_1nf
query = "SELECT * FROM orchids_1nf"
cursor.execute(query)

# Lấy tất cả các dòng dữ liệu từ bảng
rows = cursor.fetchall()

# Chuẩn hóa dữ liệu và chèn vào bảng mới
for row in rows:
    OrchidID, Name, Properties_1NF = row
    
    # Tách các đặc tính
    properties = Properties_1NF.split(", ")
    
    # Đảm bảo số lượng thuộc tính là 3 (Color, Size, Fragrance)
    if len(properties) == 3:
        color, size, fragrance = properties
        insert_query = "INSERT INTO orchid_1nf_normalized (OrchidID, Name, Color, Size, Fragrance) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(insert_query, (OrchidID, Name, color, size, fragrance))
    else:
        print(f"Lỗi: Số lượng thuộc tính không đúng cho OrchidID {OrchidID}")

# Lưu thay đổi vào cơ sở dữ liệu
conn.commit()

# Hiển thị dữ liệu đã chèn
cursor.execute("SELECT * FROM orchid_1nf_normalized")
normalized_rows = cursor.fetchall()

# Hiển thị tiêu đề của bảng
column_names = ["OrchidID", "Name", "Color", "Size", "Fragrance"]
print(f"| {' | '.join(column_names)} |")
print("-" * 50)

# Hiển thị các dòng dữ liệu
for row in normalized_rows:
    print(f"| {' | '.join(str(value) for value in row)} |")

# Đóng cursor và kết nối sau khi hoàn thành
cursor.close()
conn.close()
