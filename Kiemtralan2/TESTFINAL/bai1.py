import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog, Frame, Label, Entry
import mysql.connector
import os
import vlc

# Kết nối với cơ sở dữ liệu
def connect_to_database():
    return mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="SQLdat1502:3",
        database="kiemtralan2"
    )

# Khởi tạo trình phát VLC
media_player = vlc.MediaPlayer()

# Hàm tải danh sách video
def load_videos():
    conn = connect_to_database()
    cursor = conn.cursor()
    cursor.execute("SELECT Movie_Id, Movie_name FROM movies")
    video_list.delete(0, tk.END)
    for video in cursor.fetchall():
        video_list.insert(tk.END, video[1])
    cursor.close()
    conn.close()  # Đóng kết nối sau khi sử dụng

# Hàm mở video
def open_video():
    selected_video = video_list.curselection()
    if selected_video:
        video_name = video_list.get(selected_video)
        conn = connect_to_database()
        cursor = conn.cursor()
        cursor.execute("SELECT file_path FROM movies WHERE Movie_name = %s", (video_name,))
        file_path = cursor.fetchone()
        cursor.close()
        conn.close()  # Đóng kết nối sau khi sử dụng
        
        if file_path:
            media_player.set_media(vlc.Media(file_path[0]))
            media_player.set_hwnd(video_frame.winfo_id())
            media_player.play()
            display_video_info(None)
        else:
            messagebox.showwarning("Lỗi", "Không tìm thấy video.")
    else:
        messagebox.showwarning("Chọn video", "Hãy chọn một video để mở.")

# Hàm thêm video mới
def add_video():
    file_path = filedialog.askopenfilename(title="Chọn file video", filetypes=[("Video files", "*.mp4 *.avi")])
    if file_path:
        video_name = os.path.basename(file_path)
        director_name = simpledialog.askstring("Nhập tên đạo diễn", "Tên đạo diễn:")
        
        conn = connect_to_database()
        cursor = conn.cursor()
        # Lấy ID mới cho video
        cursor.execute("SELECT COALESCE(MAX(Movie_Id), 0) + 1 FROM movies")
        new_id = cursor.fetchone()[0]
        cursor.execute("INSERT INTO movies (Movie_Id, Movie_name, Director, file_path) VALUES (%s, %s, %s, %s)",
                       (new_id, video_name, director_name, file_path))
        conn.commit()
        cursor.close()
        conn.close()  # Đóng kết nối sau khi sử dụng
        load_videos()

# Hàm xóa video
def delete_video():
    selected_video = video_list.curselection()
    if selected_video:
        video_name = video_list.get(selected_video)
        conn = connect_to_database()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM movies WHERE Movie_name = %s", (video_name,))
        conn.commit()
        cursor.close()
        conn.close()  # Đóng kết nối sau khi sử dụng
        load_videos()
    else:
        messagebox.showwarning("Chọn video", "Hãy chọn một video để xóa")

# Hàm sửa thông tin video
def edit_video():
    selected_video = video_list.curselection()
    if selected_video:
        video_name = video_list.get(selected_video)
        new_name = simpledialog.askstring("Chỉnh sửa video", "Nhập tên mới cho video:", initialvalue=video_name)
        new_director = simpledialog.askstring("Chỉnh sửa video", "Nhập tên đạo diễn mới:")
        
        if new_name and new_director:
            conn = connect_to_database()
            cursor = conn.cursor()
            cursor.execute("UPDATE movies SET Movie_name = %s, Director = %s WHERE Movie_name = %s",
                           (new_name, new_director, video_name))
            conn.commit()
            cursor.close()
            conn.close()  # Đóng kết nối sau khi sử dụng
            load_videos()
    else:
        messagebox.showwarning("Chọn video", "Hãy chọn một video để chỉnh sửa")

# Hàm tải danh sách âm nhạc
def load_music():
    conn = connect_to_database()
    cursor = conn.cursor()
    cursor.execute("SELECT Song_Id, Song_name FROM songs")
    music_list.delete(0, tk.END)
    for music in cursor.fetchall():
        music_list.insert(tk.END, music[1])
    cursor.close()
    conn.close()  # Đóng kết nối sau khi sử dụng

