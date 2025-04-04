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

# Thực hiện truy vấn để lấy tất cả dữ liệu từ bảng robots_manager
query = "SELECT RobotID, RobotName, Tasks FROM mushrooms_data.robots_manager"
cursor.execute(query)

# Lấy tất cả các dòng dữ liệu từ bảng
rows = cursor.fetchall()

# Danh sách chứa dữ liệu đã chuẩn hóa
normalized_data = []

# Duyệt qua các hàng dữ liệu
for row in rows:
    RobotID, RobotName, Tasks = row
    # Tách các nhiệm vụ (Tasks) dựa trên dấu phẩy
    task_list = Tasks.split(', ')
    # Tạo từng hàng dữ liệu cho mỗi nhiệm vụ
    for task in task_list:
        normalized_data.append((RobotID, RobotName, task))

# Hiển thị dữ liệu đã chuẩn hóa
print(f"| RobotID | RobotName | Task |")
print("-" * 50)

# In dữ liệu đã chuẩn hóa
for data in normalized_data:
    print(f"| {data[0]} | {data[1]} | {data[2]} |")

# Đóng cursor và kết nối sau khi hoàn thành
cursor.close()
conn.close()
