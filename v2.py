import tkinter as tk
import tkinter.filedialog
import tkinter.messagebox
from tkinter import ttk
import ffmpeg
#ffmpeg.set_ffmpeg_exe("/bin/ffmpeg.exe")
def select_input_file():
    input_file = tkinter.filedialog.askopenfilename(filetypes=[("Video files", "*.mp4;*.avi;*.mkv")])
    input_file_label.config(text=input_file)
    return input_file

def select_output_folder():
    output_folder = tkinter.filedialog.askdirectory()
    output_folder_label.config(text=output_folder)
    return output_folder

def compress_video():
    input_file = select_input_file()
    output_folder = select_output_folder()
    output_file = output_folder + "/compressed_video.mp4"
    
    # Validate inputs
    if not input_file:
        tkinter.messagebox.showerror("Erreur", "Aucun fichier vidéo sélectionné")
        return
    if not output_folder:
        tkinter.messagebox.showerror("Erreur", "Aucun dossier de sortie sélectionné")
        return

    # Start compression
    progress_bar.start(50)
    (
        ffmpeg
        .input(input_file)
        .output(output_file, vcodec='h264', acodec='aac', crf=20, b='1000k', ab='128k', r=25, s='720x480')
        .overwrite_output()
        .run()
    )
    progress_bar.stop()
    tkinter.messagebox.showinfo("Succès", "Compression terminée avec succès")

def cancel_compression():
    progress_bar.stop()
    root.destroy()

root = tk.Tk()
root.geometry("500x500")
root.title("Compresseur de vidéo")





output_folder_label = tk.Label(root, text="Choisissez un dossier pour enregistrer le fichier compressé")
output_folder_label.pack()

select_output_button = tk.Button(root, text="Sélectionner", command=select_output_folder)
select_output_button.pack()
input_file_label = tk.Label(root, text="Sélectionnez un fichier vidéo")
input_file_label.pack()
compress_button = tk.Button(root, text="Compresser", command=compress_video)
compress_button.pack()

cancel_button = tk.Button(root, text="Annuler", command=cancel_compression)
cancel_button.pack()

progress_bar = ttk.Progressbar(root, mode="indeterminate")
progress_bar.pack()
root.mainloop()