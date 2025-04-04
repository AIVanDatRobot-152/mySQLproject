from flask import Flask, render_template, request, Response
import mysql.connector
from io import BytesIO
import pygame

app = Flask(__name__)

# Kết nối tới cơ sở dữ liệu MySQL
def create_connection():
    connection = None
    try:
        connection = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password="SQLdat1502:3",
            database="imager_data"
        )
        if connection.is_connected():
            print("Kết nối thành công")
    except mysql.connector.Error as e:
        print(f"Lỗi khi kết nối MySQL: {e}")
    return connection

# Truy xuất dữ liệu âm thanh từ MySQL bằng ID
def retrieve_audio_by_id(connection, audio_id):
    try:
        cursor = connection.cursor()
        sql_query = "SELECT Music_data FROM music_data WHERE Music_Id = %s"
        cursor.execute(sql_query, (audio_id,))
        result = cursor.fetchone()
        if result:
            return BytesIO(result[0])
        else:
            return None
    except mysql.connector.Error as e:
        print(f"Lỗi khi truy xuất âm thanh: {e}")
        return None

# Route cho trang chủ với giao diện tìm kiếm
@app.route('/')
def home():
    return render_template('home.html')

# Route để phát nhạc dựa trên ID
@app.route('/play', methods=['POST'])
def play():
    audio_id = request.form['audio_id']
    connection = create_connection()
    if connection and audio_id:
        audio_data = retrieve_audio_by_id(connection, audio_id)
        connection.close()
        if audio_data:
            return Response(audio_data, mimetype='audio/mpeg')
        else:
            return "Không tìm thấy âm thanh với ID đã nhập", 404
    else:
        return "Kết nối MySQL không thành công hoặc ID âm thanh không hợp lệ", 400

if __name__ == '__main__':
    app.run(debug=True)
