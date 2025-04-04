import mysql.connector

# Kết nối tới cơ sở dữ liệu MySQL
mydb = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="SQLdat1502:3",
    database="new_database"
)

mycursor = mydb.cursor()

# Hàm truy vấn dữ liệu
def data():
    while True:
        inp = input("Nhập ID hoa lan cần truy vấn (hoặc nhấn Enter để thoát): ")

        if inp == '':
            break

        try:
            input_id = int(inp)

            # Truy vấn thông tin từ bảng hoa_lan
            query = "SELECT Nameflower, Color, Size, Origin, notes FROM hoa_lan WHERE ID = %s"
            mycursor.execute(query, (input_id,))
            result = mycursor.fetchone()

            if result:
                # Giải nén kết quả từ truy vấn
                tenhoalan, mausac, size, suatxu, notes = result
                print(f"Thông tin về {tenhoalan}:")
                print(f"Màu sắc: {mausac}")
                print(f"Kích thước: {size}")
                print(f"Xuất xứ: {suatxu}")
                print(f"Ghi chú: {notes}")
            else:
                print(f"Không tìm thấy loài hoa lan có ID {input_id}")
        except ValueError:
            print("Vui lòng nhập một số nguyên hợp lệ cho ID.")
        except mysql.connector.Error as err:
            print(f"Lỗi khi truy vấn: {err}")

# Bắt đầu chương trình
data()

# Đóng kết nối sau khi kết thúc
mydb.close()