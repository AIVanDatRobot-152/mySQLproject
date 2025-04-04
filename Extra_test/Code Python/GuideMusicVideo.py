import mysql.connector
from tkinter import *
from tkinter import messagebox, ttk, filedialog
import pygame
import io
import os
import subprocess

# Kết nối tới cơ sở dữ liệu MySQL
def connect_to_database():
    conn = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="SQLdat1502:3",
        database="kiemtralan2"
    )
    return conn

# ------------------ Phần giao diện Music ------------------

# Phát nhạc từ dữ liệu
def play_music_from_data(song_data):
    pygame.mixer.init()
    mp3_stream = io.BytesIO(song_data)
    pygame.mixer.music.load(mp3_stream)
    pygame.mixer.music.play()

# Phát nhạc từ đường dẫn
def play_music_from_path(file_path):
    if os.path.exists(file_path):
        subprocess.run(["start", "", file_path], shell=True)
    else:
        messagebox.showerror("Error", "File path does not exist.")

def stop_music():
    if pygame.mixer.music.get_busy():
        pygame.mixer.music.stop()

def query_music_data(event=None):
    try:
        conn = connect_to_database()
        cursor = conn.cursor()
        search_value = entry_music_search.get().strip()

        if search_value:
            sql = "SELECT Song_Id, Song_name, Artist, Album, file_data, file_path FROM songs WHERE Song_Id LIKE %s OR Song_name LIKE %s"
            cursor.execute(sql, (f"%{search_value}%", f"%{search_value}%"))
        else:
            sql = "SELECT Song_Id, Song_name, Artist, Album, file_data, file_path FROM songs"
            cursor.execute(sql)

        for row in music_tree.get_children():
            music_tree.delete(row)

        global song_data, song_path
        for row in cursor.fetchall():
            music_tree.insert("", "end", values=row[:-2])
            song_data, song_path = row[4], row[5]

        cursor.close()
        conn.close()
    except Exception as e:
        messagebox.showerror("Error", f"Error fetching data: {e}")

def play_selected_music_data():
    selected_item = music_tree.selection()
    if selected_item:
        selected_song = music_tree.item(selected_item, "values")
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

def upload_music():
    file_path = filedialog.askopenfilename(title="Select a Music File", filetypes=[("MP3 Files", "*.mp3")])
    if file_path:
        song_name = os.path.basename(file_path)
        artist = "Unknown Artist"
        album = "Unknown Album"
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
            query_music_data()
        except Exception as e:
            messagebox.showerror("Error", f"Error uploading music: {e}")

# Hàm xóa nhạc
def delete_music():
    selected_item = music_tree.selection()
    if selected_item:
        selected_song = music_tree.item(selected_item, "values")
        if selected_song:
            song_id = selected_song[0]
            try:
                conn = connect_to_database()
                cursor = conn.cursor()
                sql = "DELETE FROM songs WHERE Song_Id = %s"
                cursor.execute(sql, (song_id,))
                conn.commit()
                cursor.close()
                conn.close()
                messagebox.showinfo("Success", "Music deleted successfully.")
                query_music_data()  # Cập nhật lại danh sách nhạc
            except Exception as e:
                messagebox.showerror("Error", f"Error deleting music: {e}")
    else:
        messagebox.showwarning("Select Music", "Please select a song to delete.")

# ------------------ Phần giao diện Video ------------------

def play_video(file_path):
    if os.path.exists(file_path):
        subprocess.run(["start", "", file_path], shell=True)
    else:
        messagebox.showerror("Error", "File path does not exist.")