# Hàm thêm âm nhạc mới
def add_music():
    file_path = filedialog.askopenfilename(title="Chọn file âm nhạc", filetypes=[("Audio files", "*.mp3 *.wav")])
    if file_path:
        music_name = simpledialog.askstring("Thêm âm nhạc", "Nhập tên bài hát:")
        singer_name = simpledialog.askstring("Thêm âm nhạc", "Nhập tên ca sĩ:")
        album_name = simpledialog.askstring("Thêm âm nhạc", "Nhập tên album:")
        
        if music_name and singer_name and album_name:
            conn = connect_to_database()
            cursor = conn.cursor()
            # Lấy ID mới cho bài hát
            cursor.execute("SELECT COALESCE(MAX(Song_Id), 0) + 1 FROM songs")
            new_id = cursor.fetchone()[0]
            cursor.execute("INSERT INTO songs (Song_Id, Song_name, Artist, Album, file_path) VALUES (%s, %s, %s, %s, %s)",
                           (new_id, music_name, singer_name, album_name, file_path))
            conn.commit()
            cursor.close()
            conn.close()  # Đóng kết nối sau khi sử dụng
            load_music()

# Hàm xóa âm nhạc
def delete_music():
    selected_music = music_list.curselection()
    if selected_music:
        music_name = music_list.get(selected_music)
        conn = connect_to_database()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM songs WHERE Song_name = %s", (music_name,))
        conn.commit()
        cursor.close()
        conn.close()  # Đóng kết nối sau khi sử dụng
        load_music()
    else:
        messagebox.showwarning("Chọn âm nhạc", "Hãy chọn một bài hát để xóa")

# Hàm sửa thông tin âm nhạc
def edit_music():
    selected_music = music_list.curselection()
    if selected_music:
        music_name = music_list.get(selected_music)
        new_name = simpledialog.askstring("Chỉnh sửa âm nhạc", "Nhập tên mới cho bài hát:", initialvalue=music_name)
        new_singer = simpledialog.askstring("Chỉnh sửa âm nhạc", "Nhập tên ca sĩ mới:")
        new_album = simpledialog.askstring("Chỉnh sửa âm nhạc", "Nhập tên album mới:")
        
        if new_name and new_singer and new_album:
            conn = connect_to_database()
            cursor = conn.cursor()
            cursor.execute("UPDATE songs SET Song_name = %s, Artist = %s, Album = %s WHERE Song_name = %s",
                           (new_name, new_singer, new_album, music_name))
            conn.commit()
            cursor.close()
            conn.close()  # Đóng kết nối sau khi sử dụng
            load_music()
    else:
        messagebox.showwarning("Chọn âm nhạc", "Hãy chọn một bài hát để chỉnh sửa")

# Hàm phát nhạc
def play_music():
    selected_music = music_list.curselection()
    if selected_music:
        music_name = music_list.get(selected_music)
        conn = connect_to_database()
        cursor = conn.cursor()
        cursor.execute("SELECT file_path FROM songs WHERE Song_name = %s", (music_name,))
        file_path = cursor.fetchone()
        
        if file_path:
            media_player.set_media(vlc.Media(file_path[0]))
            media_player.play()
            display_music_info(None)
        cursor.close()
        conn.close()  # Đóng kết nối sau khi sử dụng
    else:
        messagebox.showwarning("Chọn âm nhạc", "Hãy chọn một bài hát để phát")

# Hàm hiển thị thông tin video
def display_video_info(event):
    selected_video = video_list.curselection()
    if selected_video:
        video_name = video_list.get(selected_video)
        conn = connect_to_database()
        cursor = conn.cursor()
        cursor.execute("SELECT Director, file_path FROM movies WHERE Movie_name = %s", (video_name,))
        video_info = cursor.fetchone()
        cursor.close()
        conn.close()  # Đóng kết nối sau khi sử dụng
        
        if video_info:
            video_info_text.set(f"Tên video: {video_name}\nĐạo diễn: {video_info[0]}\nĐường dẫn: {video_info[1]}")
        else:
            video_info_text.set("Không tìm thấy thông tin video.")
    else:
        video_info_text.set("")

