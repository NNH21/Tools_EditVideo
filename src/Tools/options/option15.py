# Provide comments for this code 
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os
import moviepy.editor as mp

class VideoOverlayApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Overlay Video")
        self.geometry("430x500")

        self.main_video_path_var = tk.StringVar()
        self.overlay_video_path_var = tk.StringVar()
        self.output_path_var = tk.StringVar()

        self.opacity_var = tk.DoubleVar(value=0.5)
        self.position_x_var = tk.DoubleVar(value=0.0)
        self.position_y_var = tk.DoubleVar(value=0.0)
        self.scale_var = tk.DoubleVar(value=1.0)

        tk.Label(self, text="Video Chính:").pack(pady=5)
        main_video_frame = tk.Frame(self)
        main_video_frame.pack(pady=5)
        tk.Entry(main_video_frame, textvariable=self.main_video_path_var, width=50).pack(side=tk.LEFT, padx=5)
        tk.Button(main_video_frame, text="Chọn", command=self.choose_main_video,bg = "lightgreen", fg="black").pack(side=tk.LEFT)

        tk.Label(self, text="Video Phủ:").pack(pady=5)
        overlay_video_frame = tk.Frame(self)
        overlay_video_frame.pack(pady=5)
        tk.Entry(overlay_video_frame, textvariable=self.overlay_video_path_var, width=50).pack(side=tk.LEFT, padx=5)
        tk.Button(overlay_video_frame, text="Chọn", command=self.choose_overlay_video, bg = "lightgreen", fg="black").pack(side=tk.LEFT)

        tk.Label(self, text="Độ trong suốt của video phủ:").pack(pady=5)
        opacity_slider = ttk.Scale(self, from_=0.0, to=1.0, length=200, variable=self.opacity_var, orient=tk.HORIZONTAL)
        opacity_slider.pack()

        tk.Label(self, text="Vị trí của video phủ (X, Y):").pack(pady=5)
        position_frame = tk.Frame(self)
        position_frame.pack(pady=5)
        tk.Scale(position_frame, label="X", from_=0.0, to=1.0, resolution=0.01, variable=self.position_x_var, orient=tk.HORIZONTAL).pack(side=tk.LEFT, padx=5)
        tk.Scale(position_frame, label="Y", from_=0.0, to=1.0, resolution=0.01, variable=self.position_y_var, orient=tk.HORIZONTAL).pack(side=tk.LEFT)

        tk.Label(self, text="Tỉ lệ kích thước video phủ:").pack(pady=5)
        scale_slider = ttk.Scale(self, from_=0.1, to=2.0, length=200, variable=self.scale_var, orient=tk.HORIZONTAL)
        scale_slider.pack()

        tk.Label(self, text="Thư Mục Xuất File:").pack(pady=5)
        output_frame = tk.Frame(self)
        output_frame.pack(pady=5)
        tk.Entry(output_frame, textvariable=self.output_path_var, width=50).pack(side=tk.LEFT, padx=5)
        tk.Button(output_frame, text="Chọn", command=self.choose_output_dir,bg = "lightgreen", fg="black").pack(side=tk.LEFT)

        tk.Button(self, text="Phủ Video", command=self.overlay_videos, bg = "yellow", fg="black").pack(pady=20)

    def choose_main_video(self):
        filetypes = [("Video files", "*.mp4;*.avi;*.mov;*.mkv;*.wmv")]
        main_video_path = filedialog.askopenfilename(filetypes=filetypes)
        if main_video_path:
            self.main_video_path_var.set(main_video_path)

    def choose_overlay_video(self):
        filetypes = [("Video files", "*.mp4;*.avi;*.mov;*.mkv;*.wmv")]
        overlay_video_path = filedialog.askopenfilename(filetypes=filetypes)
        if overlay_video_path:
            self.overlay_video_path_var.set(overlay_video_path)

    def choose_output_dir(self):
        output_dir = filedialog.askdirectory()
        if output_dir:
            self.output_path_var.set(output_dir)

    def overlay_videos(self):
        main_video_path = self.main_video_path_var.get()
        overlay_video_path = self.overlay_video_path_var.get()
        output_dir = self.output_path_var.get()

        opacity = self.opacity_var.get()
        position_x = self.position_x_var.get()
        position_y = self.position_y_var.get()
        scale = self.scale_var.get()

        if not main_video_path or not overlay_video_path or not output_dir:
            messagebox.showerror("Lỗi", "Vui lòng chọn cả video chính và video phủ, và chỉ định thư mục xuất file.")
            return

        try:
            main_video = mp.VideoFileClip(main_video_path)
            overlay_video = mp.VideoFileClip(overlay_video_path)

            # Cắt video chính nếu nó dài hơn video phủ
            if main_video.duration > overlay_video.duration:
                main_video = main_video.subclip(0, overlay_video.duration)
            # Cắt video phủ nếu nó dài hơn video chính
            elif overlay_video.duration > main_video.duration:
                overlay_video = overlay_video.subclip(0, main_video.duration)

            # Điều chỉnh kích thước của video phủ
            overlay_video = overlay_video.resize((int(overlay_video.w * scale), int(overlay_video.h * scale)))

            # Điều chỉnh vị trí của video phủ trên video chính
            overlay_video = overlay_video.set_position((position_x, position_y))

            # Điều chỉnh độ trong suốt của video phủ
            overlay_video = overlay_video.set_opacity(opacity)

            # Ghép hai video lại với nhau
            final_clip = main_video.set_duration(main_video.duration)
            final_clip = mp.CompositeVideoClip([final_clip, overlay_video])

            # Đặt tên file đầu ra
            ten_video_chinh = os.path.splitext(os.path.basename(main_video_path))[0]
            ten_file_output = f"{ten_video_chinh}_voi_video_phu.mp4"
            output_path = os.path.join(output_dir, ten_file_output)

            # Xuất video kết hợp
            final_clip.write_videofile(output_path, codec="libx264")

            messagebox.showinfo("Thành công", "Video đã được phủ thành công!")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Có lỗi xảy ra: {str(e)}")

if __name__ == "__main__":
    app = VideoOverlayApp()
    app.mainloop()