def query_video_data(search_query=None):
    try:
        conn = connect_to_database()
        cursor = conn.cursor()

        if search_query:
            sql = "SELECT Movie_Id, Movie_name, Director, file_path FROM kiemtralan2.movies WHERE Movie_name LIKE %s OR Director LIKE %s OR Movie_Id LIKE %s"
            cursor.execute(sql, ('%' + search_query + '%', '%' + search_query + '%', '%' + search_query + '%'))
        else:
            sql = "SELECT Movie_Id, Movie_name, Director, file_path FROM kiemtralan2.movies"
            cursor.execute(sql)

        for row in video_tree.get_children():
            video_tree.delete(row)

        for row in cursor.fetchall():
            video_tree.insert("", "end", values=row)

        cursor.close()
        conn.close()
    except Exception as e:
        messagebox.showerror("Error", f"Error fetching data: {e}")

def play_selected_video():
    selected_item = video_tree.selection()
    if selected_item:
        selected_movie = video_tree.item(selected_item, "values")
        if selected_movie:
            file_path = selected_movie[3]
            play_video(file_path)
    else:
        messagebox.showwarning("Select Movie", "Please select a movie to play.")

def insert_video():
    file_path = filedialog.askopenfilename(filetypes=[("Video Files", "*.mp4;*.avi;*.mkv;*.mov")])
    if file_path:
        movie_name = entry_video_name.get()
        director_name = entry_video_director.get()

        if movie_name and director_name:
            try:
                conn = connect_to_database()
                cursor = conn.cursor()
                sql = "INSERT INTO kiemtralan2.movies (Movie_name, Director, file_path) VALUES (%s, %s, %s)"
                cursor.execute(sql, (movie_name, director_name, file_path))
                conn.commit()
                cursor.close()
                conn.close()
                messagebox.showinfo("Success", "Video added successfully.")
                query_video_data()  
            except Exception as e:
                messagebox.showerror("Error", f"Error inserting data: {e}")
        else:
            messagebox.showwarning("Input Error", "Please enter movie name and director.")

def delete_video():
    selected_item = video_tree.selection()
    if selected_item:
        selected_movie = video_tree.item(selected_item, "values")
        if selected_movie:
            movie_id = selected_movie[0]
            try:
                conn = connect_to_database()
                cursor = conn.cursor()
                sql = "DELETE FROM kiemtralan2.movies WHERE Movie_Id = %s"
                cursor.execute(sql, (movie_id,))
                conn.commit()
                cursor.close()
                conn.close()
                messagebox.showinfo("Success", "Video deleted successfully.")
                query_video_data()
            except Exception as e:
                messagebox.showerror("Error", f"Error deleting data: {e}")
    else:
        messagebox.showwarning("Select Movie", "Please select a movie to delete.")

def search_movie(event=None):
    search_query = entry_video_search.get()
    query_video_data(search_query)

# Tạo giao diện với Tkinter
root = Tk()
root.title("Nguyen Van Dat - 2286300010")
root.geometry("900x600")
root.configure(bg="#f0f0f0")

# ------------------ Khung bên trái cho Music ------------------
frame_left = Frame(root, bg="#f0f0f0")
frame_left.pack(side=LEFT, fill=Y, padx=10, pady=10)

# Label và ô nhập tìm kiếm cho nhạc
label_music_search = Label(frame_left, text="Search Music Name or Artist:", fg="purple", bg="#f0f0f0", font=("Arial", 14))
label_music_search.pack(pady=10)
entry_music_search = Entry(frame_left, font=("Arial", 14), width=25)
entry_music_search.pack(pady=10)
entry_music_search.bind("<Return>", query_music_data)

# Tạo khung cho các nút nhạc
frame_music_buttons = Frame(frame_left, bg="#f0f0f0")
frame_music_buttons.pack(pady=20)

# Nút truy vấn danh sách nhạc
button_music_query = Button(frame_music_buttons, text="Load Music List", command=query_music_data, bg="#87CEEB", fg="black", font=("Arial", 12))
button_music_query.grid(row=0, column=0, padx=5, pady=5)

# Nút phát nhạc từ đường dẫn
button_music_play = Button(frame_music_buttons, text="Play Selected Music", command=play_selected_music_data, bg="#87CEEB", fg="black", font=("Arial", 12))
button_music_play.grid(row=1, column=0, padx=5, pady=5)

