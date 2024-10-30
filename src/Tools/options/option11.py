import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from rembg import remove
from moviepy.editor import VideoFileClip
import cv2
import numpy as np

class BackgroundRemoverApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("TÁCH NỀN CHO VIDEO HOẶC HÌNH ẢNH")
        self.geometry("500x300")  # Tăng kích thước cửa sổ để phù hợp với nội dung

        # Biến lưu trữ đường dẫn file nguồn và thư mục xuất file
        self.source_path = tk.StringVar()
        self.output_dir = tk.StringVar()

        # Widget cho đường dẫn file nguồn
        ttk.Label(self, text="Chọn file ảnh hoặc video:").pack(pady=5)
        ttk.Entry(self, textvariable=self.source_path, width=50).pack(pady=5)
        ttk.Button(self, text="Chọn file", command=self.browse_source,bg = "lightgreen", fg="black").pack(pady=5)

        # Widget cho đường dẫn thư mục xuất file
        ttk.Label(self, text="Thư mục xuất file:").pack(pady=5)
        ttk.Entry(self, textvariable=self.output_dir, width=50).pack(pady=5)
        ttk.Button(self, text="Chọn thư mục", command=self.browse_output, bg = "lightgreen", fg="black").pack(pady=5)

        # Nút bắt đầu tiến hành
        ttk.Button(self, text="Bắt đầu tiến hành", command=self.start_processing, bg = "yellow", fg="black").pack(pady=20)

    def browse_source(self):
        filetypes = [("Image and Video files", "*.png;*.jpg;*.jpeg;*.mp4;*.avi;*.mov;*.mkv;*.wmv")]
        filepath = filedialog.askopenfilename(title="Chọn file ảnh hoặc video", filetypes=filetypes)
        self.source_path.set(filepath)

    def browse_output(self):
        dirpath = filedialog.askdirectory(title="Chọn thư mục xuất file")
        self.output_dir.set(dirpath)

    def start_processing(self):
        source_path = self.source_path.get()
        output_dir = self.output_dir.get()

        if not os.path.exists(source_path):
            messagebox.showerror("Lỗi", "File nguồn không tồn tại!")
            return
        if not os.path.exists(output_dir):
            messagebox.showerror("Lỗi", "Thư mục xuất không tồn tại!")
            return

        ext = os.path.splitext(source_path)[1].lower()
        print(f"Processing file: {source_path}")
        if ext in [".png", ".jpg", ".jpeg"]:
            print("Processing as image.")
            self.process_image(source_path, output_dir)
        elif ext in [".mp4", ".avi", ".mov", ".mkv", ".wmv"]:
            print("Processing as video.")
            self.process_video(source_path, output_dir)
        else:
            messagebox.showerror("Lỗi", "Định dạng file không hợp lệ!")

    def process_image(self, image_path, output_dir):
        try:
            print(f"Processing image: {image_path}")
            with open(image_path, 'rb') as img_file:
                img = remove(img_file.read())
            output_path = os.path.join(output_dir, "output_image.png")
            with open(output_path, 'wb') as out_file:
                out_file.write(img)
            messagebox.showinfo("Thành công", f"Đã xuất ảnh thành công: {output_path}")
            print(f"Image saved to: {output_path}")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Có lỗi xảy ra trong quá trình xử lý ảnh:\n{str(e)}")
            print(f"Error processing image: {e}")

    def process_video(self, video_path, output_dir):
        try:
            print(f"Processing video: {video_path}")
            output_path = os.path.join(output_dir, "output_video.mp4")
            clip = VideoFileClip(video_path)
            new_clips = []

            for frame in clip.iter_frames():
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frame_rgba = remove(frame_rgb)
                frame_bgr = cv2.cvtColor(frame_rgba, cv2.COLOR_RGBA2BGR)
                new_clips.append(frame_bgr)

            height, width, _ = new_clips[0].shape
            out = cv2.VideoWriter(output_path, cv2.VideoWriter_fourcc(*'mp4v'), clip.fps, (width, height))

            for frame in new_clips:
                out.write(frame)
            out.release()
            clip.close()

            if os.path.exists(output_path):
                messagebox.showinfo("Thành công", f"Đã xuất video thành công: {output_path}")
                print(f"Video saved to: {output_path}")
            else:
                messagebox.showerror("Lỗi", "Không thể ghi video đầu ra!")
                print("Error: Output video file not found.")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Có lỗi xảy ra trong quá trình xử lý video:\n{str(e)}")
            print(f"Error processing video: {e}")

if __name__ == "__main__":
    app = BackgroundRemoverApp()
    app.mainloop()
