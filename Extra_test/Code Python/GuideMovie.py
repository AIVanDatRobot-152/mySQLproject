import mysql.connector
from tkinter import *
from tkinter import messagebox, ttk, filedialog
import subprocess
import os

# Kết nối tới cơ sở dữ liệu MySQL
def connect_to_database():
    conn = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="SQLdat1502:3",
        database="kiemtralan2"
    )
    return conn

# Phát video bằng file_path
def play_video(file_path):
    if os.path.exists(file_path):
        subprocess.run(["start", "", file_path], shell=True)  # Dùng "start" để mở file
    else:
        messagebox.showerror("Error", "File path does not exist.")

# Truy vấn dữ liệu từ bảng và hiển thị danh sách phim
def query_data(search_query=None):
    try:
        conn = connect_to_database()
        cursor = conn.cursor()

        # Truy vấn dữ liệu từ bảng movies với điều kiện tìm kiếm
        if search_query:
            sql = "SELECT Movie_Id, Movie_name, Director, file_path FROM kiemtralan2.movies WHERE Movie_name LIKE %s OR Director LIKE %s OR Movie_Id LIKE %s"
            cursor.execute(sql, ('%' + search_query + '%', '%' + search_query + '%', '%' + search_query + '%'))
        else:
            sql = "SELECT Movie_Id, Movie_name, Director, file_path FROM kiemtralan2.movies"
            cursor.execute(sql)

        # Xóa dữ liệu cũ trong danh sách phim
        for row in tree.get_children():
            tree.delete(row)

        # Lưu danh sách phim
        for row in cursor.fetchall():
            tree.insert("", "end", values=row)  # Thêm dữ liệu vào Treeview

        cursor.close()
        conn.close()

    except Exception as e:
        messagebox.showerror("Error", f"Error fetching data: {e}")

# Phát video từ dòng đã chọn
def play_selected_video():
    selected_item = tree.selection()
    if selected_item:
        selected_movie = tree.item(selected_item, "values")
        if selected_movie:
            file_path = selected_movie[3]  # Lấy file_path từ dòng đã chọn
            play_video(file_path)
    else:
        messagebox.showwarning("Select Movie", "Please select a movie to play.")

# Chèn video vào cơ sở dữ liệu
def insert_video():
    file_path = filedialog.askopenfilename(filetypes=[("Video Files", "*.mp4;*.avi;*.mkv;*.mov")])
    if file_path:
        movie_name = entry_name.get()
        director_name = entry_director.get()

        if movie_name and director_name:
            try:
                conn = connect_to_database()
                cursor = conn.cursor()

                # Chèn video vào cơ sở dữ liệu
                sql = "INSERT INTO kiemtralan2.movies (Movie_name, Director, file_path) VALUES (%s, %s, %s)"
                cursor.execute(sql, (movie_name, director_name, file_path))
                conn.commit()
                cursor.close()
                conn.close()
                messagebox.showinfo("Success", "Video added successfully.")
                query_data()  # Cập nhật danh sách phim
            except Exception as e:
                messagebox.showerror("Error", f"Error inserting data: {e}")
        else:
            messagebox.showwarning("Input Error", "Please enter movie name and director.")

# Xóa video từ cơ sở dữ liệu
def delete_video():
    selected_item = tree.selection()
    if selected_item:
        selected_movie = tree.item(selected_item, "values")
        if selected_movie:
            movie_id = selected_movie[0]  # Lấy Movie_Id từ dòng đã chọn
            try:
                conn = connect_to_database()
                cursor = conn.cursor()

                # Xóa video khỏi cơ sở dữ liệu
                sql = "DELETE FROM kiemtralan2.movies WHERE Movie_Id = %s"
                cursor.execute(sql, (movie_id,))
                conn.commit()
                cursor.close()
                conn.close()
                messagebox.showinfo("Success", "Video deleted successfully.")
                query_data()  # Cập nhật danh sách phim
            except Exception as e:
                messagebox.showerror("Error", f"Error deleting data: {e}")
    else:
        messagebox.showwarning("Select Movie", "Please select a movie to delete.")

