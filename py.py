import tkinter as tk
import tkinter.filedialog as filedialog
import ffmpeg
#ffmpeg.set_ffmpeg_exe("/bin/ffmpeg.exe")
def compress_video():
    input_path = filedialog.askopenfilename(filetypes=[("Video Files", "*.avi;*.mp4;*.mkv")])
    output_path = filedialog.asksaveasfilename(defaultextension=".mp4", filetypes=[("MP4 Files", "*.mp4")])

    input_stream = ffmpeg.input(input_path)
    output_stream = input_stream.output(
        output_path,
        vcodec='h264',
        acodec='aac',
        crf=20,
        b='1000k',
        ab='128k',
        r=25,
        s='720x480',
    )

    ffmpeg.run(output_stream)

root = tk.Tk()
root.title("Video Compression App")

compress_button = tk.Button(root, text="Compress Video", command=compress_video)
compress_button.pack()

root.mainloop()
