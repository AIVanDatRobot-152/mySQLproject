import mysql.connector
from tkinter import *
from tkinter import messagebox, ttk, filedialog
import pygame
import io
import os
import subprocess  # Thư viện để mở file nhạc bằng phần mềm khác

# Kết nối tới cơ sở dữ liệu MySQL
def connect_to_database():
    conn = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="SQLdat1502:3",
        database="kiemtralan2"
    )
    return conn

# Phát nhạc bằng file nhạc từ MySQL (file_data)
def play_music_from_data(song_data):
    pygame.mixer.init()
    mp3_stream = io.BytesIO(song_data)  # Chuyển dữ liệu nhị phân sang stream để phát
    pygame.mixer.music.load(mp3_stream)
    pygame.mixer.music.play()

# Phát nhạc bằng URL (file_path)
def play_music_from_path(file_path):
    if os.path.exists(file_path):
        subprocess.run(["start", "", file_path], shell=True)  # Dùng "start" để mở file
    else:
        messagebox.showerror("Error", "File path does not exist.")

# Dừng nhạc
def stop_music():
    if pygame.mixer.music.get_busy():  # Kiểm tra xem nhạc có đang phát không
        pygame.mixer.music.stop()

# Truy vấn dữ liệu từ bảng và hiển thị danh sách nhạc
def query_data(event=None):
    try:
        conn = connect_to_database()
        cursor = conn.cursor()

        # Lấy giá trị từ ô tìm kiếm
        search_value = entry_search.get().strip()

        # Truy vấn dữ liệu từ bảng, nếu có giá trị tìm kiếm thì lọc
        if search_value:
            sql = "SELECT Song_Id, Song_name, Artist, Album, file_data, file_path FROM songs WHERE Song_Id LIKE %s OR Song_name LIKE %s"
            cursor.execute(sql, (f"%{search_value}%", f"%{search_value}%"))
        else:
            sql = "SELECT Song_Id, Song_name, Artist, Album, file_data, file_path FROM songs"
            cursor.execute(sql)

        # Xóa dữ liệu cũ trong danh sách nhạc
        for row in tree.get_children():
            tree.delete(row)

        # Lưu danh sách nhạc
        global song_data, song_path
        for row in cursor.fetchall():
            tree.insert("", "end", values=row[:-2])  # Chỉ thêm các cột cần thiết vào Treeview
            # Lưu dữ liệu nhạc từ dòng cuối cùng
            song_data, song_path = row[4], row[5]

        cursor.close()
        conn.close()

    except Exception as e:
        messagebox.showerror("Error", f"Error fetching data: {e}")

# Phát nhạc từ dòng đã chọn bằng file_data
def play_selected_music_data():
    selected_item = tree.selection()
    if selected_item:
        selected_song = tree.item(selected_item, "values")
        if selected_song:
            song_id = selected_song[0]
            conn = connect_to_database()
            cursor = conn.cursor()
            cursor.execute("SELECT file_data FROM songs WHERE Song_Id = %s", (song_id,))
            row = cursor.fetchone()

            if row:
                song_data = row[0]
                play_music_from_data(song_data)

            cursor.close()
            conn.close()
    else:
        messagebox.showwarning("Select Song", "Please select a song to play.")

# Phát nhạc từ dòng đã chọn bằng file_path
def play_selected_music_path():
    selected_item = tree.selection()
    if selected_item:
        selected_song = tree.item(selected_item, "values")
        if selected_song:
            song_id = selected_song[0]
            conn = connect_to_database()
            cursor = conn.cursor()
            cursor.execute("SELECT file_path FROM songs WHERE Song_Id = %s", (song_id,))
            row = cursor.fetchone()

            if row:
                song_path = row[0]
                play_music_from_path(song_path)

            cursor.close()
            conn.close()
    else:
        messagebox.showwarning("Select Song", "Please select a song to play.")

# Thêm nhạc mới vào cơ sở dữ liệu
def upload_music():
    file_path = filedialog.askopenfilename(title="Select a Music File", filetypes=[("MP3 Files", "*.mp3")])
    if file_path:
        song_name = os.path.basename(file_path)
        artist = "Unknown Artist"  # Thay đổi theo yêu cầu của bạn
        album = "Unknown Album"  # Thay đổi theo yêu cầu của bạn

        # Đọc dữ liệu nhạc
        with open(file_path, "rb") as file:
            file_data = file.read()

        try:
            conn = connect_to_database()
            cursor = conn.cursor()
            sql = "INSERT INTO songs (Song_name, Artist, Album, file_data, file_path) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(sql, (song_name, artist, album, file_data, file_path))
            conn.commit()
            cursor.close()
            conn.close()
            messagebox.showinfo("Success", "Music uploaded successfully.")
            query_data()  # Cập nhật danh sách nhạc sau khi thêm
        except Exception as e:
            messagebox.showerror("Error", f"Error uploading music: {e}")

