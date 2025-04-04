import mysql.connector

# Kết nối tới cơ sở dữ liệu MySQL
conn = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="SQLdat1502:3",
    database="fruits_database"
)

# Tạo đối tượng cursor để thực thi các truy vấn
cursor = conn.cursor()

# Tạo bảng mới cho FruitTypes
create_types_table_query = """
CREATE TABLE IF NOT EXISTS FruitTypes (
    CommonName VARCHAR(255) PRIMARY KEY,
    ScientificName VARCHAR(255)
)
"""
cursor.execute(create_types_table_query)

# Tạo bảng mới cho Fruits
create_fruits_table_query = """
CREATE TABLE IF NOT EXISTS Fruits (
    FruitID VARCHAR(10) PRIMARY KEY,
    CommonName VARCHAR(255),
    FOREIGN KEY (CommonName) REFERENCES FruitTypes(CommonName)
)
"""
cursor.execute(create_fruits_table_query)

# Tạo bảng mới cho FruitAttributes
create_attributes_table_query = """
CREATE TABLE IF NOT EXISTS FruitAttributes (
    FruitID VARCHAR(10),
    Color VARCHAR(50),
    Taste VARCHAR(50),
    FOREIGN KEY (FruitID) REFERENCES Fruits(FruitID)
)
"""
cursor.execute(create_attributes_table_query)

# Truy vấn dữ liệu từ bảng gốc
query = "SELECT FruitID, CommonName, ScientificName, Color, Taste FROM fruits_database.fruits_data"
cursor.execute(query)

# Lấy tất cả các dòng dữ liệu từ bảng
rows = cursor.fetchall()

# Chuẩn hóa dữ liệu và chèn vào bảng mới
for row in rows:
    FruitID, CommonName, ScientificName, Color, Taste = row
    
    # Chèn vào bảng FruitTypes nếu chưa tồn tại
    insert_type_query = """
    INSERT INTO FruitTypes (CommonName, ScientificName) 
    VALUES (%s, %s) 
    ON DUPLICATE KEY UPDATE ScientificName = VALUES(ScientificName)
    """
    cursor.execute(insert_type_query, (CommonName, ScientificName))
    
    # Chèn vào bảng Fruits nếu chưa tồn tại
    insert_fruit_query = """
    INSERT INTO Fruits (FruitID, CommonName) 
    VALUES (%s, %s) 
    ON DUPLICATE KEY UPDATE CommonName = VALUES(CommonName)
    """
    cursor.execute(insert_fruit_query, (FruitID, CommonName))
    
    # Chèn vào bảng FruitAttributes nếu chưa tồn tại
    insert_attributes_query = """
    INSERT INTO FruitAttributes (FruitID, Color, Taste) 
    VALUES (%s, %s, %s) 
    ON DUPLICATE KEY UPDATE Color = VALUES(Color), Taste = VALUES(Taste)
    """
    cursor.execute(insert_attributes_query, (FruitID, Color, Taste))

# Lưu thay đổi vào cơ sở dữ liệu
conn.commit()

# Hiển thị dữ liệu đã chèn
print("FruitTypes Table:")
cursor.execute("SELECT * FROM FruitTypes")
types_rows = cursor.fetchall()
for type_row in types_rows:
    print(type_row)

print("\nFruits Table:")
cursor.execute("SELECT * FROM Fruits")
fruits_rows = cursor.fetchall()
for fruit in fruits_rows:
    print(fruit)

print("\nFruitAttributes Table:")
cursor.execute("SELECT * FROM FruitAttributes")
attributes_rows = cursor.fetchall()
for attribute in attributes_rows:
    print(attribute)

# Đóng cursor và kết nối sau khi hoàn thành
cursor.close()
conn.close()
