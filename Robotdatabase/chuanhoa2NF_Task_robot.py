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

# Tạo bảng RobotsEND
create_robots_table_query = """
CREATE TABLE IF NOT EXISTS RobotsEND (
    RobotID VARCHAR(10) PRIMARY KEY,
    RobotType VARCHAR(50)
)
"""
cursor.execute(create_robots_table_query)

# Tạo bảng TasksEnd
create_tasks_table_query = """
CREATE TABLE IF NOT EXISTS TasksEnd (
    TaskID VARCHAR(50) PRIMARY KEY,
    TaskDescription VARCHAR(50)
)
"""
cursor.execute(create_tasks_table_query)

# Tạo bảng robot_tasks để liên kết giữa RobotsEND và TasksEnd
create_robot_tasks_table_query = """
CREATE TABLE IF NOT EXISTS robot_tasks (
    RobotID VARCHAR(10),
    TaskID VARCHAR(50),
    PRIMARY KEY (RobotID, TaskID),
    FOREIGN KEY (RobotID) REFERENCES RobotsEND(RobotID),
    FOREIGN KEY (TaskID) REFERENCES TasksEnd(TaskID)
)
"""
cursor.execute(create_robot_tasks_table_query)

# Thực hiện truy vấn để lấy tất cả dữ liệu từ bảng tasks_robot
query = "SELECT * FROM mushrooms_data.tasks_robot"
cursor.execute(query)

# Lấy tất cả các dòng dữ liệu từ bảng
rows = cursor.fetchall()

# Chuẩn hóa dữ liệu
for row in rows:
    RobotID, TaskID, RobotType, TaskDescription = row

    # Chèn thông tin vào bảng RobotsEND
    cursor.execute("INSERT IGNORE INTO RobotsEND (RobotID, RobotType) VALUES (%s, %s)", (RobotID, RobotType))
    
    # Chèn thông tin vào bảng TasksEnd
    cursor.execute("INSERT IGNORE INTO TasksEnd (TaskID, TaskDescription) VALUES (%s, %s)", (TaskID, TaskDescription))
    
    # Chèn thông tin vào bảng robot_tasks để liên kết giữa RobotsEND và TasksEnd
    cursor.execute("INSERT IGNORE INTO robot_tasks (RobotID, TaskID) VALUES (%s, %s)", (RobotID, TaskID))

# Lưu thay đổi vào cơ sở dữ liệu
conn.commit()

# Hiển thị dữ liệu từ các bảng mới
print("Bảng RobotsEND:")
cursor.execute("SELECT * FROM RobotsEND")
for row in cursor.fetchall():
    print(row)

print("\nBảng TasksEnd:")
cursor.execute("SELECT * FROM TasksEnd")
for row in cursor.fetchall():
    print(row)

print("\nBảng robot_tasks:")
cursor.execute("SELECT * FROM robot_tasks")
for row in cursor.fetchall():
    print(row)

# Đóng cursor và kết nối sau khi hoàn thành
cursor.close()
conn.close()
