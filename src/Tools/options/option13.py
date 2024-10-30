import tkinter as tk
from tkinter import filedialog, messagebox
import moviepy.editor as mp
import os
from moviepy.video.fx.all import colorx, lum_contrast

class AdjustVideoPropertiesApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Tăng - Giảm Độ Sáng, Bão Hòa, Tương Phản")
        self.geometry("400x500")

        self.video_files = []
        self.output_path = ""
        self.brightness = 0
        self.saturation = 0
        self.contrast = 0

        self.create_widgets()

    def create_widgets(self):
        tk.Label(self, text="1. Chọn các video cần điều chỉnh:", pady=10).pack()
        self.video_files_entry = tk.Entry(self, width=50)
        self.video_files_entry.pack()
        tk.Button(self, text="Chọn Video", command=self.choose_videos, bg = "lightgreen", fg="black").pack()

        tk.Label(self, text="2. Chọn thư mục lưu video sau khi điều chỉnh:", pady=10).pack()
        self.output_entry = tk.Entry(self, width=50)
        self.output_entry.pack()
        tk.Button(self, text="Chọn Thư Mục", command=self.choose_output_directory, bg = "lightgreen", fg="black").pack()

        tk.Label(self, text="3. Điều chỉnh độ sáng:", pady=10).pack()
        self.brightness_slider = tk.Scale(self, from_=-50, to=50, orient=tk.HORIZONTAL)
        self.brightness_slider.pack()

        tk.Label(self, text="4. Điều chỉnh độ bão hòa:", pady=10).pack()
        self.saturation_slider = tk.Scale(self, from_=-50, to=50, orient=tk.HORIZONTAL)
        self.saturation_slider.pack()

        tk.Label(self, text="5. Điều chỉnh độ tương phản:", pady=10).pack()
        self.contrast_slider = tk.Scale(self, from_=-50, to=50, orient=tk.HORIZONTAL)
        self.contrast_slider.pack()

        tk.Button(self, text="Bắt đầu tiến hành", command=self.adjust_video_properties, bg = "yellow", fg="black").pack(pady=20)

    def choose_videos(self):
        self.video_files = filedialog.askopenfilenames(title="Chọn các video", filetypes=[("Video files", "*.mp4;*.avi;*.mov;*.mkv;*.wmv")])
        self.video_files_entry.delete(0, tk.END)
        self.video_files_entry.insert(tk.END, "; ".join(self.video_files))

    def choose_output_directory(self):
        self.output_path = filedialog.askdirectory(title="Chọn thư mục lưu video")
        self.output_entry.delete(0, tk.END)
        self.output_entry.insert(tk.END, self.output_path)

    def adjust_video_properties(self):
        if not self.video_files or not self.output_path:
            messagebox.showerror("Lỗi", "Vui lòng chọn video và thư mục lưu")
            return

        self.brightness = self.brightness_slider.get()
        self.saturation = self.saturation_slider.get()
        self.contrast = self.contrast_slider.get()

        for video_file in self.video_files:
            try:
                video = mp.VideoFileClip(video_file)

                # Adjust brightness
                if self.brightness != 0:
                    video = video.fx(mp.vfx.colorx, 1 + (self.brightness / 100))

                # Adjust saturation
                if self.saturation != 0:
                    video = video.fx(mp.vfx.lum_contrast, 0, 1, 1 + (self.saturation / 100))

                # Adjust contrast
                if self.contrast != 0:
                    video = video.fx(mp.vfx.lum_contrast, self.contrast, 0.5, 1)

                output_file = os.path.join(self.output_path, os.path.splitext(os.path.basename(video_file))[0] + "_adjusted.mp4")
                video.write_videofile(output_file, codec='libx264', fps=video.fps)
                video.close()

            except Exception as e:
                messagebox.showerror("Lỗi", f"Có lỗi xảy ra với video {video_file}: {str(e)}")

        messagebox.showinfo("Thông báo", "Điều chỉnh video hoàn tất!")

if __name__ == "__main__":
    app = AdjustVideoPropertiesApp()
    app.mainloop()
