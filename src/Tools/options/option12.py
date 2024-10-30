import tkinter as tk
from tkinter import messagebox, filedialog, Toplevel, scrolledtext
from gtts import gTTS
import os
import pygame

def chon_thu_muc():
    thu_muc = filedialog.askdirectory()
    if thu_muc:
        folder_entry.delete(0, tk.END)
        folder_entry.insert(0, thu_muc)

def chuyen_doi_va_hien_thi():
    van_ban = text_entry.get("1.0", tk.END).strip()
    thu_muc = folder_entry.get().strip()
    ten_file = file_name_entry.get().strip() + '.mp3'
    
    if not van_ban:
        messagebox.showerror("Lỗi", "Vui lòng nhập vào một đoạn văn bản.")
        return
    
    if not thu_muc:
        messagebox.showerror("Lỗi", "Vui lòng nhập đường dẫn thư mục đầu ra.")
        return
    
    if not ten_file:
        messagebox.showerror("Lỗi", "Vui lòng nhập tên cho file âm thanh.")
        return
    
    try:
        tts = gTTS(van_ban, lang='vi')  # Removed speed parameter
        file_path = os.path.join(thu_muc, ten_file)
        tts.save(file_path)
        messagebox.showinfo("Thành công", "Chuyển đổi văn bản thành giọng nói thành công!")
        hien_thi_cua_so_am_thanh(file_path)
    except Exception as e:
        messagebox.showerror("Lỗi", f"Có lỗi xảy ra: {str(e)}")

def hien_thi_cua_so_am_thanh(file_path):
    top = Toplevel()
    top.title("Nghe âm thanh")
    
    play_button = tk.Button(top, text="Play", command=lambda: phat_am_thanh(file_path), bg = "lightgreen", fg="black")
    play_button.pack(pady=10)

def phat_am_thanh(file_path):
    pygame.mixer.init()
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()

def thoat_ung_dung():
    pygame.mixer.quit()
    root.destroy()

root = tk.Tk()
root.title("Chuyển đổi Văn bản thành Giọng nói")

frame_text = tk.Frame(root)
frame_text.pack(pady=10)

text_label = tk.Label(frame_text, text="Nhập văn bản:")
text_label.pack(anchor=tk.W)

text_scrollbar = tk.Scrollbar(frame_text)
text_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

text_entry = scrolledtext.ScrolledText(frame_text, height=10, width=50, wrap=tk.WORD, yscrollcommand=text_scrollbar.set)
text_entry.pack()

text_scrollbar.config(command=text_entry.yview)

frame_folder = tk.Frame(root)
frame_folder.pack(pady=10)

folder_label = tk.Label(frame_folder, text="Đường dẫn thư mục đầu ra:")
folder_label.pack(side=tk.LEFT)
folder_entry = tk.Entry(frame_folder, width=50)
folder_entry.pack(side=tk.LEFT, padx=(10, 0))

choose_button = tk.Button(frame_folder, text="Chọn", command=chon_thu_muc, bg = "lightgreen", fg="black")
choose_button.pack(side=tk.LEFT)

frame_file_name = tk.Frame(root)
frame_file_name.pack(pady=10)

file_name_label = tk.Label(frame_file_name, text="Tên file âm thanh:")
file_name_label.pack(side=tk.LEFT)
file_name_entry = tk.Entry(frame_file_name, width=30)
file_name_entry.pack(side=tk.LEFT, padx=(10, 0))

frame_buttons = tk.Frame(root)
frame_buttons.pack(pady=10)

convert_button = tk.Button(frame_buttons, text="Chuyển đổi và Hiển thị", command=chuyen_doi_va_hien_thi, bg = "yellow", fg="black")
convert_button.pack(side=tk.LEFT)

exit_button = tk.Button(frame_buttons, text="Thoát", command=thoat_ung_dung,bg = "grey", fg="black")
exit_button.pack(side=tk.LEFT)

root.mainloop()
