import mysql.connector
from tkinter import *
from tkinter import messagebox
import tempfile
from moviepy.editor import *
import threading

# Biến toàn cục để giữ video đang phát
current_video = None
video_thread = None

# Kết nối tới cơ sở dữ liệu MySQL
def connect_to_database():
    conn = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="SQLdat1502:3",
        database="kiemtralan2"  # Sửa đổi tên cơ sở dữ liệu
    )
    return conn

# Hàm phát video trong một thread riêng
def play_video_thread(video_data):
    global current_video, video_thread
    try:
        # Tạo file tạm cho video
        with tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as temp_video_file:
            temp_video_file.write(video_data)  # Lưu dữ liệu nhị phân vào file tạm
            temp_video_file_path = temp_video_file.name

        # Sử dụng MoviePy để phát video
        current_video = VideoFileClip(temp_video_file_path)
        current_video.preview()  # Phát video kèm âm thanh

    except Exception as e:
        messagebox.showerror("Error", f"Error playing video: {e}")

    finally:
        # Đặt lại video_thread khi video kết thúc
        video_thread = None

# Phát video và nhạc bằng cách chạy một thread
def play_video_and_music(video_data):
    global video_thread
    if video_thread is None:  # Kiểm tra xem có video nào đang phát không
        video_thread = threading.Thread(target=play_video_thread, args=(video_data,))
        video_thread.start()  # Bắt đầu thread phát video

# Dừng video
def stop_video():
    global current_video, video_thread
    if current_video is not None:
        current_video.close()  # Dừng và đóng video
        current_video = None  # Đặt lại biến để cho phép truy vấn video mới
        video_thread = None  # Đặt lại thread để cho phép video mới phát
        messagebox.showinfo("Stopped", "Video đã được dừng.")

# Truy vấn dữ liệu từ bảng dựa trên ID hoặc tên
def query_data(event=None):
    try:
        search_term = entry_search.get().strip()  # Lấy dữ liệu từ ô nhập liệu
        conn = connect_to_database()
        cursor = conn.cursor()

        # Truy vấn dữ liệu dựa trên ID hoặc tên
        if search_term.isdigit():
            sql = "SELECT Movie_Id, Movie_name, file_path, Director FROM movies WHERE Movie_Id = %s"
            cursor.execute(sql, (search_term,))
        else:
            sql = "SELECT Movie_Id, Movie_name, file_path, Director FROM movies WHERE Movie_name = %s"
            cursor.execute(sql, (search_term,))

        row = cursor.fetchone()

        if row:
            label_name.config(text=f"Name: {row[1]}")
            label_description.config(text=f"Director: {row[3]}")

            # Dừng video nếu đang phát trước khi phát video mới
            stop_video()

            # Phát video mới
            video_data = row[2]
            play_video_and_music(video_data)
        else:
            messagebox.showinfo("Not Found", "No data found for the given ID or Name.")
        
        cursor.close()
        conn.close()

    except Exception as e:
        messagebox.showerror("Error", f"Error fetching data: {e}")

# Tạo giao diện với Tkinter
root = Tk()
root.title("Video Query App")
root.geometry("400x400")

# Label và ô nhập ID hoặc tên
label_search = Label(root, text="Enter Movie ID or Name:")
label_search.pack(pady=10)
entry_search = Entry(root)
entry_search.pack(pady=10)
entry_search.bind("<Return>", query_data)  # Kích hoạt tìm kiếm bằng phím Enter

# Hiển thị tên và mô tả
label_name = Label(root, text="Name: ")
label_name.pack(pady=5)
label_description = Label(root, text="Director: ")
label_description.pack(pady=5)

# Nút truy vấn để phát video
button_query = Button(root, text="Truy vấn và phát video", command=query_data)
button_query.pack(pady=20)

# Nút dừng video
button_stop = Button(root, text="Dừng Video", command=stop_video)
button_stop.pack(pady=10)

# Nút thoát ứng dụng
button_quit = Button(root, text="Thoát", command=root.quit)
button_quit.pack(pady=10)

# Chạy giao diện
root.mainloop()
