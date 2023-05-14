import os
import subprocess
import tkinter.filedialog
import tkinter.messagebox
import customtkinter

class CompressApp(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        screen_x = int(self.winfo_screenwidth())
        screen_y = int(self.winfo_screenheight())
        window_x = 500
        window_y = 500
        position_x = (screen_x // 2) - (window_x // 2)
        position_y = (screen_y // 2) - (window_y // 2)
        geo = "{}x{}+{}+{}".format(window_x, window_y, position_x, position_y)
        self.geometry(geo)
        self.title("Compresseur de vidéo")
        self.input_file = None
        self.output_folder = None
        self.output_file_name = tkinter.StringVar()
        self.output_file_name.set("compressed_video")
        self.output_file_name.trace("w", self.update_l)
        self.create_widgets()

    def update_l(self, *args) -> str:
        return self.output_file_name.get()

    def create_widgets(self):
        self.select_frame = customtkinter.CTkFrame(self,  corner_radius=0)
        self.select_frame.pack(padx=20,pady=20)
        self.output_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.output_frame.pack(padx=20, pady=20)
        self.btn_frame = customtkinter.CTkFrame(self,  corner_radius=0)
        self.btn_frame.pack(padx=20, pady=20)


        self.output_folder_label = customtkinter.CTkLabel(self.select_frame,
                                             text="Choise Folder")
        self.select_output_button = customtkinter.CTkButton(self.select_frame, text="Select", command=self.select_output_folder)
        self.input_file_label = customtkinter.CTkLabel(self.select_frame, text="Choice Video File")
        self.select_input_button = customtkinter.CTkButton(self.select_frame, text="Select", command=self.select_input_file)

        self.output_file_name_label = customtkinter.CTkLabel(self.output_frame,
                                                          text="OutPoutFIle Name:")

        self.entry_name =  customtkinter.CTkEntry(self.output_frame,
                                    textvariable=self.output_file_name)  # la taille du champ se modifie par:



        self.compress_button = customtkinter.CTkButton(self.btn_frame, text="Compresser", command=self.compress_video,
                                          )#state="disabled"
        self.cancel_button = customtkinter.CTkButton(self.btn_frame, text="Annuler", command=self.cancel_compression)
        self.progress_bar = customtkinter.CTkProgressBar(self, indeterminate_speed=1)

        self.output_folder_label.pack()

        self.select_output_button.pack()
        self.input_file_label.pack()
        self.select_input_button.pack()
        self.output_file_name_label.grid(row=1, column=0, padx=20, )
        self.entry_name.grid(row=1, column=1, padx=20, pady=(20, 10))
        self.compress_button.pack(pady=(20, 10))
        self.cancel_button.pack(pady=(20, 10))
        self.progress_bar.pack()

    def select_input_file(self) -> str:
        self.input_file = tkinter.filedialog.askopenfilename(filetypes=[("Video files", "*.mp4;*.avi;*.mkv")])
        self.input_file_label.configure(text=self.input_file)
        return self.input_file

    def select_output_folder(self) -> str:
        self.output_folder = tkinter.filedialog.askdirectory()
        self.output_folder_label.configure(text= self.output_folder)
        return self.output_folder



    def compress_video(self):
        # Validate inputs
        if not self.input_file:
            tkinter.messagebox.showerror("Erreur", "Aucun fichier vidéo sélectionné")
            return
        if not self.output_folder:
            tkinter.messagebox.showerror("Erreur", "Aucun dossier de sortie sélectionné")
            return

        if len(self.update_l()) > 0:
            self.output_file = self.output_folder + "/" + self.update_l() + ".mp4"
        else:
            self.output_file = self.output_folder + "/" + "compressed_video" + ".mp4"

        # Construct the command
        command = f'ffmpeg -i "{self.input_file}" -vcodec h264 -acodec aac -crf 20 -b:v 1000k -b:a 128k -r 25 -s 720x480 "{self.output_file}"'

        # Start compression
        self.progress_bar.start()
        self.progress_bar.set(50)
        subprocess.run(command, shell=True)

        # Extract a thumbnail from the compressed video
        thumbnail_file = os.path.splitext(self.output_file)[0] + '.jpg'
        thumbnail_command = f'ffmpeg -i "{self.output_file}" -ss 3 -filter:v "scale=720:-1" -vframes 1 "{thumbnail_file}"'
        subprocess.run(thumbnail_command, shell=True)

        self.progress_bar.stop()
        tkinter.messagebox.showinfo("Succès", "Compression terminée avec succès")


    def cancel_compression(self):
        self.progress_bar.stop()
        self.destroy()


def main():

    app = CompressApp()
    app.mainloop()


if __name__ == "__main__":
    main()