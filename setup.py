import tkinter as tk
from tkinter import ttk
import ffmpeg
import tkinter.filedialog
import tkinter.messagebox

class CompressApp():
    def __init__(self,master:tk):
        self.master = master
       
        self.input_file = None
        self.output_folder = None
        self.output_file_name = tkinter.StringVar()
        self.output_file_name.set("compressed_video")
        self.output_file_name.trace("w",self.update_l)
        self.create_widgets()
        
    def update_l(self,*args)-> str:
        return self.output_file_name.get()
        
    def create_widgets(self):
        self.output_folder_label = ttk.Label(self.master, text="Choisissez un dossier pour enregistrer le fichier compressé")
        self.select_output_button = ttk.Button(self.master, text="Sélectionner", command=self.select_output_folder)
        self.input_file_label = ttk.Label(self.master, text="Sélectionnez un fichier vidéo")
        self.select_input_button = ttk.Button(self.master, text="Sélectionner", command=self.select_input_file)

        self.entry_name = ttk.Entry(self.master,textvariable = self.output_file_name) #la taille du champ se modifie par:

        self.compress_button = ttk.Button(self.master, text="Compresser", command=self.compress_video,default=['disabled'])
        self.cancel_button = ttk.Button(self.master, text="Annuler", command=self.cancel_compression)
        self.progress_bar = ttk.Progressbar(self.master, mode="indeterminate")
        self.progress_bar = ttk.Progressbar(self.master, mode="indeterminate")

        
        self.output_folder_label.pack()
        
        self.select_output_button.pack()
        self.input_file_label.pack()
        self.select_input_button.pack()
        self.entry_name.pack()
        self.compress_button.pack()
        self.cancel_button.pack()
        self.progress_bar.pack()
        
    def select_input_file(self) -> str:
        self.input_file = tkinter.filedialog.askopenfilename(filetypes=[("Video files", "*.mp4;*.avi;*.mkv")])
        self.input_file_label.config(text=self.input_file)
        return self.input_file

    def select_output_folder(self) -> str:
        self.output_folder = tkinter.filedialog.askdirectory()
        self.output_folder_label.config(text=self.output_folder)
        return self.output_folder

    def compress_video(self):
       
        
        # Validate inputs
        if not self.input_file:
            tkinter.messagebox.showerror("Erreur", "Aucun fichier vidéo sélectionné")
            return
        if not self.output_folder:
            tkinter.messagebox.showerror("Erreur", "Aucun dossier de sortie sélectionné")
            return

        if len(self.update_l()) >0:
            self.output_file = self.output_folder +"/"+ self.update_l()+".mp4"
        else:
            self.output_file = self.output_folder +"/"+ "compressed_video"+".mp4"
        # Start compression
        self.progress_bar.start(50)
        (
            ffmpeg
            .input(self.input_file)
            .output(self.output_file, vcodec='h264', acodec='aac', crf=20, b='1000k', ab='128k', r=25, s='720x480')
            .overwrite_output()
            .run(),
             ffmpeg
            .input(self.input_file, ss=3)
            .filter('scale', 720, -1)
            .output( self.output_file+".jpg", vframes=1)
            .run()
        )
        self.progress_bar.stop()
        tkinter.messagebox.showinfo("Succès", "Compression terminée avec succès")

    def cancel_compression(self):
        self.progress_bar.stop()
        self.master.destroy()
        
        
def main():
    root = tk.Tk()
    screen_x = int(root.winfo_screenwidth())
    screen_y = int(root.winfo_screenheight())
    window_x = 500
    window_y = 500
    position_x = (screen_x // 2) - (window_x // 2)
    position_y = (screen_y // 2) - (window_y // 2)
    geo = "{}x{}+{}+{}".format(window_x, window_y, position_x, position_y)
    root.geometry(geo)
    root.title("Compresseur de vidéo")
    style = ttk.Style()
    style.theme_names()
    #style.theme_use("aqua")
    app = CompressApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()