# Xóa nhạc đã chọn khỏi cơ sở dữ liệu
def delete_music():
    selected_item = tree.selection()
    if selected_item:
        selected_song = tree.item(selected_item, "values")
        if selected_song:
            song_id = selected_song[0]
            try:
                conn = connect_to_database()
                cursor = conn.cursor()
                cursor.execute("DELETE FROM songs WHERE Song_Id = %s", (song_id,))
                conn.commit()
                cursor.close()
                conn.close()
                messagebox.showinfo("Success", "Music deleted successfully.")
                query_data()  # Cập nhật danh sách nhạc sau khi xóa
            except Exception as e:
                messagebox.showerror("Error", f"Error deleting music: {e}")
    else:
        messagebox.showwarning("Select Song", "Please select a song to delete.")

# Cập nhật thông tin bài hát đang phát
def update_current_song_info():
    selected_item = tree.selection()
    if selected_item:
        selected_song = tree.item(selected_item, "values")
        if selected_song:
            song_info = f"Name: {selected_song[1]} | Artist: {selected_song[2]} | Album: {selected_song[3]}"
            label_song_info.config(text=song_info)  # Cập nhật thông tin bài hát

# Tạo giao diện với Tkinter
root = Tk()
root.title("Music Query App")
root.geometry("800x600")
root.configure(bg="#f0f0f0")  # Màu nền

# Tạo khung bên trái cho thanh tìm kiếm và thông tin nhạc
frame_left = Frame(root, bg="#f0f0f0")
frame_left.pack(side=LEFT, fill=Y, padx=10, pady=10)

# Label và ô nhập ID hoặc tên
label_search = Label(frame_left, text="Enter Music ID or Name:", fg="purple", bg="#f0f0f0", font=("Arial", 14))
label_search.pack(pady=10)
entry_search = Entry(frame_left, font=("Arial", 14), width=25)
entry_search.pack(pady=10)
entry_search.bind("<Return>", query_data)  # Kích hoạt tìm kiếm bằng phím Enter

# Hiển thị thông tin bài hát
label_song_info = Label(frame_left, text="", fg="black", bg="#f0f0f0", font=("Arial", 12))
label_song_info.pack(pady=10)

# Tạo khung cho các nút tương tác
frame_buttons = Frame(frame_left, bg="#f0f0f0")
frame_buttons.pack(pady=20)

# Nút truy vấn danh sách nhạc
button_query = Button(frame_buttons, text="Load Music List", command=query_data, bg="#87CEEB", fg="black", font=("Arial", 12))
button_query.grid(row=0, column=0, padx=5, pady=5)

# Nút phát nhạc từ nhạc đã chọn (file_data)
button_play_data = Button(frame_buttons, text="Play from Data", command=play_selected_music_data, bg="#87CEEB", fg="black", font=("Arial", 12))
button_play_data.grid(row=1, column=0, padx=5, pady=5)

# Nút phát nhạc từ nhạc đã chọn (file_path)
button_play_path = Button(frame_buttons, text="Play from Path", command=play_selected_music_path, bg="#87CEEB", fg="black", font=("Arial", 12))
button_play_path.grid(row=2, column=0, padx=5, pady=5)

# Nút tải lên nhạc
button_upload = Button(frame_buttons, text="Upload Music", command=upload_music, bg="#87CEEB", fg="black", font=("Arial", 12))
button_upload.grid(row=3, column=0, padx=5, pady=5)

# Nút xóa nhạc đã chọn
button_delete = Button(frame_buttons, text="Delete Music", command=delete_music, bg="#FF6347", fg="white", font=("Arial", 12))
button_delete.grid(row=4, column=0, padx=5, pady=5)

# Nút dừng nhạc
button_stop = Button(frame_buttons, text="Stop Music", command=stop_music, bg="#FF6347", fg="white", font=("Arial", 12))
button_stop.grid(row=5, column=0, padx=5, pady=5)

# Tạo khung bên phải cho danh sách nhạc
frame_right = Frame(root, bg="#f0f0f0")
frame_right.pack(side=RIGHT, fill=BOTH, expand=True, padx=10, pady=10)

# Tạo Treeview để hiển thị danh sách nhạc
tree = ttk.Treeview(frame_right, columns=("Song_Id", "Song_name", "Artist", "Album"), show="headings")
tree.heading("Song_Id", text="ID")
tree.heading("Song_name", text="Name")
tree.heading("Artist", text="Artist")
tree.heading("Album", text="Album")

tree.column("Song_Id", width=70)
tree.column("Song_name", width=150)
tree.column("Artist", width=100)
tree.column("Album", width=100)
tree.pack(pady=10)

# Thêm thanh cuộn cho Treeview
scrollbar = ttk.Scrollbar(frame_right, orient=VERTICAL, command=tree.yview)
tree.configure(yscroll=scrollbar.set)
scrollbar.pack(side=RIGHT, fill=Y)

tree.pack(fill=BOTH, expand=True)

# Bắt sự kiện khi nhạc dừng
def on_music_stop():
    label_song_info.config(text="")  # Xóa thông tin bài hát đang phát

# Cập nhật thông tin bài hát đang phát
tree.bind("<<TreeviewSelect>>", lambda event: update_current_song_info())

# Chạy giao diện
root.mainloop()
