import tkinter as tk
from tkinter import filedialog, messagebox
import moviepy.editor as mp
import os

def select_files():
    files = filedialog.askopenfilenames(filetypes=[("Video files", "*.mp4;*.avi;*.mov;*.mkv;*.wmv")])
    file_list.delete(0, tk.END)
    for file in files:
        file_list.insert(tk.END, file)

def select_output_folder():
    folder = filedialog.askdirectory()
    if folder:
        output_folder_entry.delete(0, tk.END)
        output_folder_entry.insert(0, folder)

def select_cover_image():
    file = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.jpeg;*.png")])
    if file:
        cover_image_entry.delete(0, tk.END)
        cover_image_entry.insert(0, file)

def create_cover():
    files = file_list.get(0, tk.END)
    output_folder = output_folder_entry.get()
    cover_image_path = cover_image_entry.get()

    if not files:
        messagebox.showerror("Error", "Please select video files.")
        return

    if not output_folder:
        messagebox.showerror("Error", "Please select an output folder.")
        return

    if not cover_image_path:
        messagebox.showerror("Error", "Please select a cover image.")
        return

    for file in files:
        video = mp.VideoFileClip(file)
        cover_image = mp.ImageClip(cover_image_path).set_duration(video.duration)
        final_video = mp.CompositeVideoClip([cover_image.set_position(("center", "center")), video.set_position(("center", "center")).set_start(0)])

        output_path = os.path.join(output_folder, os.path.basename(file).rsplit('.', 1)[0] + "_with_cover.mp4")
        final_video.write_videofile(output_path, codec='libx264', audio_codec='aac')

    messagebox.showinfo("Success", "Videos have been processed and saved with covers.")

# Create the main window
root = tk.Tk()
root.title("TẠO BÌA CHO VIDEO")

# Set window size
window_width = 400
window_height = 500
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = (screen_width // 2) - (window_width // 2)
y = (screen_height // 2) - (window_height // 2)
root.geometry(f"{window_width}x{window_height}+{x}+{y}")

# File selection
tk.Label(root, text="Chọn file cần thêm (Có thể chọn nhiều file 1 lúc):").pack()
file_list = tk.Listbox(root, selectmode=tk.MULTIPLE, width=50)
file_list.pack(pady=5)
tk.Button(root, text="Browse", command=select_files,bg = "lightgreen", fg="black").pack(pady=5)

# Output folder selection
tk.Label(root, text="Chọn thư mục xuất file:").pack()
output_folder_entry = tk.Entry(root, width=50)
output_folder_entry.pack(pady=5)
tk.Button(root, text="Browse", command=select_output_folder, bg = "lightgreen", fg="black").pack(pady=5)

# Cover image selection
tk.Label(root, text="Chọn ảnh để làm bìa cho video:").pack()
cover_image_entry = tk.Entry(root, width=50)
cover_image_entry.pack(pady=5)
tk.Button(root, text="Browse", command=select_cover_image, bg = "lightgreen", fg="black").pack(pady=5)

# Start processing button
tk.Button(root, text="Bắt đầu tiến hành", command=create_cover, bg = "yellow", fg="black").pack(pady=20)

# Run the application
root.mainloop()
