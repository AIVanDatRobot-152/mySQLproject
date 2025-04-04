import mysql.connector

# Kết nối tới cơ sở dữ liệu MySQL
mydb = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="SQLdat1502:3",
    database="banana_data"
)

mycursor = mydb.cursor()

# Hàm truy vấn dữ liệu
def data():
    while True:
        inp = input("Nhập ID cần truy vấn (hoặc nhấn Enter để thoát): ")

        if inp == '':
            break

        try:
            input_id = int(inp)

            # Truy vấn thông tin từ bảng hoa_lan
            query = "SELECT Size, Weight, Sweetness, Softness, HarvestTime, Ripeness, Acidity, Quality FROM banana WHERE ID = %s"
            mycursor.execute(query, (input_id,))
            result = mycursor.fetchone()

            if result:
                # Giải nén kết quả từ truy vấn
                Size, Weight, Sweetness, Softness, HarvestTime, Ripeness, Acidity, Quality = result
                print(f"Thông tin về quả chuối:")
                print(f"Kích thước: {Size}")
                print(f"Khối lượng: {Weight}")
                print(f"Độ ngọt: {Sweetness}")
                print(f"Độ mềm: {Softness}")
                print(f"Thời gian thu hoạch: {HarvestTime}")
                print(f"Độ chín: {Ripeness}")
                print(f"Độ chua: {Acidity}")
                print(f"Chất lượng: {Quality}")
            else:
                print(f"Không tìm thấy cây chuối có ID {input_id}")
        except ValueError:
            print("Vui lòng nhập một số nguyên hợp lệ cho ID.")
        except mysql.connector.Error as err:
            print(f"Lỗi khi truy vấn: {err}")

# Bắt đầu chương trình
data()

# Đóng kết nối sau khi kết thúc
mydb.close()