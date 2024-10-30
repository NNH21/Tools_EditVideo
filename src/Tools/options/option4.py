import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os
from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.video.fx.speedx import speedx

class VideoSpeedApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("TỐC ĐỘ THAY ĐỔI NHANH CHẬM")
        self.geometry("400x350")

        self.create_widgets()

    def create_widgets(self):
        # Label và Entry cho thư mục chọn file cần chỉnh sửa
        self.label_choose_input = tk.Label(self, text="Chọn file video cần chỉnh sửa tốc độ:")
        self.label_choose_input.pack(pady=10)

        self.entry_input_path = tk.Entry(self, width=40, state='disabled')
        self.entry_input_path.pack()

        self.btn_browse_input = tk.Button(self, text="Chọn file", command=self.browse_input_file, bg = "lightgreen", fg="black")
        self.btn_browse_input.pack(pady=5)

        # Label và Entry cho thư mục chọn nơi xuất file
        self.label_choose_output = tk.Label(self, text="Chọn thư mục xuất file sau khi chỉnh sửa:")
        self.label_choose_output.pack(pady=10)

        self.entry_output_path = tk.Entry(self, width=40, state='disabled')
        self.entry_output_path.pack()

        self.btn_browse_output = tk.Button(self, text="Chọn thư mục", command=self.browse_output_folder, bg = "lightgreen", fg="black")
        self.btn_browse_output.pack(pady=5)

        # Thanh trượt cho lựa chọn tốc độ từ 0.1x đến 5x
        self.label_speed = tk.Label(self, text="Chọn tốc độ (0.1x - 5x):")
        self.label_speed.pack(pady=5)

        self.scale_speed = tk.Scale(self, from_=0.1, to=5.0, resolution=0.1, orient=tk.HORIZONTAL, length=300)
        self.scale_speed.set(1.0)  # Tốc độ mặc định là 1.0x
        self.scale_speed.pack()

        # Button để bắt đầu chỉnh sửa tốc độ video
        self.btn_start_process = tk.Button(self, text="Bắt đầu tiến hành", command=self.start_processing, bg = "yellow", fg="black")
        self.btn_start_process.pack(pady=10)

    def browse_input_file(self):
        file_path = filedialog.askopenfilename(filetypes=[
            ("Video files", "*.mp4;*.avi;*.mov;*.mkv;*.wmv"),
            ("All files", "*.*")
        ])
        if file_path:
            self.entry_input_path.config(state='normal')
            self.entry_input_path.delete(0, tk.END)
            self.entry_input_path.insert(0, file_path)
            self.entry_input_path.config(state='disabled')

    def browse_output_folder(self):
        folder_path = filedialog.askdirectory()
        if folder_path:
            self.entry_output_path.config(state='normal')
            self.entry_output_path.delete(0, tk.END)
            self.entry_output_path.insert(0, folder_path)
            self.entry_output_path.config(state='disabled')

    def start_processing(self):
        input_path = self.entry_input_path.get()
        output_folder = self.entry_output_path.get()
        speed_factor = float(self.scale_speed.get())

        if not input_path or not output_folder:
            messagebox.showerror("Error", "Vui lòng chọn đầy đủ file video và thư mục xuất file.")
            return
        
        try:
            video_clip = VideoFileClip(input_path)
            edited_video = speedx(video_clip, speed_factor)

            video_name = os.path.splitext(os.path.basename(input_path))[0]
            output_path = os.path.join(output_folder, f"{video_name}_speed.mp4")

            edited_video.write_videofile(output_path, codec='libx264')

            messagebox.showinfo("Thông báo", f"Đã chỉnh sửa tốc độ video thành công và lưu tại {output_path}.")
        except Exception as e:
            messagebox.showerror("Error", f"Lỗi khi chỉnh sửa tốc độ video: {str(e)}")

if __name__ == "__main__":
    app = VideoSpeedApp()
    app.mainloop()
