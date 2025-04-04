import mysql.connector
from tkinter import *
from tkinter import messagebox, filedialog
import pygame
import io
import tempfile
from moviepy.editor import *
import threading

# Kết nối tới cơ sở dữ liệu MySQL
def connect_to_database():
    return mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="SQLdat1502:3",
        database="kiemtralan2"
    )

# Biến toàn cục để giữ video và nhạc đang phát
current_video = None
video_thread = None

# Hàm phát video trong một thread riêng
def play_video_thread(video_data):
    global current_video, video_thread
    try:
        with tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as temp_video_file:
            temp_video_file.write(video_data)
            temp_video_file_path = temp_video_file.name

        current_video = VideoFileClip(temp_video_file_path)
        current_video.preview()
    except Exception as e:
        messagebox.showerror("Error", f"Error playing video: {e}")
    finally:
        video_thread = None

# Phát video
def play_video(video_data):
    global video_thread
    if video_thread is None:
        video_thread = threading.Thread(target=play_video_thread, args=(video_data,))
        video_thread.start()

# Dừng video
def stop_video():
    global current_video, video_thread
    if current_video is not None:
        current_video.close()
        current_video = None
        video_thread = None
        messagebox.showinfo("Stopped", "Video đã được dừng.")

# Phát nhạc
def play_music(songs):
    pygame.mixer.init()
    mp3_stream = io.BytesIO(songs)
    pygame.mixer.music.load(mp3_stream, 'mp3')
    pygame.mixer.music.play()

# Dừng nhạc
def stop_music():
    if pygame.mixer.music.get_busy():
        pygame.mixer.music.stop()

# Tạm dừng nhạc
def pause_music():
    if pygame.mixer.music.get_busy():
        pygame.mixer.music.pause()

# Tiếp tục phát nhạc
def unpause_music():
    if pygame.mixer.music.get_busy():
        pygame.mixer.music.unpause()

# Truy vấn dữ liệu âm nhạc từ bảng
def query_music():
    try:
        search_term = entry_music_search.get().strip()
        conn = connect_to_database()
        cursor = conn.cursor()

        if search_term.isdigit():
            sql = "SELECT Song_Id, Song_name, Artist, Album, file_path FROM songs WHERE Song_Id = %s"
            cursor.execute(sql, (search_term,))
        else:
            sql = "SELECT Song_Id, Song_name, Artist, Album, file_path FROM songs WHERE Song_name = %s"
            cursor.execute(sql, (search_term,))

        row = cursor.fetchone()

        if row:
            label_music_name.config(text=f"Name: {row[1]}", fg="blue")
            label_music_artist.config(text=f"Artist: {row[2]}", fg="purple")
            label_music_album.config(text=f"Album: {row[3]}", fg="green")

            # Phát nhạc
            songs = row[4]
            play_music(songs)
        else:
            messagebox.showinfo("Not Found", "No music found for the given ID or Name.")
        
        cursor.close()
        conn.close()

    except Exception as e:
        messagebox.showerror("Error", f"Error fetching music data: {e}")

# Truy vấn dữ liệu video từ bảng
def query_video():
    try:
        search_term = entry_movie_search.get().strip()
        conn = connect_to_database()
        cursor = conn.cursor()

        if search_term.isdigit():
            sql = "SELECT Movie_Id, Movie_name, Director, file_path FROM movies WHERE Movie_Id = %s"
            cursor.execute(sql, (search_term,))
        else:
            sql = "SELECT Movie_Id, Movie_name, Director, file_path FROM movies WHERE Movie_name = %s"
            cursor.execute(sql, (search_term,))

        row = cursor.fetchone()

        if row:
            label_movie_name.config(text=f"Name: {row[1]}", fg="blue")
            label_movie_director.config(text=f"Director: {row[2]}", fg="green")

            # Dừng video nếu đang phát trước khi phát video mới
            stop_video()

            # Phát video mới
            video_data = row[3]
            play_video(video_data)
        else:
            messagebox.showinfo("Not Found", "No movie found for the given ID or Name.")
        
        cursor.close()
        conn.close()

    except Exception as e:
        messagebox.showerror("Error", f"Error fetching video data: {e}")

# Tải lên file âm nhạc
def upload_music():
    file_path = filedialog.askopenfilename(filetypes=[("Audio Files", "*.mp3")])
    if file_path:
        with open(file_path, "rb") as file:
            music_data = file.read()
            conn = connect_to_database()
            cursor = conn.cursor()
            sql = "INSERT INTO songs (Song_name, Artist, Album, file_path) VALUES (%s, %s, %s, %s)"
            cursor.execute(sql, (file_path.split("/")[-1], "Unknown Artist", "Unknown Album", music_data))
            conn.commit()
            cursor.close()
            conn.close()
            messagebox.showinfo("Upload Success", "Music uploaded successfully.")

# Tải lên file video
def upload_video():
    file_path = filedialog.askopenfilename(filetypes=[("Video Files", "*.mp4")])
    if file_path:
        with open(file_path, "rb") as file:
            video_data = file.read()
            conn = connect_to_database()
            cursor = conn.cursor()
            sql = "INSERT INTO movies (Movie_name, Director, file_path) VALUES (%s, %s, %s)"
            cursor.execute(sql, (file_path.split("/")[-1], "Unknown Director", video_data))
            conn.commit()
            cursor.close()
            conn.close()
            messagebox.showinfo("Upload Success", "Video uploaded successfully.")

# Tạo giao diện với Tkinter
root = Tk()
root.title("Media Query App")
root.geometry("800x600")

# Khung cho giao diện chính
frame_main = Frame(root, borderwidth=5, relief="solid")
frame_main.pack(expand=True, fill=BOTH, padx=10, pady=10)

# Khung bên trái cho nhạc
frame_music = Frame(frame_main, width=400)
frame_music.pack(side=LEFT, fill=Y, padx=5)

label_music_search = Label(frame_music, text="Search Music (ID/Name):")
label_music_search.pack(pady=10)
entry_music_search = Entry(frame_music, width=30)
entry_music_search.pack(pady=10)
button_music_query = Button(frame_music, text="Play Music", command=query_music)
button_music_query.pack(pady=10)
button_music_upload = Button(frame_music, text="Upload Music", command=upload_music)
button_music_upload.pack(pady=10)

label_music_name = Label(frame_music, text="Name: ", fg="black")
label_music_name.pack(pady=5)
label_music_artist = Label(frame_music, text="Artist: ", fg="black")
label_music_artist.pack(pady=5)
label_music_album = Label(frame_music, text="Album: ", fg="black")
label_music_album.pack(pady=5)

# Khung bên phải cho video
frame_video = Frame(frame_main, width=400)
frame_video.pack(side=RIGHT, fill=Y, padx=5)

label_movie_search = Label(frame_video, text="Search Movie (ID/Name):")
label_movie_search.pack(pady=10)
entry_movie_search = Entry(frame_video, width=30)
entry_movie_search.pack(pady=10)
button_movie_query = Button(frame_video, text="Play Movie", command=query_video)
button_movie_query.pack(pady=10)
button_movie_upload = Button(frame_video, text="Upload Movie", command=upload_video)
button_movie_upload.pack(pady=10)

label_movie_name = Label(frame_video, text="Name: ", fg="black")
label_movie_name.pack(pady=5)
label_movie_director = Label(frame_video, text="Director: ", fg="black")
label_movie_director.pack(pady=5)

# Chạy ứng dụng
root.mainloop()
