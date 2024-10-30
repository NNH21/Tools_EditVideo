import tkinter as tk
from tkinter import filedialog, messagebox
import os
from moviepy.editor import VideoFileClip, ImageClip, CompositeVideoClip

class Option8App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Gắn Logo Vào Video")
        self.geometry("400x450")

        self.file_to_edit = ""
        self.output_folder = ""
        self.logo_image_path = ""
        self.logo_position = ""
        self.output_filename = ""

        self.create_widgets()

    def create_widgets(self):
        # Label và Entry cho chọn file cần gắn logo
        tk.Label(self, text="Chọn file video cần gắn logo:").pack(pady=10)
        self.file_entry = tk.Entry(self, width=40)
        self.file_entry.pack()
        tk.Button(self, text="Browser", command=self.browse_file, bg = "lightgreen", fg="black").pack()

        # Label và Entry cho chọn file logo
        tk.Label(self, text="Chọn file logo:").pack(pady=10)
        self.logo_entry = tk.Entry(self, width=40)
        self.logo_entry.pack()
        tk.Button(self, text="Browser", command=self.browse_logo, bg = "lightgreen", fg="black").pack()

        # Label và Entry cho chọn thư mục xuất file
        tk.Label(self, text="Chọn thư mục xuất file:").pack(pady=10)
        self.folder_entry = tk.Entry(self, width=40)
        self.folder_entry.pack()
        tk.Button(self, text="Browser", command=self.browse_folder, bg = "lightgreen", fg="black").pack()

        # Label và OptionMenu để chọn vị trí gắn logo
        tk.Label(self, text="Chọn vị trí gắn logo:").pack(pady=10)
        positions = [
            "Trên cùng bên phải",
            "Trên cùng bên trái",
            "Dưới cùng bên phải",
            "Dưới cùng bên trái"
        ]
        self.position_var = tk.StringVar(self)
        self.position_var.set(positions[0])  # Mặc định chọn vị trí đầu tiên
        option_menu = tk.OptionMenu(self, self.position_var, *positions)
        option_menu.pack()

        # Label và Entry cho nhập tên file xuất sau khi gắn logo
        tk.Label(self, text="Nhập tên file xuất (không có đuôi):").pack(pady=10)
        self.filename_entry = tk.Entry(self, width=40)
        self.filename_entry.pack()

        # Button để bắt đầu tiến hành gắn logo
        tk.Button(self, text="Bắt đầu tiến hành", command=self.start_editing, bg = "yellow", fg="black").pack(pady=20)

    def browse_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Video files", "*.mp4;*.avi;*.mov;*.mkv;*.wmv")])
        if file_path:
            self.file_entry.delete(0, tk.END)
            self.file_entry.insert(0, file_path)

    def browse_logo(self):
        logo_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.bmp")])
        if logo_path:
            self.logo_entry.delete(0, tk.END)
            self.logo_entry.insert(0, logo_path)

    def browse_folder(self):
        folder_path = filedialog.askdirectory()
        if folder_path:
            self.folder_entry.delete(0, tk.END)
            self.folder_entry.insert(0, folder_path)

    def start_editing(self):
        self.file_to_edit = self.file_entry.get().strip()
        self.output_folder = self.folder_entry.get().strip()
        self.logo_image_path = self.logo_entry.get().strip()
        self.logo_position = self.position_var.get()
        self.output_filename = self.filename_entry.get().strip()

        if not self.file_to_edit:
            tk.messagebox.showerror("Lỗi", "Vui lòng chọn file video cần gắn logo.")
            return
        if not os.path.isfile(self.file_to_edit):
            tk.messagebox.showerror("Lỗi", "File video không tồn tại.")
            return
        if not self.output_folder:
            tk.messagebox.showerror("Lỗi", "Vui lòng chọn thư mục xuất file.")
            return
        if not os.path.isdir(self.output_folder):
            tk.messagebox.showerror("Lỗi", "Thư mục xuất file không tồn tại.")
            return
        if not self.logo_image_path:
            tk.messagebox.showerror("Lỗi", "Vui lòng chọn file logo.")
            return
        if not os.path.isfile(self.logo_image_path):
            tk.messagebox.showerror("Lỗi", "File logo không tồn tại.")
            return
        if not self.output_filename:
            tk.messagebox.showerror("Lỗi", "Vui lòng nhập tên file xuất.")
            return

        try:
            # Load video clip
            video_clip = VideoFileClip(self.file_to_edit)

            # Load logo image and create ImageClip
            logo_clip = ImageClip(self.logo_image_path)
            logo_clip = logo_clip.resize(height=50)  # Resize logo clip if needed

            # Calculate logo position on the video
            logo_x, logo_y = self.calculate_logo_position(video_clip, logo_clip)

            # Create CompositeVideoClip with logo
            final_clip = CompositeVideoClip([video_clip,
                                             logo_clip.set_position((logo_x, logo_y)).set_duration(video_clip.duration)])

            # Write video to output file
            output_file = os.path.join(self.output_folder, f"{self.output_filename}.mp4")
            final_clip.write_videofile(output_file, codec="libx264", audio_codec="aac")

            tk.messagebox.showinfo("Thông báo", f"Đã gắn logo vào video thành công. Đã lưu tại: {output_file}")
        except Exception as e:
            tk.messagebox.showerror("Lỗi", f"Lỗi trong quá trình gắn logo vào video: {str(e)}")

    def calculate_logo_position(self, video_clip, logo_clip):
        # Calculate logo position based on user-selected position
        logo_width, logo_height = logo_clip.size

        if self.logo_position == "Trên cùng bên phải":
            logo_x = video_clip.size[0] - logo_width
            logo_y = 0
        elif self.logo_position == "Trên cùng bên trái":
            logo_x = 0
            logo_y = 0
        elif self.logo_position == "Dưới cùng bên phải":
            logo_x = video_clip.size[0] - logo_width
            logo_y = video_clip.size[1] - logo_height
        elif self.logo_position == "Dưới cùng bên trái":
            logo_x = 0
            logo_y = video_clip.size[1] - logo_height

        return logo_x, logo_y

if __name__ == "__main__":
    app = Option8App()
    app.mainloop()