# Tìm kiếm phim theo ID, tên phim hoặc tác giả
def search_movie(event=None):
    search_query = entry_search.get()
    query_data(search_query)

# Tạo giao diện với Tkinter
root = Tk()
root.title("Movie Query App")
root.geometry("800x600")
root.configure(bg="#f0f0f0")  # Màu nền

# Tạo khung bên trái cho thông tin video và các nút
frame_left = Frame(root, bg="#f0f0f0")
frame_left.pack(side=LEFT, fill=Y, padx=10, pady=10)

# Label và ô nhập tìm kiếm
label_search = Label(frame_left, text="Search Movie ID, Name, or Director:", fg="purple", bg="#f0f0f0", font=("Arial", 14))
label_search.pack(pady=10)
entry_search = Entry(frame_left, font=("Arial", 14), width=25)
entry_search.pack(pady=10)
entry_search.bind("<Return>", search_movie)  # Kích hoạt tìm kiếm bằng phím Enter

# Label và ô nhập tên phim và đạo diễn
label_name = Label(frame_left, text="ADD Movie Name:", fg="purple", bg="#f0f0f0", font=("Arial", 14))
label_name.pack(pady=10)
entry_name = Entry(frame_left, font=("Arial", 14), width=25)
entry_name.pack(pady=10)

label_director = Label(frame_left, text="ADD Director Name:", fg="purple", bg="#f0f0f0", font=("Arial", 14))
label_director.pack(pady=10)
entry_director = Entry(frame_left, font=("Arial", 14), width=25)
entry_director.pack(pady=10)

# Tạo khung cho các nút tương tác
frame_buttons = Frame(frame_left, bg="#f0f0f0")
frame_buttons.pack(pady=20)

# Nút truy vấn danh sách phim
button_query = Button(frame_buttons, text="Load Movie List", command=query_data, bg="#87CEEB", fg="black", font=("Arial", 12))
button_query.grid(row=0, column=0, padx=5, pady=5)

# Nút chèn video
button_insert = Button(frame_buttons, text="Insert Video", command=insert_video, bg="#87CEEB", fg="black", font=("Arial", 12))
button_insert.grid(row=1, column=0, padx=5, pady=5)

# Nút phát video từ phim đã chọn
button_play = Button(frame_buttons, text="Play Video", command=play_selected_video, bg="#87CEEB", fg="black", font=("Arial", 12))
button_play.grid(row=2, column=0, padx=5, pady=5)

# Nút xóa video đã chọn
button_delete = Button(frame_buttons, text="Delete Video", command=delete_video, bg="#87CEEB", fg="black", font=("Arial", 12))
button_delete.grid(row=3, column=0, padx=5, pady=5)

# Tạo khung bên phải cho danh sách phim
frame_right = Frame(root, bg="#f0f0f0")
frame_right.pack(side=RIGHT, fill=BOTH, expand=True, padx=10, pady=10)

# Tạo Treeview để hiển thị danh sách phim
tree = ttk.Treeview(frame_right, columns=("Movie_Id", "Movie_name", "Director", "file_path"), show="headings")
tree.heading("Movie_Id", text="ID")
tree.heading("Movie_name", text="Name")
tree.heading("Director", text="Director")
tree.heading("file_path", text="File Path")

# Đặt chiều rộng cho các cột
tree.column("Movie_Id", width=70)
tree.column("Movie_name", width=100)
tree.column("Director", width=150)
tree.column("file_path", width=150)

# Thêm thanh cuộn cho Treeview
scrollbar = ttk.Scrollbar(frame_right, orient=VERTICAL, command=tree.yview)
tree.configure(yscroll=scrollbar.set)
scrollbar.pack(side=RIGHT, fill=Y)

tree.pack(fill=BOTH, expand=True)

# Chạy giao diện
root.mainloop()