# Hàm hiển thị thông tin âm nhạc
def display_music_info(event):
    selected_music = music_list.curselection()
    if selected_music:
        music_name = music_list.get(selected_music)
        conn = connect_to_database()
        cursor = conn.cursor()
        cursor.execute("SELECT Artist, Album, file_path FROM songs WHERE Song_name = %s", (music_name,))
        music_info = cursor.fetchone()
        cursor.close()
        conn.close()  # Đóng kết nối sau khi sử dụng
        
        if music_info:
            music_info_text.set(f"Tên bài hát: {music_name}\nCa sĩ: {music_info[0]}\nAlbum: {music_info[1]}\nĐường dẫn: {music_info[2]}")
        else:
            music_info_text.set("Không tìm thấy thông tin âm nhạc.")
    else:
        music_info_text.set("")

# Tạo giao diện người dùng
root = tk.Tk()
root.title("Media Player")
root.geometry("800x600")

# Khung video
video_frame = Frame(root, width=640, height=360)
video_frame.pack(pady=10)

# Khung tìm kiếm và nút bấm
search_frame = Frame(root)
search_frame.pack(pady=10)

# Thanh tìm kiếm video
search_video_label = Label(search_frame, text="Tìm video:")
search_video_label.grid(row=0, column=0, padx=5)
search_video_entry = Entry(search_frame, width=20)
search_video_entry.grid(row=0, column=1, padx=5)

# Nút tìm kiếm video
search_video_button = tk.Button(search_frame, text="Tìm", command=lambda: search_video(search_video_entry.get()))
search_video_button.grid(row=0, column=2, padx=5)

# Danh sách video
video_list = tk.Listbox(root, width=50, height=10)
video_list.pack(pady=10)
video_list.bind('<<ListboxSelect>>', display_video_info)

# Thông tin video
video_info_text = tk.StringVar()
video_info_label = Label(root, textvariable=video_info_text, justify='left')
video_info_label.pack(pady=10)

# Khung âm nhạc
music_frame = Frame(root, width=640, height=360)
music_frame.pack(pady=10)

# Khung tìm kiếm âm nhạc
search_frame_music = Frame(root)
search_frame_music.pack(pady=10)

# Thanh tìm kiếm âm nhạc
search_music_label = Label(search_frame_music, text="Tìm âm nhạc:")
search_music_label.grid(row=0, column=0, padx=5)
search_music_entry = Entry(search_frame_music, width=20)
search_music_entry.grid(row=0, column=1, padx=5)

# Nút tìm kiếm âm nhạc
search_music_button = tk.Button(search_frame_music, text="Tìm", command=lambda: search_music(search_music_entry.get()))
search_music_button.grid(row=0, column=2, padx=5)

# Danh sách âm nhạc
music_list = tk.Listbox(root, width=50, height=10)
music_list.pack(pady=10)
music_list.bind('<<ListboxSelect>>', display_music_info)

# Thông tin âm nhạc
music_info_text = tk.StringVar()
music_info_label = Label(root, textvariable=music_info_text, justify='left')
music_info_label.pack(pady=10)

# Nút thêm video
add_video_button = tk.Button(root, text="Thêm video", command=add_video)
add_video_button.pack(side=tk.LEFT, padx=5)

# Nút xóa video
delete_video_button = tk.Button(root, text="Xóa video", command=delete_video)
delete_video_button.pack(side=tk.LEFT, padx=5)

# Nút chỉnh sửa video
edit_video_button = tk.Button(root, text="Chỉnh sửa video", command=edit_video)
edit_video_button.pack(side=tk.LEFT, padx=5)

# Nút phát nhạc
play_music_button = tk.Button(root, text="Phát nhạc", command=play_music)
play_music_button.pack(side=tk.LEFT, padx=5)

# Nút thêm âm nhạc
add_music_button = tk.Button(root, text="Thêm âm nhạc", command=add_music)
add_music_button.pack(side=tk.LEFT, padx=5)

# Nút xóa âm nhạc
delete_music_button = tk.Button(root, text="Xóa âm nhạc", command=delete_music)
delete_music_button.pack(side=tk.LEFT, padx=5)

# Nút chỉnh sửa âm nhạc
edit_music_button = tk.Button(root, text="Chỉnh sửa âm nhạc", command=edit_music)
edit_music_button.pack(side=tk.LEFT, padx=5)

# Tải danh sách video và âm nhạc khi khởi động
load_videos()
load_music()

root.mainloop()
