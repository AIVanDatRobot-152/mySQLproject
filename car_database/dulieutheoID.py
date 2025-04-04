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
        inp = input("Nhập ID Xe cần truy vấn (hoặc nhấn Enter để thoát): ")

        if inp == '':
            break

        try:
            input_id = int(inp)

            # Truy vấn thông tin từ bảng car_database
            query = """ SELECT Make, Model, Generation, YearFromGeneration, YearToGeneration, Serie, Trim FROM car_database WHERE idtrim = %s"""
            mycursor.execute(query, (input_id,))
            result = mycursor.fetchone()

            if result:
                # Giải nén kết quả từ truy vấn
                Make, Model, Generation, YearFromGeneration, YearToGeneration, Serie, Trim = result
                print(f"Hãng xe: {Make}")
                print(f"Mẫu xe: {Model}")
                print(f"Thế hệ: {Generation}")
                print(f"Năm sản xuất từ: {YearFromGeneration}")
                print(f"Năm sản xuất đến: {YearToGeneration}")
                print(f"Dòng xe: {Serie}")
                print(f"Phiên bản: {Trim}")
            else:
                print(f"Không tìm thấy xe có ID {input_id}")
        except ValueError:
            print("Vui lòng nhập một số nguyên hợp lệ cho ID.")
        except mysql.connector.Error as err:
            print(f"Lỗi khi truy vấn: {err}")

# Bắt đầu chương trình
data()

# Đóng kết nối sau khi kết thúc
mydb.close()
