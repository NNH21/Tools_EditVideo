import tkinter as tk
from tkinter import filedialog, messagebox
import os
import moviepy.editor as mp

def chon_video():
    duong_dan_video = filedialog.askopenfilename(filetypes=[
        ("Tất cả các định dạng hỗ trợ", "*.mp4;*.wmv;*.hevc;*.avl;*.mov;*.f4v;*.mkv;*.ts;*.3gp;*.mpeg-2;*.webm;*.gif;*.mp3"),
        ("Tất cả các tệp", "*.*")])
    if duong_dan_video:
        video_entry.delete(0, tk.END)
        video_entry.insert(0, duong_dan_video)
        global duong_dan_video_chon
        duong_dan_video_chon = duong_dan_video

def chon_thu_muc():
    duong_dan_thu_muc = filedialog.askdirectory()
    if duong_dan_thu_muc:
        folder_entry.delete(0, tk.END)
        folder_entry.insert(0, duong_dan_thu_muc)
        global duong_dan_thu_muc_xuat
        duong_dan_thu_muc_xuat = duong_dan_thu_muc

def chon_am_thanh():
    global duong_dan_am_thanh
    duong_dan_am_thanh = filedialog.askopenfilename(filetypes=[
        ("Tất cả các định dạng âm thanh", "*.mp3;*.wav;*.flac;*.aac;*.ogg;*.m4a;*.aiff;*.wma"),
        ("Tất cả các tệp", "*.*")])
    if duong_dan_am_thanh:
        audio_entry.delete(0, tk.END)
        audio_entry.insert(0, duong_dan_am_thanh)

def chon_dinh_dang_video(value):
    global dinh_dang_video
    dinh_dang_video = value

def chuyen_doi_video():
    if not duong_dan_video_chon or not duong_dan_thu_muc_xuat:
        tk.messagebox.showerror("Lỗi", "Vui lòng chọn video và thư mục xuất trước khi bắt đầu tiến hành")
        return
    
    ten_file = ten_file_entry.get().strip()  # Lấy tên file từ entry
    if not ten_file:
        tk.messagebox.showerror("Lỗi", "Vui lòng nhập tên cho file chuyển đổi")
        return
    
    video_name = os.path.basename(duong_dan_video_chon)
    video_output_path = os.path.join(duong_dan_thu_muc_xuat, f"{ten_file}{dinh_dang_video}")
    clip = mp.VideoFileClip(duong_dan_video_chon)
    
    if duong_dan_am_thanh:
        try:
            audio_clip = mp.AudioFileClip(duong_dan_am_thanh)
            audio_duration = audio_clip.duration
            video_duration = clip.duration
            if audio_duration < video_duration:
                tk.messagebox.showwarning("Cảnh báo", "Độ dài của âm thanh ngắn hơn độ dài của video. Video sẽ được cắt ngắn lại.")
                clip = clip.subclip(0, audio_duration)
            else:
                audio_clip = audio_clip.subclip(0, video_duration)  # Cắt âm thanh theo độ dài của video
            clip = clip.set_audio(audio_clip)
        except Exception as e:
            tk.messagebox.showwarning("Cảnh báo", f"Lỗi khi thêm âm thanh vào video: {e}")
    
    try:
        clip.write_videofile(video_output_path, preset='superfast')  # Tăng tốc độ chuyển đổi ở đây
        clip.close()
        tk.messagebox.showinfo("Thông báo", f"Đã chuyển đổi và lưu video xuất ra tại: {video_output_path}")
    except Exception as e:
        tk.messagebox.showerror("Lỗi", f"Lỗi khi chuyển đổi và lưu video: {e}")

def thoat_chuong_trinh():
    root.destroy()

# Tạo cửa sổ chính
root = tk.Tk()
root.title("Công Cụ Xử Lý Video")

# Kích thước của cửa sổ và vị trí ban đầu
root.geometry("600x330")

# Label và Entry cho việc nhập đường dẫn video
label_nhap_video = tk.Label(root, text="Nhập đường dẫn video:")
label_nhap_video.grid(row=0, column=0, padx=10, pady=10)

video_entry = tk.Entry(root, width=50)
video_entry.grid(row=0, column=1, padx=10, pady=10)

video_button = tk.Button(root, text="Browser", command=chon_video, bg = "lightgreen", fg="black")
video_button.grid(row=0, column=2, padx=10, pady=10)

# Label và Entry cho việc nhập đường dẫn thư mục xuất
label_nhap_thu_muc = tk.Label(root, text="Nhập đường dẫn thư mục xuất:")
label_nhap_thu_muc.grid(row=1, column=0, padx=10, pady=10)

folder_entry = tk.Entry(root, width=50)
folder_entry.grid(row=1, column=1, padx=10, pady=10)

folder_button = tk.Button(root, text="Browser", command=chon_thu_muc, bg = "lightgreen", fg="black")
folder_button.grid(row=1, column=2, padx=10, pady=10)

# Label và Entry cho việc chọn đường dẫn âm thanh
label_nhap_am_thanh = tk.Label(root, text="Chọn âm thanh sau khi chuyển đổi:")
label_nhap_am_thanh.grid(row=2, column=0, padx=10, pady=10)

audio_entry = tk.Entry(root, width=50)
audio_entry.grid(row=2, column=1, padx=10, pady=10)

audio_button = tk.Button(root, text="Browser", command=chon_am_thanh, bg = "lightgreen", fg="black")
audio_button.grid(row=2, column=2, padx=10, pady=10)

# Label và Dropdown cho chọn định dạng video đầu ra
label_dinh_dang_video = tk.Label(root, text="Chọn định dạng video đầu ra:")
label_dinh_dang_video.grid(row=3, column=0, padx=10, pady=10)

dinh_dang_video_var = tk.StringVar()
dinh_dang_video_var.set(".mp4")  # Mặc định chọn định dạng MP4
dinh_dang_video_dropdown = tk.OptionMenu(root, dinh_dang_video_var, ".mp4", ".avi", ".mov", command=chon_dinh_dang_video)
dinh_dang_video_dropdown.grid(row=3, column=1, padx=10, pady=10)
dinh_dang_video_dropdown.config(width=10)

# Label và Entry cho việc nhập tên file
label_ten_file = tk.Label(root, text="Nhập tên cho file chuyển đổi:")
label_ten_file.grid(row=4, column=0, padx=10, pady=10)

ten_file_entry = tk.Entry(root, width=50)
ten_file_entry.grid(row=4, column=1, padx=10, pady=10)

# Button để bắt đầu tiến hành chuyển đổi
start_button = tk.Button(root, text="Bắt đầu tiến hành", command=chuyen_doi_video, bg = "yellow", fg="black")
start_button.grid(row=5, columnspan=3, padx=10, pady=10)

# Button để thoát chương trình
exit_button = tk.Button(root, text="Thoát", command=thoat_chuong_trinh, bg = "grey", fg="black")
exit_button.grid(row=6, columnspan=3, padx=10, pady=10)

# Biến lưu đường dẫn video và thư mục xuất đã chọn
duong_dan_video_chon = None
duong_dan_thu_muc_xuat = None
duong_dan_am_thanh = None
dinh_dang_video = ".mp4"  # Định dạng video mặc định


root.mainloop()
