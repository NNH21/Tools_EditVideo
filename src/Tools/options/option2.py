import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os
from moviepy.video.io.VideoFileClip import VideoFileClip

class VideoCutterApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("CẮT VIDEO TÙY CHỌN THỜI LƯỢNG")
        self.geometry("350x350")

        self.create_widgets()

    def create_widgets(self):
        # Label và Entry cho thư mục chọn file cần cắt
        self.label_choose_input = tk.Label(self, text="Chọn file video cần cắt:")
        self.label_choose_input.pack(pady=10)

        self.entry_input_path = tk.Entry(self, width=40, state='disabled')
        self.entry_input_path.pack()

        self.btn_browse_input = tk.Button(self, text="Chọn file", command=self.browse_input_file,bg = "lightgreen", fg="black")
        self.btn_browse_input.pack(pady=5)

        # Label và Entry cho thư mục chọn nơi xuất file
        self.label_choose_output = tk.Label(self, text="Chọn thư mục xuất file sau khi cắt:")
        self.label_choose_output.pack(pady=10)

        self.entry_output_path = tk.Entry(self, width=40, state='disabled')
        self.entry_output_path.pack()

        self.btn_browse_output = tk.Button(self, text="Chọn thư mục", command=self.browse_output_folder, bg = "lightgreen", fg="black")
        self.btn_browse_output.pack(pady=5)

        # Combobox cho lựa chọn số giây cắt đầu và cuối video
        self.label_cut_start = tk.Label(self, text="Cắt bao nhiêu giây đầu video:")
        self.label_cut_start.pack(pady=5)

        self.combo_cut_start = ttk.Combobox(self, width=37)
        self.combo_cut_start['values'] = ("0", "1", "2", "3", "4", "5")
        self.combo_cut_start.pack()

        self.label_cut_end = tk.Label(self, text="Cắt bao nhiêu giây cuối video:")
        self.label_cut_end.pack(pady=5)

        self.combo_cut_end = ttk.Combobox(self, width=37)
        self.combo_cut_end['values'] = ("0", "1", "2", "3", "4", "5")
        self.combo_cut_end.pack()

        # Button để bắt đầu cắt video
        self.btn_start_cut = tk.Button(self, text="Bắt đầu tiến hành", command=self.start_cutting, bg = "yellow", fg="black")
        self.btn_start_cut.pack(pady=10)

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

    def start_cutting(self):
        input_path = self.entry_input_path.get()
        output_folder = self.entry_output_path.get()
        cut_start = int(self.combo_cut_start.get())
        cut_end = int(self.combo_cut_end.get())

        if not input_path or not output_folder:
            messagebox.showerror("Error", "Vui lòng chọn đầy đủ file video và thư mục xuất file.")
            return
        
        try:
            video_clip = VideoFileClip(input_path)
            duration = video_clip.duration

            if cut_start > duration or cut_end > duration:
                messagebox.showerror("Error", "Thời lượng cắt không hợp lệ. Vui lòng kiểm tra lại.")
                return

            cut_video = video_clip.subclip(cut_start, duration - cut_end)
            video_name = os.path.splitext(os.path.basename(input_path))[0]
            output_path = os.path.join(output_folder, f"{video_name}_cut.mp4")

            cut_video.write_videofile(output_path, codec='libx264')

            messagebox.showinfo("Thông báo", f"Đã cắt video thành công và lưu tại {output_path}.")
        except Exception as e:
            messagebox.showerror("Error", f"Lỗi khi cắt video: {str(e)}")

if __name__ == "__main__":
    app = VideoCutterApp()
    app.mainloop()
