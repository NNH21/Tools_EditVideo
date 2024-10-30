import tkinter as tk
from tkinter import filedialog, messagebox
import os
import moviepy.editor as mp

class VideoSplitterApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Chia Video Thời Gian Bằng Nhau")
        self.geometry("400x350")

        self.process = None

        # Đường dẫn video
        self.video_path_var = tk.StringVar()
        self.output_dir_var = tk.StringVar()

        # Button và Entry để chọn file video
        tk.Label(self, text="Chọn Video:").pack(pady=5)
        video_frame = tk.Frame(self)
        video_frame.pack(pady=5)
        tk.Entry(video_frame, textvariable=self.video_path_var, width=50).pack(side=tk.LEFT, padx=5)
        tk.Button(video_frame, text="Browse", command=self.choose_video, bg = "lightgreen", fg="black").pack(side=tk.LEFT)

        # Button và Entry để chọn thư mục xuất file
        tk.Label(self, text="Chọn Thư Mục Xuất File:").pack(pady=5)
        output_frame = tk.Frame(self)
        output_frame.pack(pady=5)
        tk.Entry(output_frame, textvariable=self.output_dir_var, width=50).pack(side=tk.LEFT, padx=5)
        tk.Button(output_frame, text="Browse", command=self.choose_output_dir, bg = "lightgreen", fg="black").pack(side=tk.LEFT)

        # Nhập thời lượng muốn chia
        tk.Label(self, text="Nhập Thời Lượng (giây)").pack(pady=10)
        self.duration_entry = tk.Entry(self)
        self.duration_entry.pack()

        # Chọn số lượng video cần chia
        tk.Label(self, text="Chọn Số Lượng Video").pack(pady=10)
        self.num_videos_var = tk.IntVar(value=1)
        self.num_videos_menu = tk.OptionMenu(self, self.num_videos_var, *range(1, 11))
        self.num_videos_menu.pack()

        # Button để bắt đầu tiến hành chia video
        tk.Button(self, text="Bắt Đầu Tiến Hành", command=self.split_video, bg = "yellow", fg="black").pack(pady=20)

    def choose_video(self):
        filetypes = [("Video files", "*.mp4;*.avi;*.mov;*.mkv;*.wmv")]
        video_path = filedialog.askopenfilename(filetypes=filetypes)
        if video_path:
            self.video_path_var.set(video_path)

    def choose_output_dir(self):
        output_dir = filedialog.askdirectory()
        if output_dir:
            self.output_dir_var.set(output_dir)

    def split_video(self):
        video_path = self.video_path_var.get()
        output_dir = self.output_dir_var.get()

        if not video_path or not output_dir:
            messagebox.showerror("Lỗi", "Vui lòng chọn video và thư mục xuất file")
            return

        try:
            duration = int(self.duration_entry.get())
            num_videos = self.num_videos_var.get()
        except ValueError:
            messagebox.showerror("Lỗi", "Vui lòng nhập thời lượng hợp lệ")
            return

        video = mp.VideoFileClip(video_path)
        video_duration = video.duration

        # Lấy tên file gốc và phần mở rộng
        base_name, ext = os.path.splitext(os.path.basename(video_path))

        for i in range(num_videos):
            start_time = i * duration
            end_time = start_time + duration
            if start_time < video_duration:
                clip = video.subclip(start_time, min(end_time, video_duration))
                output_path = os.path.join(output_dir, f"{base_name}_{i + 1}.mp4")
                clip.write_videofile(output_path, codec="libx264")
            else:
                break

        messagebox.showinfo("Thành công", "Video đã được chia thành công")

if __name__ == "__main__":
    app = VideoSplitterApp()
    app.mainloop()
