import tkinter as tk
from tkinter import messagebox
import subprocess
import os
import sys

class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Tools Edit By HoangMis")
        self.geometry("400x600")
        self.attributes("-topmost", True)  # Đặt cửa sổ luôn luôn ở trên cùng

        self.process = None

        # Đường dẫn tuyệt đối tới thư mục chứa file main.py
        self.base_dir = os.path.dirname(os.path.abspath(__file__))

        # Tạo một Canvas để đặt hình nền
        self.canvas = tk.Canvas(self, width=400, height=600)
        self.canvas.pack()

        # Thêm hình nền
        image_path = os.path.join(self.base_dir, "assets/bg.png")
        if os.path.exists(image_path):
            self.background_image = tk.PhotoImage(file=image_path)  # Đường dẫn tới file ảnh nền
            self.canvas.create_image(0, 0, anchor="nw", image=self.background_image)
        else:
            print("Error: Background image not found at", image_path)

        self.create_start_menu()

    def create_start_menu(self):
        self.canvas.delete("all")

        if hasattr(self, 'background_image'):
            self.canvas.create_image(0, 0, anchor="nw", image=self.background_image)

        # Thay đổi màu sắc của các nút
        start_button = tk.Button(self, text="START", width=20, command=self.create_main_menu, bg="lightgreen", fg="black")
        setting_button = tk.Button(self, text="SETTING", width=20, bg="lightblue", fg="black", command=self.show_settings)
        exit_button = tk.Button(self, text="EXIT", width=20, bg="lightcoral", fg="black", command=self.exit_app)

        self.canvas.create_window(200, 250, window=start_button)
        self.canvas.create_window(200, 300, window=setting_button)
        self.canvas.create_window(200, 350, window=exit_button)

    def create_main_menu(self):
        self.canvas.delete("all")

        if hasattr(self, 'background_image'):
            self.canvas.create_image(0, 0, anchor="nw", image=self.background_image)

        menu_options = [
            "1. CHIA VIDEO THỜI GIAN BẰNG NHAU",
            "2. CẮT VIDEO TÙY CHỌN THỜI LƯỢNG",
            "3. THÊM VĂN BẢN VÀO VIDEO",
            "4. TỐC ĐỘ THAY ĐỔI NHANH CHẬM",
            "5. CHUYỂN TỈ LỆ VIDEO",
            "6. GHÉP 2 VIDEO VỚI NHAU",
            "7. XÓA NHẠC - GHÉP NHẠC MỚI",
            "8. GẮN LOGO RIÊNG VÀO VIDEO",
            "9. THÊM INTRO - OUTRO HÀNG LOẠT",
            "10. CHUYỂN VIDEO THÀNH ÂM THANH",
            "11. TÁCH NỀN CHO VIDEO HOẶC HÌNH ẢNH",
            "12. CHUYỂN ĐỔI VĂN BẢN THÀNH GIỌNG NÓI (AI)",
            "13. TĂNG - GIẢM ĐỘ SÁNG, BÃO HÒA, TƯƠNG PHẢN",
            "14. TẠO BÌA CHO VIDEO",
            "15. PHỦ VIDEO CHO VIDEO (Video phủ - Video ghép)"
        ]

        menu_frame = tk.Frame(self.canvas)
        self.canvas.create_window(200, 300, window=menu_frame)

        for i, option in enumerate(menu_options, start=1):
            button = tk.Button(menu_frame, text=option, width=40, command=lambda opt=i: self.run_option(opt), bg = "violet", fg="black")
            button.pack(pady=3)

        back_button = tk.Button(self, text="Back", width=20, command=self.create_start_menu, bg = "grey", fg="black")
        self.canvas.create_window(200, 550, window=back_button)

    def show_settings(self):
        messagebox.showinfo("Settings", "Chức năng cài đặt đang được phát triển.")

    def exit_app(self):
        self.quit()

    def run_option(self, option_number):
        if self.process is not None:
            # Terminate the current running process
            self.process.terminate()
            self.process = None

        option_script = f"options/option{option_number}.py"
        script_path = os.path.join(self.base_dir, option_script)
        if os.path.exists(script_path):
            self.process = subprocess.Popen([sys.executable, script_path], cwd=os.path.dirname(script_path))
        else:
            messagebox.showerror("Error", f"Script {option_script} not found.")

    def clear_canvas(self):
        self.canvas.delete("all")

if __name__ == "__main__":
    app = MainApp()
    app.mainloop()
