import mysql.connector

# Kết nối tới cơ sở dữ liệu MySQL
conn = mysql.connector.connect(
    host="127.0.0.1",        # Địa chỉ máy chủ MySQL (hoặc IP của máy chủ MySQL)
    user="root",             # Tên đăng nhập MySQL
    password="SQLdat1502:3",   # Mật khẩu MySQL
    database="kiemtralan2"   # Tên cơ sở dữ liệu
)

# Tạo đối tượng cursor để thực thi các truy vấn
cursor = conn.cursor()

# Truy vấn chỉ các cột Movie_Id, Movie_name và Director, bỏ qua cột file_path
query = "SELECT Movie_Id, Movie_name, Director, file_path FROM kiemtralan2.movies"
cursor.execute(query)

# Lấy tất cả các dòng dữ liệu từ bảng
rows = cursor.fetchall()

# Lấy tiêu đề của bảng (tên các cột)
column_names = [i[0] for i in cursor.description]

# Hiển thị tiêu đề của bảng
print(f"| {' | '.join(column_names)} |")
print("-" * 50)

# Hiển thị các dòng dữ liệu
for row in rows:
    print(f"| {' | '.join(str(value) for value in row)} |")

# Đóng cursor và kết nối sau khi hoàn thành
cursor.close()
conn.close()
