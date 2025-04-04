import tkinter as tk
from tkinter import messagebox, ttk
import mysql.connector

# Kết nối tới cơ sở dữ liệu MySQL
conn = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="SQLdat1502:3",
    database="firesmokesensor"
)
cursor = conn.cursor()

# Hàm tìm kiếm dựa trên ID hoặc loại cảm biến
def search_data():
    search_term = search_entry.get()
    query = "SELECT * FROM data_sensors WHERE Id = %s OR Sensor_type = %s"
    cursor.execute(query, (search_term, search_term))
    result = cursor.fetchall()
    display_data(result, data_tree)

# Hàm hiển thị dữ liệu trong bảng
def display_data(data, tree):
    for item in tree.get_children():
        tree.delete(item)
    for row in data:
        tree.insert("", "end", values=row)

# Hàm lấy và hiển thị dữ liệu từ bảng sensors, data_sensors, timestamps
def fetch_all_data():
    query = "SELECT * FROM data_sensors"
    cursor.execute(query)
    data_sensors = cursor.fetchall()
    display_data(data_sensors, data_tree)

# Hàm thêm dữ liệu
def add_data():
    sensor_type = type_entry.get()
    sensor_value = value_entry.get()
    status = status_entry.get()
    query = "INSERT INTO data_sensors (Sensor_type, Sensor_value, Status) VALUES (%s, %s, %s)"
    cursor.execute(query, (sensor_type, sensor_value, status))
    conn.commit()
    fetch_all_data()
    messagebox.showinfo("Thông báo", "Dữ liệu đã được thêm thành công.")

# Hàm xóa dữ liệu theo ID
def delete_data():
    selected_item = data_tree.selection()[0]
    item_id = data_tree.item(selected_item)['values'][0]
    query = "DELETE FROM data_sensors WHERE Id = %s"
    cursor.execute(query, (item_id,))
    conn.commit()
    fetch_all_data()
    messagebox.showinfo("Thông báo", "Dữ liệu đã được xóa thành công.")

# Hàm xem nhật ký hoạt động của cảm biến
def view_logs():
    query = "SELECT * FROM timestamps"
    cursor.execute(query)
    logs = cursor.fetchall()
    display_data(logs, log_tree)

# Giao diện chính
root = tk.Tk()
root.title("Quản lý Dữ liệu Cảm biến Robot Chữa cháy")
root.geometry("1000x2500")

# Khung tìm kiếm
search_frame = tk.Frame(root)
search_frame.pack(pady=10)
search_label = tk.Label(search_frame, text="Tìm kiếm (ID hoặc Loại Cảm biến):")
search_label.pack(side="left")
search_entry = tk.Entry(search_frame)
search_entry.pack(side="left", padx=5)
search_button = tk.Button(search_frame, text="Tìm kiếm", command=search_data)
search_button.pack(side="left")

# Khung thêm dữ liệu
add_frame = tk.Frame(root)
add_frame.pack(pady=10)
tk.Label(add_frame, text="Loại cảm biến:").grid(row=0, column=0)
type_entry = tk.Entry(add_frame)
type_entry.grid(row=0, column=1)
tk.Label(add_frame, text="Giá trị cảm biến:").grid(row=1, column=0)
value_entry = tk.Entry(add_frame)
value_entry.grid(row=1, column=1)
tk.Label(add_frame, text="Trạng thái:").grid(row=2, column=0)
status_entry = tk.Entry(add_frame)
status_entry.grid(row=2, column=1)
add_button = tk.Button(add_frame, text="Thêm dữ liệu", command=add_data)
add_button.grid(row=3, columnspan=2, pady=5)

# Bảng hiển thị dữ liệu cảm biến
data_tree = ttk.Treeview(root, columns=("Id", "Sensor_type", "Sensor_value", "image_data", "Status"), show="headings")
data_tree.heading("Id", text="ID")
data_tree.heading("Sensor_type", text="Loại Cảm Biến")
data_tree.heading("Sensor_value", text="Giá trị")
data_tree.heading("image_data", text="Hình ảnh")
data_tree.heading("Status", text="Trạng thái")
data_tree.pack(pady=10)

# Nút xóa
delete_button = tk.Button(root, text="Xóa dữ liệu", command=delete_data)
delete_button.pack(pady=5)

# Bảng xem nhật ký hoạt động
log_frame = tk.LabelFrame(root, text="Nhật ký hoạt động của cảm biến")
log_frame.pack(fill="both", expand="yes", padx=10, pady=10)
log_tree = ttk.Treeview(log_frame, columns=("Time_id", "Record_time"), show="headings")
log_tree.heading("Time_id", text="ID Thời gian")
log_tree.heading("Record_time", text="Thời gian Ghi nhận")
log_tree.pack()

log_button = tk.Button(root, text="Xem Nhật ký Hoạt động", command=view_logs)
log_button.pack(pady=5)

# Hiển thị dữ liệu ban đầu
fetch_all_data()

root.mainloop()

# Đóng kết nối sau khi thoát ứng dụng
cursor.close()
conn.close()
