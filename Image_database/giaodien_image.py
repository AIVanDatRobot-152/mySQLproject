import mysql.connector
from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
import io

# Kết nối tới cơ sở dữ liệu MySQL
def connect_to_database():
    conn = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="SQLdat1502:3",
        database="imager_data"
    )
    return conn

# Truy vấn dữ liệu từ bảng dựa trên ID
def query_data():
    try:
        image_id = entry_id.get()
        conn = connect_to_database()
        cursor = conn.cursor()

        # Truy vấn dữ liệu theo ID
        sql = "SELECT Image_Id, Image_name, Image_data, Description_image FROM image_data WHERE Image_Id = %s"
        cursor.execute(sql, (image_id,))
        row = cursor.fetchone()

        if row:
            label_name.config(text=f"Name: {row[1]}")
            label_description.config(text=f"Description: {row[3]}")

            # Hiển thị hình ảnh
            image_data = row[2]
            image = Image.open(io.BytesIO(image_data))
            image = image.resize((200, 200))  # Chỉnh kích thước cho hình ảnh
            photo = ImageTk.PhotoImage(image)
            label_image.config(image=photo)
            label_image.image = photo  # Giữ tham chiếu tới hình ảnh
        else:
            messagebox.showinfo("Not Found", "No data found for the given ID.")
        
        cursor.close()
        conn.close()

    except Exception as e:
        messagebox.showerror("Error", f"Error fetching data: {e}")

# Tạo giao diện với Tkinter
root = Tk()
root.title("Image Query App")
root.geometry("400x400")

# ID input
label_id = Label(root, text="Enter Image ID:")
label_id.pack(pady=10)
entry_id = Entry(root)
entry_id.pack(pady=10)

# Name, Description and Image display
label_name = Label(root, text="Name: ")
label_name.pack(pady=5)
label_description = Label(root, text="Description: ")
label_description.pack(pady=5)

label_image = Label(root)
label_image.pack(pady=10)

# Button để truy vấn
button_query = Button(root, text="Truy vấn", command=query_data)
button_query.pack(pady=20)

# Chạy giao diện
root.mainloop()
