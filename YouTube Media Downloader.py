# THE FOLLOWING CODE IMPORTS THE REQUIRED MODULES AND LIBRARIES
import os
import pytube 
from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
from tkinter import OptionMenu


# CREATING THE FIRST MAIN WINDOW AND SETTING ITS ATTRIBUTES
win = Tk()
win.config(bg='#B7DDFF')
win.title('YouTube Media Downloader')
win.geometry('840x320')

# CLASS HAVING THE MEDIA DOWNLOAD METHODS
class Download_Methods:
    def __init__(self, link : pytube.YouTube):
        self.yt_link = link
        self.file_path = ''

    # METHOD TO DOWNLOAD ONLY AUDIO FROM YOUTUBE
    def only_audio_download(self, path=os.getcwd()):
        yt_addr = self.yt_link
        video = yt_addr.streams.filter(only_audio=True).first()
        save_file = video.download(output_path=path)

        base, ext = os.path.splitext(save_file)
        prev_name = base.strip(self.yt_link.title)
        new_file = prev_name + filename +  '.mp3'

        os.rename(save_file, new_file)

        messagebox.showinfo('Download Successful', f'The song has been downloaded succesfully at {path}.', parent=settings_scr)
        settings_scr.destroy()

    def drop_menu(self, scr, var, options, y_coord):
        drop = OptionMenu(scr, var, *options)
        drop.config(font=('Arial', 12), padx=105, pady=2, border=2)
        drop.place(x=260, y=y_coord)

        drop_menu = win.nametowidget(drop.menuname)
        drop_menu.config(font=('Arial', 12))

    # METHOD TO SET THE DOWNLOAD SETTINGS AS PER USER PREFERENCES
    def download_settings(self):
        global save_to_btn, res, audio_var, video_var, settings_scr, f_name_entry

        settings_scr = Toplevel(win, bg='#B0AAFF')
        settings_scr.title('Set Download Settings')
        settings_scr.geometry('575x320')

        Label(settings_scr, text='Set Video Resolution:', font=('Arial', 16), bg='#B0AAFF').place(x=30, y=30)
        Label(settings_scr, text='Download only audio:', font=('Arial', 16), bg='#B0AAFF').place(x=30, y=70)
        Label(settings_scr, text='File Name:', font=('Arial', 16), bg='#B0AAFF').place(x=30, y=115)
        Label(settings_scr, text='Save to:', font=('Arial', 16), bg='#B0AAFF').place(x=30, y=155)

        res = StringVar()
        resolutions = ['144p', '240p', '360p', '480p', '720p'] 
        res.set(resolutions[1])
        start.drop_menu(settings_scr, res, resolutions, 30)

        audio_var = StringVar()
        video_var = StringVar()

        audio_video_options = ['True', 'False']
        audio_var.set('False')
        video_var.set('False')

        start.drop_menu(settings_scr, audio_var, audio_video_options, y_coord=70)

        f_name_entry = Entry(settings_scr, width=30, border=3, font=('Arial 12'))
        f_name_entry.place(x=260, y=112)

        f_name_entry.insert(0, self.yt_link.title)

        save_to_btn = Button(settings_scr, text='Select Folder...', font=('Arial', 10, 'bold'), padx=90, pady=3, borderwidth=1, command=lambda: start.file_location(settings_scr))
        save_to_btn.place(x=260, y=155)
        Button(settings_scr, text='Start Download', font=('Arial', 12), padx=200, pady=3, border=2, command=start.set_settings).place(x=30, y=220)
        Button(settings_scr, text='Cancel', font=('Arial', 12), padx=229, pady=3, borderwidth=2, command=settings_scr.destroy).place(x=30, y=260)

    # METHOD TO SAVE THE USER PREFERRED SETTINGS AND START THE DOWNLOAD ACCORDINGLY
    def set_settings(self):
        global video_quality, video, audio, filename

        hyperlink = self.yt_link

        video_quality = res.get()
        video = True if video_var.get() == 'True' else False
        audio = False if audio_var.get() == 'False' else True
        filename = f_name_entry.get()

        try:
            try:
                # THE FOLLOWING CODE DOWNLOADS ONLY AUDIO
                if audio == True and video == False:
                    start.only_audio_download(self.file_path)
                
                # THE FOLLOWING CODE DOWNLOADS ONLY VIDEO
                elif audio == False and video == False: 
                    hyperlink.streams.filter(resolution=video_quality, only_audio=audio, only_video=video).first().download(self.file_path, filename=filename + '.mp4')
                    messagebox.showinfo('Download Successful', f'The video has been saved at {self.file_path}.',parent=settings_scr)
                    settings_scr.destroy()

                # THE FOLLOWING CODE DOWNLOADS MEDIA TO THE CURRENT DIRECTORY 
                elif len(self.file_path) == 0:
                    permit_save = messagebox.askyesnocancel('Warning', 'You have not selected any folder. The video will be saved in the current directory. Do you want to continue?')
                    if permit_save == True:
                        if audio == True and video == False:
                            start.only_audio_download(hyperlink)
                            
                        elif audio == False and video == False:
                            hyperlink.streams.filter(res=video_quality, only_audio=audio, only_video=video).first().download(os.getcwd(), filename=filename + '.mp4')
                            messagebox.showinfo('Download Successful', f'The video has been saved at {os.getcwd()} .',parent=settings_scr)
                            settings_scr.destroy()

                        else:
                            messagebox.showerror('Error', 'Please select the appropriate download settings to download the audio/video file.',parent=settings_scr)
                else:
                    messagebox.showerror('Error', 'Please select the appropriate download settings to download the audio/video files.',parent=settings_scr)
            except FileExistsError:
                if len(self.file_path) == 0:
                    self.file_path = os.getcwd()
                messagebox.showerror('Error', f"{hyperlink.title} already exists at {self.file_path}", parent=settings_scr)

        except:            
            messagebox.showwarning('Error', 'Please choose appropriate download settings.\nCommon errors might occur due to inappropriate file names invalid folder path, etc.', parent=settings_scr)

    # METHOD TO ACCESS FILE EXPLORER AND SET SAVE TO LOCATION
    def file_location(self, scr):
        self.file_path = filedialog.askdirectory(initialdir=os.path.expanduser('~'), title='Select a Folder', parent=scr)

        folder = self.file_path.split('/')
        save_to_btn.config(text=f"Saving To: {folder[-1]}", fg='#FF0000', padx=40)
        if len(self.file_path) == 0:
            save_to_btn.config(text='Select Folder...', fg='#000000', padx=65)

