import tkinter as tk
from tkinter import filedialog, messagebox
import os
from moviepy.editor import VideoFileClip
from moviepy.video.fx.resize import resize

class Option5App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Chuyển Tỉ Lệ Video")
        self.geometry("350x400")

        self.file_to_convert = ""
        self.output_folder = ""
        self.aspect_ratio = ""
        self.output_file_name = ""

        self.create_widgets()

    def create_widgets(self):
        # Label và Entry cho chọn file cần chuyển đổi
        tk.Label(self, text="Chọn file video cần chuyển đổi:").pack(pady=10)
        self.file_entry = tk.Entry(self, width=40)
        self.file_entry.pack()
        tk.Button(self, text="Browser", command=self.browse_file,bg = "lightgreen", fg="black").pack()

        # Label và Entry cho chọn thư mục xuất file
        tk.Label(self, text="Chọn thư mục xuất file:").pack(pady=10)
        self.folder_entry = tk.Entry(self, width=40)
        self.folder_entry.pack()
        tk.Button(self, text="Browser", command=self.browse_folder, bg = "lightgreen", fg="black").pack()

        # Label và OptionMenu để chọn tỉ lệ khung hình
        tk.Label(self, text="Chọn tỉ lệ khung hình:").pack(pady=10)
        aspect_ratios = [
            "9:16",
            "16:9",
            "1:1",
            "4:3",
            "2:1",
            "5.8",
            "2.35:1",
            "3:4"
        ]
        self.aspect_ratio_var = tk.StringVar(self)
        self.aspect_ratio_var.set(aspect_ratios[0])  # Mặc định chọn tỉ lệ đầu tiên
        option_menu = tk.OptionMenu(self, self.aspect_ratio_var, *aspect_ratios)
        option_menu.pack()

        # Label và Entry cho nhập tên file xuất sau khi cắt
        tk.Label(self, text="Nhập tên file xuất sau khi cắt:").pack(pady=10)
        self.output_file_entry = tk.Entry(self, width=40)
        self.output_file_entry.pack()

        # Button để bắt đầu tiến hành chuyển đổi
        tk.Button(self, text="Bắt đầu tiến hành", command=self.start_conversion,bg = "yellow", fg="black").pack(pady=20)

    def browse_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Video files", "*.mp4;*.avi;*.mov;*.mkv;*.wmv")])
        if file_path:
            self.file_entry.delete(0, tk.END)
            self.file_entry.insert(0, file_path)

    def browse_folder(self):
        folder_path = filedialog.askdirectory()
        if folder_path:
            self.folder_entry.delete(0, tk.END)
            self.folder_entry.insert(0, folder_path)

    def start_conversion(self):
        self.file_to_convert = self.file_entry.get().strip()
        self.output_folder = self.folder_entry.get().strip()
        self.output_file_name = self.output_file_entry.get().strip()

        if not self.file_to_convert:
            tk.messagebox.showerror("Lỗi", "Vui lòng chọn file video cần chuyển đổi.")
            return
        if not os.path.isfile(self.file_to_convert):
            tk.messagebox.showerror("Lỗi", "File video không tồn tại.")
            return
        if not self.output_folder:
            tk.messagebox.showerror("Lỗi", "Vui lòng chọn thư mục xuất file.")
            return
        if not os.path.isdir(self.output_folder):
            tk.messagebox.showerror("Lỗi", "Thư mục xuất file không tồn tại.")
            return
        if not self.output_file_name:
            tk.messagebox.showerror("Lỗi", "Vui lòng nhập tên file xuất sau khi cắt.")
            return

        try:
            clip = VideoFileClip(self.file_to_convert)
            width, height = clip.size

            # Chuyển đổi tỉ lệ khung hình
            new_width, new_height = self.calculate_new_size(width, height, self.aspect_ratio_var.get())
            resized_clip = resize(clip, width=new_width, height=new_height)

            # Lưu video xuống thư mục xuất file với tên file được nhập
            output_file = os.path.join(self.output_folder, f"{self.output_file_name}.mp4")
            resized_clip.write_videofile(output_file, codec="libx264", audio_codec="aac")

            tk.messagebox.showinfo("Thông báo", f"Chuyển đổi video thành công. Đã lưu tại: {output_file}")
        except Exception as e:
            tk.messagebox.showerror("Lỗi", f"Lỗi trong quá trình chuyển đổi video: {str(e)}")

    def calculate_new_size(self, width, height, aspect_ratio):
        # Hàm tính toán kích thước mới dựa trên tỉ lệ khung hình
        if aspect_ratio == "9:16":
            new_width = int(height * 9 / 16)
            new_height = height
        elif aspect_ratio == "16:9":
            new_width = width
            new_height = int(width * 9 / 16)
        elif aspect_ratio == "1:1":
            new_width = height
            new_height = height
        elif aspect_ratio == "4:3":
            new_width = int(height * 4 / 3)
            new_height = height
        elif aspect_ratio == "2:1":
            new_width = int(height * 2)
            new_height = height
        elif aspect_ratio == "5.8":
            new_width = int(height * 5.8)
            new_height = height
        elif aspect_ratio == "2.35:1":
            new_width = int(height * 2.35)
            new_height = height
        elif aspect_ratio == "3:4":
            new_width = int(height * 3 / 4)
            new_height = height
        else:
            new_width = width
            new_height = height

        return new_width, new_height

if __name__ == "__main__":
    app = Option5App()
    app.mainloop()
