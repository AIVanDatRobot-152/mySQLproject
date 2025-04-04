import mysql.connector
from flask import Flask, render_template, request, jsonify
import io
import pygame

# Tạo một ứng dụng Flask
app = Flask(__name__)

# Kết nối đến cơ sở dữ liệu MySQL
def connect_to_database():
    conn = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="SQLdat1502:3",
        database="music_data"
    )
    return conn

# Trang chính
@app.route('/')
def index():
    return render_template('index.html')

# Truy vấn dữ liệu và phát nhạc
@app.route('/query', methods=['POST'])
def query_data():
    music_id = request.form.get('music_id')
    music_name = request.form.get('music_name')
    
    try:
        conn = connect_to_database()
        cursor = conn.cursor()

        # Truy vấn dữ liệu theo ID hoặc tên
        sql = "SELECT Music_Id, Music_name, Music_data, Description_Music FROM music_data WHERE Music_Id = %s OR Music_name = %s"
        cursor.execute(sql, (music_id, music_name))
        row = cursor.fetchone()

        if row:
            music_data = row[2]
            mp3_stream = io.BytesIO(music_data)
            pygame.mixer.init()
            pygame.mixer.music.load(mp3_stream, 'mp3')
            pygame.mixer.music.play()
            return jsonify({
                "status": "success",
                "name": row[1],
                "description": row[3]
            })
        else:
            return jsonify({"status": "error", "message": "No data found for the given ID or name."})

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})
    finally:
        cursor.close()
        conn.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4444)  # Chạy ứng dụng trên địa chỉ IP của máy chủ