# METHOD TO CONVERT THE GIVEN WEB ADDRESS FROM STRING TO A YOUTUBE HYPERLINK
def create_yt_link(addr):
    global start
    if len(addr) == 0:
            messagebox.showwarning('Error', 'Please enter the address of the youtube video you want to download.')
    else:
        try:
            yt_addr = pytube.YouTube(addr)
            start = Download_Methods(link=yt_addr)
            start.download_settings()
        except:
            messagebox.showerror('Error', 'Please enter a valid address.')

def clear_entry():
    entry_wid.delete(0, END)

# CODE TO DESIGN THE FRONT-END OF THE MAIN SCREEEN
Label(win,text='Enter the link of the Youtube video you want to download:',bg='#B7DDFF' ,font=('Arial', 16, 'bold')).place(x=120, y=30)
entry_wid = Entry(win,width=60, borderwidth=2, font=('Arial 14'))
entry_wid.place(x=70, y=70)
entry_wid.focus()

# BUTTON THAT CLEARS THE ENTRY WIDGET
Button(win, text='Clear', font=('Arial', 10), padx=20,pady=5, border=1, command=clear_entry).place(x=740, y=70)

# BUTTON THAT BEGINS THE ENTIRE PROCESS OF DOWNLOADING THE MEDIA FROM THE WEB
Button(win, text='Download', font=('Arial', 16), padx=160, pady=6, border=2, command=lambda: create_yt_link(addr=entry_wid.get())).place(x=200, y=140)
Button(win, text='Close', font=('Arial', 16), padx=260, pady=8, borderwidth=2, command=win.destroy).place(x=110, y=215)


win.mainloop()