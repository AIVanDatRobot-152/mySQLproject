import mysql.connector

# Kết nối tới cơ sở dữ liệu MySQL
conn = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="SQLdat1502:3",
    database="mushrooms_data"
)

# Tạo đối tượng cursor để thực thi các truy vấn
cursor = conn.cursor()

# Kiểm tra và thêm cột MaintenanceDates nếu không tồn tại
try:
    cursor.execute("ALTER TABLE dates_robot ADD COLUMN MaintenanceDates VARCHAR(255)")
except mysql.connector.Error as err:
    if err.errno == mysql.connector.errorcode.ER_DUP_FIELDNAME:
        print("Cột MaintenanceDates đã tồn tại.")
    else:
        print(f"Lỗi khi thêm cột: {err}")

# Tạo bảng mới để lưu dữ liệu chuẩn hóa
create_table_query = """
CREATE TABLE IF NOT EXISTS dates_robot_normalizedz (
    RobotID VARCHAR(10),
    RobotName VARCHAR(255),
    MaintenanceDates VARCHAR(255)
)
"""
cursor.execute(create_table_query)

# Truy vấn dữ liệu từ bảng gốc
query = "SELECT RobotID, RobotName, MaintenanceDates FROM dates_robot"
cursor.execute(query)

# Lấy tất cả các dòng dữ liệu từ bảng
rows = cursor.fetchall()

# Chuẩn hóa dữ liệu và chèn vào bảng mới
for row in rows:
    RobotID, RobotName, MaintenanceDates = row
    # Tách các ngày (MaintenanceDates) thành danh sách
    MaintenanceDates_list = MaintenanceDates.split(', ')
    
    # Chèn từng ngày vào bảng mới
    for date in MaintenanceDates_list:
        insert_query = "INSERT INTO dates_robot_normalizedz (RobotID, RobotName, MaintenanceDates) VALUES (%s, %s, %s)"
        cursor.execute(insert_query, (RobotID, RobotName, date))

# Lưu thay đổi vào cơ sở dữ liệu
conn.commit()

# Hiển thị dữ liệu đã chèn
cursor.execute("SELECT * FROM dates_robot_normalizedz")
normalized_rows = cursor.fetchall()
print(f"| RobotID | RobotName | MaintenanceDates |")
print("-" * 50)
for row in normalized_rows:
    print(f"| {row[0]} | {row[1]} | {row[2]} |")

# Đóng cursor và kết nối sau khi hoàn thành
cursor.close()
conn.close()
