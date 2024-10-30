import tkinter as tk
from tkinter import filedialog, messagebox
from moviepy.editor import VideoFileClip
import os

def video_to_audio(video_files, output_folder, audio_format):
    try:
        for video_file in video_files:
            clip = VideoFileClip(video_file)
            
            # Chỉnh độ tốc độ và âm lượng
            clip = clip.fx(lambda x: x.speedx(1.2))
            clip = clip.fx(lambda x: x.volumex(1.2))
            
            # Lưu âm thanh xuống file
            audio_file = os.path.join(output_folder, os.path.splitext(os.path.basename(video_file))[0] + audio_format)
            clip.audio.write_audiofile(audio_file)
            clip.close()
        
        messagebox.showinfo("Thành công", "Chuyển đổi video thành âm thanh thành công.")
    except Exception as e:
        messagebox.showerror("Lỗi", f"Lỗi khi chuyển đổi video thành âm thanh: {e}")

def select_video_files():
    filenames = filedialog.askopenfilenames(filetypes=[("Video files", "*.mp4;*.avi;*.mov;*.mkv;*.wmv;*.3gp")])
    if filenames:
        video_entry.delete("1.0", tk.END)
        for filename in filenames:
            video_entry.insert(tk.END, filename + "\n")

def select_output_folder():
    foldername = filedialog.askdirectory()
    if foldername:
        output_entry.delete(0, tk.END)
        output_entry.insert(0, foldername)

def start_conversion():
    video_files = video_entry.get("1.0", tk.END).strip().split("\n")
    output_folder = output_entry.get()
    audio_format = audio_format_var.get()  # Lấy định dạng âm thanh từ biến radio button

    if video_files and output_folder:
        video_to_audio(video_files, output_folder, audio_format)
    else:
        messagebox.showwarning("Cảnh báo", "Vui lòng chọn cả video và thư mục xuất âm thanh.")

def exit_app():
    root.destroy()

root = tk.Tk()
root.title("Chuyển đổi video thành âm thanh")

frame = tk.Frame(root, padx=20, pady=20)
frame.pack(padx=10, pady=10)

tk.Label(frame, text="Chọn video cần chuyển đổi:", wraplength=250, justify="left").grid(row=0, column=0, sticky="w")
video_entry = tk.Text(frame, width=50, height=4)
video_entry.grid(row=0, column=1, padx=10)
tk.Button(frame, text="Browser", command=select_video_files, bg = "lightgreen", fg="black").grid(row=0, column=2)

tk.Label(frame, text="Thư mục xuất âm thanh:").grid(row=1, column=0, sticky="w")
output_entry = tk.Entry(frame, width=50)
output_entry.grid(row=1, column=1, padx=10)
tk.Button(frame, text="Browser", command=select_output_folder, bg = "lightgreen", fg="black").grid(row=1, column=2)

tk.Label(frame, text="Định dạng âm thanh:").grid(row=2, column=0, sticky="w")
audio_format_var = tk.StringVar()
audio_format_var.set(".mp3")  # Mặc định chọn định dạng MP3
formats = [(".mp3", "MP3"), (".wav", "WAV"), (".ogg", "OGG")]
for i, (format_ext, format_name) in enumerate(formats):
    tk.Radiobutton(frame, text=format_name, variable=audio_format_var, value=format_ext).grid(row=2, column=i+1)

tk.Button(frame, text="Bắt đầu tiến hành", command=start_conversion, bg = "yellow", fg="black").grid(row=3, column=1, pady=20)
tk.Button(frame, text="Thoát", command=exit_app, bg = "grey", fg="black").grid(row=3, column=2, pady=20)

root.mainloop()
