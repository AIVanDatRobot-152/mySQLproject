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
        database="imager_data"
    )
    return conn

# Phát nhạc
def play_music(music_data):
    pygame.mixer.init()
    mp3_stream = io.BytesIO(music_data)  # Chuyển dữ liệu nhị phân sang stream để phát
    pygame.mixer.music.load(mp3_stream, 'mp3')
    pygame.mixer.music.play()

# Truy vấn dữ liệu từ bảng dựa trên ID
def query_data():
    try:
        music_id = entry_id.get()
        conn = connect_to_database()
        cursor = conn.cursor()

        # Truy vấn dữ liệu theo ID
        sql = "SELECT Music_Id, Music_name, Music_data, Description_Music FROM music_data WHERE Music_Id = %s"
        cursor.execute(sql, (music_id,))
        row = cursor.fetchone()

        if row:
            label_name.config(text=f"Name: {row[1]}")
            label_description.config(text=f"Description: {row[3]}")

            # Phát nhạc
            music_data = row[2]
            play_music(music_data)
        else:
            messagebox.showinfo("Not Found", "No data found for the given ID.")
        
        cursor.close()
        conn.close()

    except Exception as e:
        messagebox.showerror("Error", f"Error fetching data: {e}")

# Tạo giao diện với Tkinter
root = Tk()
root.title("Music Query App")
root.geometry("400x400")

# ID input
label_id = Label(root, text="Enter Music ID:")
label_id.pack(pady=10)
entry_id = Entry(root)
entry_id.pack(pady=10)

# Name, Description display
label_name = Label(root, text="Name: ")
label_name.pack(pady=5)
label_description = Label(root, text="Description: ")
label_description.pack(pady=5)

# Button để truy vấn
button_query = Button(root, text="Truy vấn và phát nhạc", command=query_data)
button_query.pack(pady=20)

# Chạy giao diện
root.mainloop()
