from flask import Flask, render_template, request, redirect, url_for, send_file, flash
import mysql.connector
import io
import tempfile
from moviepy.editor import VideoFileClip
import pygame
import threading

app = Flask(__name__)

# Kết nối tới cơ sở dữ liệu MySQL
def connect_to_database():
    return mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="SQLdat1502:3",
        database="kiemtralan2"
    )

# Tải nhạc lên cơ sở dữ liệu
@app.route('/upload_music', methods=['POST'])
def upload_music():
    file = request.files['file']
    if file:
        try:
            music_data = file.read()
            conn = connect_to_database()
            cursor = conn.cursor()
            sql = "INSERT INTO songs (Song_name, Artist, Album, file_path) VALUES (%s, %s, %s, %s)"
            cursor.execute(sql, (file.filename, "Unknown Artist", "Unknown Album", music_data))
            conn.commit()
            flash("Music uploaded successfully.")
        except Exception as e:
            flash(f"Error uploading music: {e}")
        finally:
            cursor.close()
            conn.close()
    return redirect(url_for('index'))

# Tải video lên cơ sở dữ liệu
@app.route('/upload_video', methods=['POST'])
def upload_video():
    file = request.files['file']
    if file:
        try:
            video_data = file.read()
            conn = connect_to_database()
            cursor = conn.cursor()
            sql = "INSERT INTO movies (Movie_name, Director, file_path) VALUES (%s, %s, %s)"
            cursor.execute(sql, (file.filename, "Unknown Director", video_data))
            conn.commit()
            flash("Video uploaded successfully.")
        except Exception as e:
            flash(f"Error uploading video: {e}")
        finally:
            cursor.close()
            conn.close()
    return redirect(url_for('index'))

# Lấy danh sách nhạc từ bảng
@app.route('/get_music_list')
def get_music_list():
    try:
        conn = connect_to_database()
        cursor = conn.cursor()
        sql = "SELECT Song_Id, Song_name, Artist, Album FROM songs"
        cursor.execute(sql)
        music_list = cursor.fetchall()
    except Exception as e:
        music_list = []
        flash(f"Error fetching music list: {e}")
    finally:
        cursor.close()
        conn.close()
    return music_list

# Lấy danh sách video từ bảng
@app.route('/get_movie_list')
def get_movie_list():
    try:
        conn = connect_to_database()
        cursor = conn.cursor()
        sql = "SELECT Movie_Id, Movie_name, Director FROM movies"
        cursor.execute(sql)
        movie_list = cursor.fetchall()
    except Exception as e:
        movie_list = []
        flash(f"Error fetching movie list: {e}")
    finally:
        cursor.close()
        conn.close()
    return movie_list

# Trang chính
@app.route('/')
def index():
    music_list = get_music_list()
    movie_list = get_movie_list()
    return render_template('guide.html', music_list=music_list, movie_list=movie_list)

if __name__ == '__main__':
    app.run(debug=True)
