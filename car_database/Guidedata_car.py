import mysql.connector
import tkinter as tk
from tkinter import messagebox

# Kết nối tới cơ sở dữ liệu MySQL
mydb = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="SQLdat1502:3",
    database="banana_data"
)

mycursor = mydb.cursor()

# Hàm để truy vấn và hiển thị dữ liệu
def show_data():
    input_id = entry_id.get()

    if not input_id.isdigit():
        messagebox.showerror("Lỗi", "Vui lòng nhập một số nguyên hợp lệ cho ID.")
        return

    try:
        query = """SELECT Make, Model, Generation, YearFromGeneration, YearToGeneration, Serie, Trim 
                   FROM car_database WHERE idtrim = %s"""
        mycursor.execute(query, (input_id,))
        result = mycursor.fetchone()

        if result:
            # Giải nén kết quả từ truy vấn
            Make, Model, Generation, YearFromGeneration, YearToGeneration, Serie, Trim = result
            # Hiển thị thông tin
            lbl_make.config(text=f"Hãng xe: {Make}", bg="#e6f7ff")
            lbl_model.config(text=f"Mẫu xe: {Model}", bg="#ccf2ff")
            lbl_generation.config(text=f"Thế hệ: {Generation}", bg="#99ebff")
            lbl_year_from.config(text=f"Năm sản xuất từ: {YearFromGeneration}", bg="#66e0ff")
            lbl_year_to.config(text=f"Năm sản xuất đến: {YearToGeneration}", bg="#33d6ff")
            lbl_serie.config(text=f"Dòng xe: {Serie}", bg="#00ccff")
            lbl_trim.config(text=f"Phiên bản: {Trim}", bg="#00bfff")
        else:
            messagebox.showinfo("Thông báo", f"Không tìm thấy xe có ID {input_id}")

    except mysql.connector.Error as err:
        messagebox.showerror("Lỗi khi truy vấn", f"Lỗi: {err}")

# Giao diện
root = tk.Tk()
root.title("Thông tin Xe")
root.geometry("400x400")

# Nhập ID xe
label = tk.Label(root, text="Nhập ID Xe:", font=('Arial', 12))
label.pack(pady=10)
entry_id = tk.Entry(root, font=('Arial', 12))
entry_id.pack(pady=5)

# Nút truy vấn
btn_query = tk.Button(root, text="Truy vấn", command=show_data, font=('Arial', 12), bg='#00bfff', fg='white')
btn_query.pack(pady=10)

# Hiển thị thông tin
lbl_make = tk.Label(root, text="", font=('Arial', 12))
lbl_make.pack(pady=5)
lbl_model = tk.Label(root, text="", font=('Arial', 12))
lbl_model.pack(pady=5)
lbl_generation = tk.Label(root, text="", font=('Arial', 12))
lbl_generation.pack(pady=5)
lbl_year_from = tk.Label(root, text="", font=('Arial', 12))
lbl_year_from.pack(pady=5)
lbl_year_to = tk.Label(root, text="", font=('Arial', 12))
lbl_year_to.pack(pady=5)
lbl_serie = tk.Label(root, text="", font=('Arial', 12))
lbl_serie.pack(pady=5)
lbl_trim = tk.Label(root, text="", font=('Arial', 12))
lbl_trim.pack(pady=5)

# Chạy giao diện
root.mainloop()

# Đóng kết nối sau khi kết thúc
mydb.close()
