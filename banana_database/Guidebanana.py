import mysql.connector
import tkinter as tk
from tkinter import ttk, messagebox

# Hàm để kết nối và truy vấn cơ sở dữ liệu
def get_data_from_db(input_id):
    try:
        # Kết nối tới cơ sở dữ liệu MySQL
        mydb = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password="SQLdat1502:3",
            database="banana_data"
        )

        mycursor = mydb.cursor()
        # Truy vấn thông tin từ bảng banana
        query = "SELECT Size, Weight, Sweetness, Softness, HarvestTime, Ripeness, Acidity, Quality FROM banana WHERE ID = %s"
        mycursor.execute(query, (input_id,))
        result = mycursor.fetchone()
        mydb.close()

        return result
    except mysql.connector.Error as err:
        messagebox.showerror("Lỗi", f"Lỗi khi truy vấn: {err}")
        return None

# Hàm để hiển thị dữ liệu trong giao diện
def show_data():
    input_id = entry_id.get()

    if not input_id.isdigit():
        messagebox.showerror("Lỗi", "Vui lòng nhập một số nguyên hợp lệ cho ID.")
        return

    result = get_data_from_db(int(input_id))
    if result:
        # Giải nén kết quả từ truy vấn
        Size, Weight, Sweetness, Softness, HarvestTime, Ripeness, Acidity, Quality = result
        label_result.config(text=f"Thông tin về quả chuối có ID {input_id}:\n"
                                 f"Kích thước: {Size}\n"
                                 f"Khối lượng: {Weight}\n"
                                 f"Độ ngọt: {Sweetness}\n"
                                 f"Độ mềm: {Softness}\n"
                                 f"Thời gian thu hoạch: {HarvestTime}\n"
                                 f"Độ chín: {Ripeness}\n"
                                 f"Độ chua: {Acidity}\n"
                                 f"Chất lượng: {Quality}")
    else:
        label_result.config(text=f"Không tìm thấy quả chuối có ID {input_id}")

# Tạo giao diện Tkinter
root = tk.Tk()
root.title("Truy vấn Quả Chuối")
root.geometry("500x400")

# Tạo màu nền và tiêu đề cho giao diện
root.configure(bg="#e1f5fe")  # Màu nền nhẹ nhàng
title_label = tk.Label(root, text="Truy vấn thông tin Quả Chuối", font=("Arial", 20, "bold"), bg="#0288d1", fg="white")
title_label.pack(pady=10)

# Tạo nhãn và ô nhập liệu cho ID
label_id = tk.Label(root, text="Nhập ID của cây chuối:", font=("Arial", 12), bg="#e1f5fe")
label_id.pack(pady=10)
entry_id = tk.Entry(root, font=("Arial", 12))
entry_id.pack(pady=5)

# Tạo nút để truy vấn dữ liệu
button = tk.Button(root, text="Truy vấn", font=("Arial", 12, "bold"), bg="#4caf50", fg="white", command=show_data)
button.pack(pady=10)

# Tạo nhãn để hiển thị kết quả truy vấn
label_result = tk.Label(root, text="", font=("Arial", 12), bg="#e1f5fe", justify="left")
label_result.pack(pady=10)

# Chạy vòng lặp giao diện
root.mainloop()
