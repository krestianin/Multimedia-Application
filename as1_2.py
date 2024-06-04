import tkinter as tk
from tkinter import filedialog, Menu, messagebox
from PIL import Image, ImageTk
import wave
import numpy as np
import matplotlib.pyplot as plt

def open_tiff():
    filepath = filedialog.askopenfilename(
        title="Open TIFF File", 
        filetypes=[("TIFF files", "*.tif *.tiff")],
        initialdir="/"
    )
    if not filepath:
        return

    try:
        img = Image.open(filepath)
        img_tk = ImageTk.PhotoImage(img)

        canvas.config(width=img.width, height=img.height)
        canvas.delete("all")
        canvas.create_image(img.width // 2, img.height // 2, image=img_tk)
        canvas.image = img_tk
        root.geometry(f"{img.width}x{img.height}")  

    except Exception as e:
        messagebox.showerror("Error", f"Failed to open image file: {e}")

def open_wav():
    filepath = filedialog.askopenfilename(
        title="Open WAV File", 
        filetypes=[("WAV files", "*.wav")],
        initialdir="/"
    )
    if not filepath:
        return

    try:
        with wave.open(filepath, 'rb') as wf:
            n_channels = wf.getnchannels()
            sampwidth = wf.getsampwidth()
            framerate = wf.getframerate()
            n_frames = wf.getnframes()
            frames = wf.readframes(n_frames)
        
        samples = np.frombuffer(frames, dtype=np.int16)
        samples = np.reshape(samples, (-1, n_channels))
        messagebox.showinfo("WAV File Info", f"Sample Width: {sampwidth} bytes\nSampling frequency: {framerate} Hz\nNumber of samples: {n_frames}")
        plot_wav(samples, framerate)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to open WAV file: {e}")

    default_width, default_height = 800, 600
    canvas.config(width=default_width, height=default_height)
    canvas.delete("all")
    root.geometry(f"{default_width}x{default_height}")  

def plot_wav(samples, framerate):

    canvas.delete("all")

    plt.figure(figsize=(10, 6))
    time = np.arange(samples.shape[0]) / framerate

    plt.subplot(2, 1, 1)
    plt.plot(time, samples[:, 0], color='blue')
    plt.title('Left Channel')
    plt.xlabel('Time, sec')
    plt.ylabel('Amplitude')

    plt.subplot(2, 1, 2)
    plt.plot(time, samples[:, 1], color='red')
    plt.title('Right Channel')
    plt.xlabel('Time, sec')
    plt.ylabel('Amplitude')
   
    plt.tight_layout()
    plt.show()

def exit_program():
    root.destroy()

root = tk.Tk()
root.title("Media Viewer")

menu = Menu(root)
root.config(menu=menu)

file_menu = Menu(menu, tearoff=0)
menu.add_cascade(label="Open file", menu=file_menu)
file_menu.add_command(label="Open TIFF Image", command=open_tiff)
file_menu.add_command(label="Open WAV File", command=open_wav)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=exit_program)

canvas = tk.Canvas(root, bg='white', width=800, height=600)
canvas.create_text(400, 300, text="Welcome to the media viewer", fill="black", font=('Helvetica 45 bold'))
canvas.pack(fill=tk.BOTH, expand=True)

root.mainloop()
