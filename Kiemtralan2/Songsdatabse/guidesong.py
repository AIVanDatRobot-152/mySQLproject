import mysql.connector
from tkinter import *
from tkinter import messagebox
import pygame
import io

# Kết nối tới cơ sở dữ liệu MySQL
def connect_to_database():
    conn = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="SQLdat1502:3",
        database="kiemtralan2"
    )
    return conn

# Phát nhạc
def play_music(songs):
    pygame.mixer.init()
    mp3_stream = io.BytesIO(songs)  # Chuyển dữ liệu nhị phân sang stream để phát
    pygame.mixer.music.load(mp3_stream, 'mp3')
    pygame.mixer.music.play()

# Dừng nhạc
def stop_music():
    if pygame.mixer.music.get_busy():  # Kiểm tra xem nhạc có đang phát không
        pygame.mixer.music.stop()

# Truy vấn dữ liệu từ bảng dựa trên ID hoặc tên
def query_data(event=None):
    try:
        search_term = entry_search.get().strip()  # Lấy dữ liệu từ ô nhập liệu
        conn = connect_to_database()
        cursor = conn.cursor()

        # Truy vấn dữ liệu dựa trên ID hoặc tên
        if search_term.isdigit():
            sql = "SELECT Song_Id, Song_name, Artist, Album, file_data FROM songs WHERE Song_Id = %s"
            cursor.execute(sql, (search_term,))
        else:
            sql = "SELECT Song_Id, Song_name, Artist, Album, file_data FROM songs WHERE Song_name = %s"
            cursor.execute(sql, (search_term,))

        row = cursor.fetchone()

        if row:
            label_name.config(text=f"Name: {row[1]}", fg="blue")  # Thêm màu xanh cho chữ
            label_description.config(text=f"Album: {row[3]}", fg="green")  # Màu xanh lá cho mô tả
            label_artist.config(text=f"Artist: {row[2]}", fg="purple")  # Thêm tên nghệ sĩ

            # Phát nhạc
            songs = row[4]  # Chuyển đến cột chứa dữ liệu âm thanh
            play_music(songs)
        else:
            messagebox.showinfo("Not Found", "No data found for the given ID or Name.")
        
        cursor.close()
        conn.close()

    except Exception as e:
        messagebox.showerror("Error", f"Error fetching data: {e}")

# Tạo giao diện với Tkinter
root = Tk()
root.title("Music Query App")
root.geometry("500x400")
root.configure(bg="#f0f0f0")  # Màu nền

# Label và ô nhập ID hoặc tên
label_search = Label(root, text="Enter Music ID or Name:", fg="purple", bg="#f0f0f0", font=("Arial", 14))  # Màu tím cho nhãn
label_search.pack(pady=20)
entry_search = Entry(root, font=("Arial", 14), width=25)
entry_search.pack(pady=10)
entry_search.bind("<Return>", query_data)  # Kích hoạt tìm kiếm bằng phím Enter

# Hiển thị tên, nghệ sĩ và mô tả
label_name = Label(root, text="Name: ", fg="blue", bg="#f0f0f0", font=("Arial", 12))  # Màu xanh cho tên
label_name.pack(pady=5)

label_artist = Label(root, text="Artist: ", fg="purple", bg="#f0f0f0", font=("Arial", 12))  # Màu tím cho nghệ sĩ
label_artist.pack(pady=5)

label_description = Label(root, text="Album: ", fg="green", bg="#f0f0f0", font=("Arial", 12))  # Màu xanh lá cho mô tả
label_description.pack(pady=5)

# Nút truy vấn để phát nhạc
button_query = Button(root, text="Play Music", command=query_data, bg="#87CEEB", fg="black", font=("Arial", 14))  # Nút màu xanh nhạt
button_query.pack(pady=20)

# Nút dừng nhạc
button_stop = Button(root, text="Stop Music", command=stop_music, bg="#FF6347", fg="white", font=("Arial", 14))  # Nút dừng nhạc màu đỏ
button_stop.pack(pady=10)

# Chạy giao diện
root.mainloop()
