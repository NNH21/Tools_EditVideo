import tkinter as tk
from tkinter import filedialog, messagebox
import moviepy.editor as mp
import os

class MergeVideosApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Ghép 2 Video")
        self.geometry("400x550")

        self.video1_path = ""
        self.video2_path = ""
        self.output_path = ""
        self.merge_type = "top-bottom"
        self.keep_audio = "video1"
        self.output_filename = "output_video.mp4"

        self.create_widgets()

    def create_widgets(self):
        tk.Label(self, text="1. Chọn video thứ 1 cần ghép:", pady=10).pack()
        self.video1_entry = tk.Entry(self, width=50)
        self.video1_entry.pack()
        tk.Button(self, text="Chọn Video", command=self.choose_video1, bg = "lightgreen", fg="black").pack()

        tk.Label(self, text="2. Chọn video thứ 2 cần ghép:", pady=10).pack()
        self.video2_entry = tk.Entry(self, width=50)
        self.video2_entry.pack()
        tk.Button(self, text="Chọn Video", command=self.choose_video2, bg = "lightgreen", fg="black").pack()

        tk.Label(self, text="3. Chọn thư mục lưu video sau khi ghép:", pady=10).pack()
        self.output_entry = tk.Entry(self, width=50)
        self.output_entry.pack()
        tk.Button(self, text="Chọn Thư Mục", command=self.choose_output_directory,bg = "lightgreen", fg="black").pack()

        tk.Label(self, text="4. Chọn kiểu ghép video:", pady=10).pack()
        self.merge_var = tk.StringVar()
        self.merge_var.set("top-bottom")
        merge_options = [("Ghép nửa trên và nửa dưới", "top-bottom"), ("Ghép nửa bên phải và nửa bên trái", "left-right")]
        for text, mode in merge_options:
            tk.Radiobutton(self, text=text, variable=self.merge_var, value=mode).pack()

        tk.Label(self, text="5. Chọn âm thanh giữ lại:", pady=10).pack()
        self.audio_var = tk.StringVar()
        self.audio_var.set("video1")
        audio_options = [("Giữ lại âm thanh video 1", "video1"), ("Giữ lại âm thanh video 2", "video2")]
        for text, mode in audio_options:
            tk.Radiobutton(self, text=text, variable=self.audio_var, value=mode).pack()

        tk.Label(self, text="6. Nhập tên file sau khi xuất:", pady=10).pack()
        self.filename_entry = tk.Entry(self, width=50)
        self.filename_entry.pack()

        tk.Button(self, text="Bắt đầu tiến hành", command=self.merge_videos, bg = "yellow", fg="black").pack(pady=20)

    def choose_video1(self):
        self.video1_path = filedialog.askopenfilename(title="Chọn video thứ 1")
        self.video1_entry.delete(0, tk.END)
        self.video1_entry.insert(tk.END, self.video1_path)

    def choose_video2(self):
        self.video2_path = filedialog.askopenfilename(title="Chọn video thứ 2")
        self.video2_entry.delete(0, tk.END)
        self.video2_entry.insert(tk.END, self.video2_path)

    def choose_output_directory(self):
        self.output_path = filedialog.askdirectory(title="Chọn thư mục lưu video")
        self.output_entry.delete(0, tk.END)
        self.output_entry.insert(tk.END, self.output_path)

    def merge_videos(self):
        if not self.video1_path or not self.video2_path or not self.output_path or not self.filename_entry.get():
            messagebox.showerror("Lỗi", "Vui lòng điền đầy đủ thông tin và chọn video")
            return

        self.output_filename = self.filename_entry.get()
        if not self.output_filename.endswith(".mp4"):
            self.output_filename += ".mp4"

        try:
            video1 = mp.VideoFileClip(self.video1_path)
            video2 = mp.VideoFileClip(self.video2_path)

            # Resize videos to have the same height and width
            video2 = video2.resize(newsize=video1.size)

            min_duration = min(video1.duration, video2.duration)
            video1 = video1.subclip(0, min_duration)
            video2 = video2.subclip(0, min_duration)

            # Remove audio if necessary
            if self.audio_var.get() == "video1":
                video2 = video2.without_audio()
            else:
                video1 = video1.without_audio()

            if self.merge_var.get() == "top-bottom":
                final_clip = mp.clips_array([[video1], [video2]])
            else:
                final_clip = mp.clips_array([[video1, video2]])

            output_file = os.path.join(self.output_path, self.output_filename)
            final_clip.write_videofile(output_file, codec='libx264', fps=video1.fps)
            video1.close()
            video2.close()
            final_clip.close()

            messagebox.showinfo("Thông báo", f"Ghép video thành công!\nVideo được lưu tại: {output_file}")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Có lỗi xảy ra: {str(e)}")

if __name__ == "__main__":
    app = MergeVideosApp()
    app.mainloop()
