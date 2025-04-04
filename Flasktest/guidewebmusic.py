from flask import Flask, render_template, request, send_file, Response
import mysql.connector
from io import BytesIO

app = Flask(__name__)

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

@app.route('/')
def home():
    return render_template('index.html')

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
