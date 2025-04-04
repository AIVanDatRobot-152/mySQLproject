from flask import Flask, render_template, request, redirect, flash, send_file
import mysql.connector
import pygame
import io
import tempfile
from moviepy.editor import *
import threading
import os

app = Flask(__name__)
app.secret_key = "your_secret_key"

# Kết nối tới cơ sở dữ liệu MySQL
def connect_to_database():
    return mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="SQLdat1502:3",
        database="kiemtralan2"
    )

# Hàm tải nhạc lên cơ sở dữ liệu
@app.route('/upload_music', methods=['POST'])
def upload_music():
    file = request.files['music_file']
    if file:
        file_data = file.read()
        file_name = file.filename
        conn = connect_to_database()
        cursor = conn.cursor()
        sql = "INSERT INTO songs (Song_name, Artist, Album, file_path) VALUES (%s, %s, %s, %s)"
        cursor.execute(sql, (file_name, "Unknown Artist", "Unknown Album", file_data))
        conn.commit()
        cursor.close()
        conn.close()
        flash('Music uploaded successfully!', 'success')
        return redirect('/')

# Hàm tải video lên cơ sở dữ liệu
@app.route('/upload_video', methods=['POST'])
def upload_video():
    file = request.files['video_file']
    if file:
        file_data = file.read()
        file_name = file.filename
        conn = connect_to_database()
        cursor = conn.cursor()
        sql = "INSERT INTO movies (Movie_name, Director, file_path) VALUES (%s, %s, %s)"
        cursor.execute(sql, (file_name, "Unknown Director", file_data))
        conn.commit()
        cursor.close()
        conn.close()
        flash('Video uploaded successfully!', 'success')
        return redirect('/')

# Lấy danh sách nhạc từ MySQL
@app.route('/get_music_list', methods=['GET'])
def get_music_list():
    conn = connect_to_database()
    cursor = conn.cursor()
    sql = "SELECT Song_Id, Song_name, Artist, Album FROM songs"
    cursor.execute(sql)
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('index.html', music_list=rows, video_list=get_video_list())

# Lấy danh sách video từ MySQL
def get_video_list():
    conn = connect_to_database()
    cursor = conn.cursor()
    sql = "SELECT Movie_Id, Movie_name, Director FROM movies"
    cursor.execute(sql)
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows

# Phát nhạc
@app.route('/play_music/<int:song_id>')
def play_music(song_id):
    conn = connect_to_database()
    cursor = conn.cursor()
    sql = "SELECT file_path FROM songs WHERE Song_Id = %s"
    cursor.execute(sql, (song_id,))
    row = cursor.fetchone()
    cursor.close()
    conn.close()

    if row:
        pygame.mixer.init()
        mp3_stream = io.BytesIO(row[0])
        pygame.mixer.music.load(mp3_stream, 'mp3')
        pygame.mixer.music.play()
        return 'Playing Music'
    else:
        flash('Music not found!', 'error')
        return redirect('/')

# Phát video
@app.route('/play_video/<int:movie_id>')
def play_video(movie_id):
    conn = connect_to_database()
    cursor = conn.cursor()
    sql = "SELECT file_path FROM movies WHERE Movie_Id = %s"
    cursor.execute(sql, (movie_id,))
    row = cursor.fetchone()
    cursor.close()
    conn.close()

    if row:
        with tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as temp_video_file:
            temp_video_file.write(row[0])
            temp_video_file_path = temp_video_file.name

        clip = VideoFileClip(temp_video_file_path)
        clip.preview()
        os.remove(temp_video_file_path)
        return 'Playing Video'
    else:
        flash('Video not found!', 'error')
        return redirect('/')

@app.route('/')
def index():
    return render_template('index.html', music_list=get_music_list(), video_list=get_video_list())

if __name__ == '__main__':
    app.run(debug=True)
