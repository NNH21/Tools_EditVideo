import tkinter as tk
from tkinter import filedialog, messagebox, colorchooser
import os
import moviepy.editor as mp

class TextOverlayApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Thêm Văn Bản Vào Video")
        self.geometry("400x500")

        self.video_path_var = tk.StringVar()
        self.output_dir_var = tk.StringVar()
        self.text_var = tk.StringVar()
        self.font_size_var = tk.IntVar(value=24)
        self.color_var = tk.StringVar(value="#FFFFFF")
        self.position_var = tk.StringVar(value="center")

        tk.Label(self, text="Chọn Video:").pack(pady=5)
        video_frame = tk.Frame(self)
        video_frame.pack(pady=5)
        tk.Entry(video_frame, textvariable=self.video_path_var, width=50).pack(side=tk.LEFT, padx=5)
        tk.Button(video_frame, text="Browse", command=self.choose_video, bg = "lightgreen", fg="black").pack(side=tk.LEFT)

        tk.Label(self, text="Chọn Thư Mục Xuất File:").pack(pady=5)
        output_frame = tk.Frame(self)
        output_frame.pack(pady=5)
        tk.Entry(output_frame, textvariable=self.output_dir_var, width=50).pack(side=tk.LEFT, padx=5)
        tk.Button(output_frame, text="Browse", command=self.choose_output_dir, bg = "lightgreen", fg="black").pack(side=tk.LEFT)

        tk.Label(self, text="Nhập Văn Bản:").pack(pady=10)
        self.text_entry = tk.Entry(self, textvariable=self.text_var, width=50)
        self.text_entry.pack()

        tk.Label(self, text="Nhập Cỡ Chữ:").pack(pady=10)
        self.font_size_entry = tk.Entry(self, textvariable=self.font_size_var)
        self.font_size_entry.pack()

        tk.Label(self, text="Chọn Màu Sắc:").pack(pady=10)
        color_frame = tk.Frame(self)
        color_frame.pack(pady=5)
        tk.Entry(color_frame, textvariable=self.color_var, width=20).pack(side=tk.LEFT, padx=5)
        tk.Button(color_frame, text="Chọn Màu", command=self.choose_color, bg = "lightgreen", fg="black").pack(side=tk.LEFT)

        tk.Label(self, text="Chọn Vị Trí:").pack(pady=10)
        positions = ["Trên cùng bên trái", "Trên cùng bên phải", "Trên cùng ở giữa", 
                     "Giữa video", "Giữa video bên phải", "Giữa video bên trái", 
                     "Góc dưới cùng bên trái", "Góc dưới cùng bên phải", "Góc dưới cùng ở giữa"]
        self.position_menu = tk.OptionMenu(self, self.position_var, *positions)
        self.position_menu.pack()

        tk.Button(self, text="Bắt Đầu Tiến Hành", command=self.add_text_to_video, bg = "yellow", fg="black").pack(pady=20)

    def choose_video(self):
        filetypes = [("Video files", "*.mp4;*.avi;*.mov;*.mkv;*.wmv")]
        video_path = filedialog.askopenfilename(filetypes=filetypes)
        if video_path:
            self.video_path_var.set(video_path)

    def choose_output_dir(self):
        output_dir = filedialog.askdirectory()
        if output_dir:
            self.output_dir_var.set(output_dir)

    def choose_color(self):
        color_code = colorchooser.askcolor(title="Chọn Màu Sắc")
        if color_code:
            self.color_var.set(color_code[1])

    def add_text_to_video(self):
        video_path = self.video_path_var.get()
        output_dir = self.output_dir_var.get()
        text = self.text_var.get()
        font_size = self.font_size_var.get()
        color = self.color_var.get()
        position = self.position_var.get()

        if not video_path or not output_dir or not text:
            messagebox.showerror("Lỗi", "Vui lòng nhập đầy đủ thông tin")
            return

        try:
            video = mp.VideoFileClip(video_path)
            
            # Tạo clip văn bản
            txt_clip = mp.TextClip(text, fontsize=font_size, color=color)
            txt_clip = txt_clip.set_duration(video.duration)
            
            # Đặt vị trí văn bản
            positions_dict = {
                "Trên cùng bên trái": "top left",
                "Trên cùng bên phải": "top right",
                "Trên cùng ở giữa": "top",
                "Giữa video": "center",
                "Giữa video bên phải": "right",
                "Giữa video bên trái": "left",
                "Góc dưới cùng bên trái": "bottom left",
                "Góc dưới cùng bên phải": "bottom right",
                "Góc dưới cùng ở giữa": "bottom"
            }
            txt_clip = txt_clip.set_position(positions_dict[position])
            
            # Tạo video mới với văn bản
            video = mp.CompositeVideoClip([video, txt_clip])
            
            # Tạo tên file đầu ra
            base_name, ext = os.path.splitext(os.path.basename(video_path))
            output_path = os.path.join(output_dir, f"{base_name}_with_text.mp4")
            
            # Ghi video đầu ra
            video.write_videofile(output_path, codec='libx264', temp_audiofile='temp-audio.m4a', remove_temp=True, fps=24)
            
            messagebox.showinfo("Thành công", "Video đã được thêm văn bản thành công")
        
        except Exception as e:
            messagebox.showerror("Lỗi", f"Có lỗi xảy ra: {str(e)}")

if __name__ == "__main__":
    app = TextOverlayApp()
    app.mainloop()