# Nút tải lên nhạc
button_music_insert = Button(frame_music_buttons, text="Upload Music", command=upload_music, bg="#87CEEB", fg="black", font=("Arial", 12))
button_music_insert.grid(row=2, column=0, padx=5, pady=5)

# Nút xóa nhạc
button_music_delete = Button(frame_music_buttons, text="Delete Music", command=delete_music, bg="#FF6347", fg="white", font=("Arial", 12))
button_music_delete.grid(row=3, column=0, padx=5, pady=5)

# Nút dừng nhạc
button_music_stop = Button(frame_music_buttons, text="Stop Music", command=stop_music, bg="#FF6347", fg="white", font=("Arial", 12))
button_music_stop.grid(row=4, column=0, padx=5, pady=5)

# Tạo bảng cho danh sách nhạc
music_tree = ttk.Treeview(frame_left, columns=("Song_Id", "Song_name", "Artist", "Album"), show='headings', height=10)
music_tree.pack()
music_tree.heading("Song_Id", text="Song ID")
music_tree.heading("Song_name", text="Song Name")
music_tree.heading("Artist", text="Artist")
music_tree.heading("Album", text="Album")
music_tree.bind("<Double-1>", play_selected_music_data)

music_tree.column("Song_Id", width=70)
music_tree.column("Song_name", width=150)
music_tree.column("Artist", width=100)
music_tree.column("Album", width=100)
music_tree.pack(pady=10)

# ------------------ Khung bên phải cho Video ------------------
frame_right = Frame(root, bg="#f0f0f0")
frame_right.pack(side=RIGHT, fill=Y, padx=10, pady=10)

# Label và ô nhập tìm kiếm cho Video
label_video_search = Label(frame_right, text="Search Movie Name or Director:", fg="purple", bg="#f0f0f0", font=("Arial", 14))
label_video_search.pack(pady=10)
entry_video_search = Entry(frame_right, font=("Arial", 14), width=25)
entry_video_search.pack(pady=10)
entry_video_search.bind("<Return>", search_movie)

# Tạo khung cho các nút Video
frame_video_buttons = Frame(frame_right, bg="#f0f0f0")
frame_video_buttons.pack(pady=20)

# Nút truy vấn danh sách video
button_video_query = Button(frame_video_buttons, text="Load Video List", command=query_video_data, bg="#87CEEB", fg="black", font=("Arial", 12))
button_video_query.grid(row=0, column=0, padx=5, pady=5)

# Nút phát video từ đường dẫn
button_video_play = Button(frame_video_buttons, text="Play Selected Video", command=play_selected_video, bg="#87CEEB", fg="black", font=("Arial", 12))
button_video_play.grid(row=1, column=0, padx=5, pady=5)

# Nút tải lên video
button_video_insert = Button(frame_video_buttons, text="Upload Video", command=insert_video, bg="#87CEEB", fg="black", font=("Arial", 12))
button_video_insert.grid(row=2, column=0, padx=5, pady=5)

# Nút xóa video đã chọn
button_video_delete = Button(frame_video_buttons, text="Delete Video", command=delete_video, bg="#FF6347", fg="white", font=("Arial", 12))
button_video_delete.grid(row=3, column=0, padx=5, pady=5)

# Tạo bảng cho danh sách video
video_tree = ttk.Treeview(frame_right, columns=("Movie_Id", "Movie_name", "Director", "File_path"), show='headings', height=10)
video_tree.pack()
video_tree.heading("Movie_Id", text="Movie ID")
video_tree.heading("Movie_name", text="Movie Name")
video_tree.heading("Director", text="Director")
video_tree.heading("File_path", text="File Path")

video_tree.column("Movie_Id", width=70)
video_tree.column("Movie_name", width=100)
video_tree.column("Director", width=100)
video_tree.column("File_path", width=150)
video_tree.pack(pady=10)

# Chạy giao diện chính
root.mainloop()
