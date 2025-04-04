from flask import Flask, render_template, request, jsonify
import mysql.connector
import os
import io
import pygame
import subprocess

app = Flask(__name__)

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

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/query_music', methods=['GET'])
def query_music():
    search_value = request.args.get('search_value', '')
    try:
        conn = connect_to_database()
        cursor = conn.cursor()
        
        if search_value:
            sql = "SELECT Song_Id, Song_name, Artist, Album FROM songs WHERE Song_Id LIKE %s OR Song_name LIKE %s"
            cursor.execute(sql, (f"%{search_value}%", f"%{search_value}%"))
        else:
            sql = "SELECT Song_Id, Song_name, Artist, Album FROM songs"
            cursor.execute(sql)

        songs = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(songs)
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route('/play_music/<int:song_id>', methods=['GET'])
def play_music(song_id):
    try:
        conn = connect_to_database()
        cursor = conn.cursor()
        cursor.execute("SELECT file_data, file_path FROM songs WHERE Song_Id = %s", (song_id,))
        row = cursor.fetchone()
        cursor.close()
        conn.close()
        if row:
            song_data, file_path = row
            if song_data:
                play_music_from_data(song_data)  # Chơi nhạc từ dữ liệu
            else:
                play_music_from_path(file_path)  # Chơi nhạc từ đường dẫn
            return jsonify({"success": True})
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route('/upload_music', methods=['POST'])
def upload_music():
    song_name = request.form['song_name']
    artist = request.form['artist']
    album = request.form['album']
    file = request.files['file']

    if file and file.filename.endswith('.mp3'):
        file_data = file.read()
        file_path = os.path.join("uploads", file.filename)  # Đường dẫn lưu file
        with open(file_path, 'wb') as f:
            f.write(file_data)
        
        try:
            conn = connect_to_database()
            cursor = conn.cursor()
            sql = "INSERT INTO songs (Song_name, Artist, Album, file_data, file_path) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(sql, (song_name, artist, album, file_data, file_path))
            conn.commit()
            cursor.close()
            conn.close()
            return jsonify({"success": True})
        except Exception as e:
            return jsonify({"error": str(e)})
    return jsonify({"error": "Invalid file type."})

@app.route('/delete_music/<int:song_id>', methods=['DELETE'])
def delete_music(song_id):
    try:
        conn = connect_to_database()
        cursor = conn.cursor()
        sql = "DELETE FROM songs WHERE Song_Id = %s"
        cursor.execute(sql, (song_id,))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"error": str(e)})

# ------------------ Phần giao diện Video ------------------

@app.route('/query_video', methods=['GET'])
def query_video():
    search_value = request.args.get('search_value', '')
    try:
        conn = connect_to_database()
        cursor = conn.cursor()
        
        if search_value:
            sql = "SELECT Movie_Id, Movie_name, Director FROM movies WHERE Movie_name LIKE %s OR Director LIKE %s"
            cursor.execute(sql, (f"%{search_value}%", f"%{search_value}%"))
        else:
            sql = "SELECT Movie_Id, Movie_name, Director FROM movies"
            cursor.execute(sql)

        movies = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(movies)
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route('/play_video/<int:movie_id>', methods=['GET'])
def play_video(movie_id):
    try:
        conn = connect_to_database()
        cursor = conn.cursor()
        cursor.execute("SELECT file_path FROM movies WHERE Movie_Id = %s", (movie_id,))
        row = cursor.fetchone()
        cursor.close()
        conn.close()
        if row:
            file_path = row[0]
            play_video_from_path(file_path)  # Chơi video từ đường dẫn
            return jsonify({"success": True})
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route('/upload_video', methods=['POST'])
def upload_video():
    movie_name = request.form['movie_name']
    director = request.form['director']
    file = request.files['file']

    if file and file.filename.endswith(('.mp4', '.avi', '.mkv', '.mov')):
        file_path = os.path.join("uploads", file.filename)
        file.save(file_path)

        try:
            conn = connect_to_database()
            cursor = conn.cursor()
            sql = "INSERT INTO movies (Movie_name, Director, file_path) VALUES (%s, %s, %s)"
            cursor.execute(sql, (movie_name, director, file_path))
            conn.commit()
            cursor.close()
            conn.close()
            return jsonify({"success": True})
        except Exception as e:
            return jsonify({"error": str(e)})
    return jsonify({"error": "Invalid file type."})

@app.route('/delete_video/<int:movie_id>', methods=['DELETE'])
def delete_video(movie_id):
    try:
        conn = connect_to_database()
        cursor = conn.cursor()
        sql = "DELETE FROM movies WHERE Movie_Id = %s"
        cursor.execute(sql, (movie_id,))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"error": str(e)})

def play_music_from_data(song_data):
    pygame.mixer.init()
    mp3_stream = io.BytesIO(song_data)
    pygame.mixer.music.load(mp3_stream)
    pygame.mixer.music.play()

def play_music_from_path(file_path):
    if os.path.exists(file_path):
        subprocess.run(["start", "", file_path], shell=True)

def play_video_from_path(file_path):
    if os.path.exists(file_path):
        subprocess.run(["start", "", file_path], shell=True)

if __name__ == '__main__':
    app.run(debug=True)
