import tkinter as tk
from tkinter import filedialog, messagebox
import moviepy.editor as mp
import os

class BatchAddIntroOutroApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Thêm Intro - Outro Hàng Loạt")
        self.geometry("350x400")

        self.video_files = []
        self.output_path = ""
        self.intro_path = ""
        self.outro_path = ""

        self.create_widgets()

    def create_widgets(self):
        tk.Label(self, text="1. Chọn các video cần thêm:", pady=10).pack()
        self.video_files_entry = tk.Entry(self, width=50)
        self.video_files_entry.pack()
        tk.Button(self, text="Chọn Video", command=self.choose_videos, bg = "lightgreen", fg="black").pack()

        tk.Label(self, text="2. Chọn thư mục lưu video sau khi ghép:", pady=10).pack()
        self.output_entry = tk.Entry(self, width=50)
        self.output_entry.pack()
        tk.Button(self, text="Chọn Thư Mục", command=self.choose_output_directory, bg = "lightgreen", fg="black").pack()

        tk.Label(self, text="3. Chọn video intro:", pady=10).pack()
        self.intro_entry = tk.Entry(self, width=50)
        self.intro_entry.pack()
        tk.Button(self, text="Chọn Video Intro", command=self.choose_intro, bg = "lightgreen", fg="black").pack()

        tk.Label(self, text="4. Chọn video outro:", pady=10).pack()
        self.outro_entry = tk.Entry(self, width=50)
        self.outro_entry.pack()
        tk.Button(self, text="Chọn Video Outro", command=self.choose_outro, bg = "lightgreen", fg="black").pack()

        tk.Button(self, text="Bắt đầu tiến hành", command=self.add_intro_outro, bg = "yellow", fg="black").pack(pady=20)

    def choose_videos(self):
        self.video_files = filedialog.askopenfilenames(title="Chọn các video", filetypes=[("Video files", "*.mp4;*.avi;*.mov;*.mkv;*.wmv")])
        self.video_files_entry.delete(0, tk.END)
        self.video_files_entry.insert(tk.END, "; ".join(self.video_files))

    def choose_output_directory(self):
        self.output_path = filedialog.askdirectory(title="Chọn thư mục lưu video")
        self.output_entry.delete(0, tk.END)
        self.output_entry.insert(tk.END, self.output_path)

    def choose_intro(self):
        self.intro_path = filedialog.askopenfilename(title="Chọn video intro", filetypes=[("Video files", "*.mp4;*.avi;*.mov;*.mkv;*.wmv")])
        self.intro_entry.delete(0, tk.END)
        self.intro_entry.insert(tk.END, self.intro_path)

    def choose_outro(self):
        self.outro_path = filedialog.askopenfilename(title="Chọn video outro", filetypes=[("Video files", "*.mp4;*.avi;*.mov;*.mkv;*.wmv")])
        self.outro_entry.delete(0, tk.END)
        self.outro_entry.insert(tk.END, self.outro_path)

    def add_intro_outro(self):
        if not self.video_files or not self.output_path:
            messagebox.showerror("Lỗi", "Vui lòng chọn video và thư mục lưu")
            return

        for video_file in self.video_files:
            try:
                video = mp.VideoFileClip(video_file)

                if self.intro_path:
                    intro = mp.VideoFileClip(self.intro_path)
                else:
                    intro = None

                if self.outro_path:
                    outro = mp.VideoFileClip(self.outro_path)
                else:
                    outro = None

                final_clip = video
                if intro:
                    final_clip = mp.concatenate_videoclips([intro, final_clip])
                if outro:
                    final_clip = mp.concatenate_videoclips([final_clip, outro])

                output_file = os.path.join(self.output_path, os.path.splitext(os.path.basename(video_file))[0] + "_edited.mp4")
                final_clip.write_videofile(output_file, codec='libx264', fps=video.fps)
                video.close()
                if intro:
                    intro.close()
                if outro:
                    outro.close()

            except Exception as e:
                messagebox.showerror("Lỗi", f"Có lỗi xảy ra với video {video_file}: {str(e)}")

        messagebox.showinfo("Thông báo", "Thêm intro và outro hoàn tất!")

if __name__ == "__main__":
    app = BatchAddIntroOutroApp()
    app.mainloop()
