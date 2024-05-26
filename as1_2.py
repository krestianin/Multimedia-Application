import tkinter as tk
from tkinter import ttk, filedialog, Menu, messagebox
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
        canvas.delete("all")  # Clear the canvas
        canvas.config(width=img.width, height=img.height)
        canvas.create_image(0, 0, anchor="nw", image=img_tk)
        canvas.image = img_tk  # Keep a reference!
    except Exception as e:
        messagebox.showerror("Error", f"Failed to open image file: {e}")

def open_wav():
    filepath = filedialog.askopenfilename(
        title="Open WAV File", 
        filetypes=[("WAV files", "*.wav")],
        initialdir="/"
    )
    canvas.delete("all")  
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
        messagebox.showinfo("WAV File Info", f"Channels: {n_channels}\nSample Width: {sampwidth} bytes\nFrame Rate: {framerate} Hz\nFrames: {n_frames}")
        time = np.arange(samples.shape[0]) / framerate
        plt.figure(figsize=(10, 6))

        # Plot left channel
        plt.subplot(2, 1, 1)
        plt.plot(time, samples[:, 0], color='blue')
        plt.title('Left Channel')
        plt.xlabel('Time [s]')
        plt.ylabel('Amplitude')

        # Plot right channel
        plt.subplot(2, 1, 2)
        plt.plot(time, samples[:, 1], color='red')
        plt.title('Right Channel')
        plt.xlabel('Time [s]')
        plt.ylabel('Amplitude')

        plt.tight_layout()
        plt.show()
    except Exception as e:
        messagebox.showerror("Error", f"Failed to open WAV file: {e}")

def exit_program():
    root.destroy()

# def show_popup(event):
#     popup_menu.tk_popup(event.x_root, event.y_root)

root = tk.Tk()
root.title("Media Viewer and Player")

root.state('zoomed') 

# style = ttk.Style()
# style.theme_use('clam')  # Set a theme

# Create a menu
menu = Menu(root)
root.config(menu=menu)
root.geometry("1000x800")


file_menu = Menu(menu, tearoff=0)
menu.add_cascade(label="Open file", menu=file_menu)
file_menu.add_command(label="Open TIFF Image", command=open_tiff)
file_menu.add_command(label="Open WAV File", command=open_wav)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=exit_program)


# Create a canvas to display images
canvas = tk.Canvas(root, bg='white')
canvas.pack(fill=tk.BOTH, expand=True)

width = root.winfo_width()
height = root.winfo_height()
canvas.create_text(width / 3, height / 2, text="Welcom to the media viewer!", fill="black", anchor='center', font=('Helvetica', 50, 'bold'))


root.mainloop()


# root = tk.Tk()
# root.title("Media Viewer")
# root.geometry("600x400")

# # Create a canvas to display images
# canvas = tk.Canvas(root, bg='white')
# canvas.pack(fill=tk.BOTH, expand=True)

# # Create a button that will open the pop-up menu
# button = tk.Button(root, text="Open File", command=lambda: button.place_forget())
# button.pack(side=tk.TOP, pady=50)

# # Create an Exit button
# exit_button = tk.Button(root, text="Exit", command=exit_program)
# exit_button.pack(side=tk.BOTTOM, pady=10)

# # Create a pop-up menu
# popup_menu = tk.Menu(root, tearoff=0)
# popup_menu.add_command(label="Open TIFF Image", command=open_tiff)
# popup_menu.add_command(label="Open WAV File", command=open_wav)

# # Bind the button to show the popup on click
# button.bind("<Button-1>", show_popup)

# root.mainloop()