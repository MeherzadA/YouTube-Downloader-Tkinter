from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from moviepy.editor import *
from pytube import YouTube
import pytube
import os

global lbl
global videoTitle
global options
global value
global fileLocation
global filetype
global extType
global path
global DownloadButton
global fileLocationEntry
global link
global congratsLabel
global checkboxvar
global checkbox
global clippingFrame
global startHH
global startMM
global startSS
global endHH
global endMM
global endSS
global illegal
# global lsf

main = Tk()
main.title("YT Downloader")
main.geometry("700x700")

lbl = Label(main)
test = StringVar()
videoTitle = Label(main)

fileExtensions = [
    ("mp4", ".mp4"),("mp3", ".mp3"),
    ("wav", ".wav"), ("AVI", ".avi")
]

illegal = ['#', '%', '&', '{', '}', '\\', '<', '>', '*', '?', '/', '$', '!', "'", '"', ':', '@','+', '`', '|', '=']

extensionslist = []




def find_video():
    global test
    global lbl
    global videoTitle
    global options
    global value
    global fileLocation
    global DownloadButton
    global link
    global checkboxvar
    global checkbox
    test = StringVar()
    test.set("")

    try:
        link = pytube.YouTube(linkentry.get())
        videoTitle = Label(main, text = link.title)
        videoTitle.pack()
        DownloadButton = Button(frame2, text="Download", state = DISABLED, command =lambda: downloads(test.get()))
        checkboxvar = StringVar()
        checkbox = Checkbutton(main, text="Would you like to clip a specific portion of this video?", variable = checkboxvar, onvalue = "h", offvalue= "b", command = clipster)
        checkbox.deselect()
        checkbox.pack()
        for extensions, value in fileExtensions:
            options = Radiobutton(main, text = extensions, variable = test, value = value, command =lambda: after_radio(test.get()))
            options.deselect()
            extensionslist.append(options)
            options.pack()
        DownloadButton.place(x = 397, y = 27)
        frame2.place(x = 50, y = 450)
        fileLocationEntry.pack()
        fileLocation = Button(frame2, text = "Select File Location", command = openfilez, state = DISABLED)
        fileLocation.pack(side = LEFT)
        # Okbutton = Button(main, text="Ok", command=after_radio(value))

    except pytube.exceptions.RegexMatchError:
        linkentry.delete(0, END)
        lbl = Label(main, text = "Invalid URL, Try again")
        lbl.pack()
    except pytube.exceptions.ExtractError:
        lbl = Label(main, text = "Could not extract the neccessary computer thingies for this to work!")
        lbl.pack()
    except pytube.exceptions.VideoUnavailable:
        lbl = Label(main, text = "The video is unavailable, or it may be unlisted")
        lbl.pack()
    videoSearch['state'] = DISABLED

def after_radio(x):
    global filetype
    global extType
    # Okbutton['state'] = DISABLED
    if x == ".mp3":
        fileLocation['state'] = NORMAL
        filetype = "MP3 AUDIO"
        extType = "*.mp3"
    elif x == ".mp4":
        fileLocation['state'] = NORMAL
        filetype = "MP4 VIDEO AND AUDIO"
        extType = "*.mp4"
    elif x == ".avi":
        fileLocation['state'] = NORMAL
        filetype = "AVI VIDEO AND AUDIO"
        extType = "*.avi"
    elif x == ".wav":
        fileLocation['state'] = NORMAL
        filetype = "WAV AUDIO"
        extType = "*.wav"

def openfilez():
    # global lsf
    global path
    fileLocationEntry['state'] = NORMAL
    fileLocationEntry.delete(0, END)
    fileLocationEntry['state'] = DISABLED
    main.filename = filedialog.askdirectory(initialdir="/", title="Select download folder")
    path = main.filename
    fileLocationEntry['state'] = NORMAL
    fileLocationEntry.insert(0, path)
    fileLocationEntry['state'] = DISABLED
    DownloadButton['state'] = NORMAL

def downloads(z):
    global congratsLabel
    congratsLabel.pack(side = BOTTOM)
    if z == ".mp3":
        try:
            MP3_audio = link.streams.filter(only_audio=True).first()
            MP3_audio = MP3_audio.download(output_path=fileLocationEntry.get())
            start, extension = os.path.splitext(MP3_audio)
            start += ".mp3"
            os.rename(MP3_audio, start)
            congratsLabel.config(text=link.title + "\n has been successfully downloaded in .mp3 format!")
        except FileExistsError:
            response = messagebox.showerror("Major RIP","You already have a file in this format downloaded in this location!")
        except:
            response = messagebox.showerror("Major RIP","Video was not able to be extracted/downloaded for unknown reasons!")
        if startHH.get().isdigit() and startMM.get().isdigit() and startSS.get().isdigit() and endHH.get().isdigit() and endMM.get().isdigit() and endSS.get().isdigit():
            try:
                VidPath = str((fileLocationEntry.get()) + "/")
                index = 0
                newTitle = ""
                newVidPath = ""
                Title = link.title
                for i in range(len(VidPath)):
                    checking = VidPath[index]
                    if checking != "/":
                        newVidPath += checking
                    elif checking == "/":
                        newVidPath += "\\"
                    index += 1
                for character in illegal:
                    Title = Title.replace(character, "")
                h = newVidPath + Title + ".mp3"
                file = AudioFileClip(h)
                clipped = file.subclip(t_start=(int(startHH.get()), int(startMM.get()), int(startSS.get())),t_end=(int(endHH.get()), int(endMM.get()), int(endSS.get())))
                clipped.write_audiofile(newVidPath + Title + " clipped.mp3")
                yesorno = messagebox.showwarning("Warning!","Warning: In order to clip your selected video, the program has saved 2 copies of the video:\nThe original, and the clipped version.\nThey can be diffrentiated via the filename.")
            except:
                noclip = messagebox.showerror("Error", "Video/audio was not able to be clipped!\nCheck to make sure you have set the proper timestamps!\nIf you did not get an error message about the original video, then rest assured that the original has been clipped properly")

    elif z == ".wav":
        try:
            WAV_audio = link.streams.filter(only_audio=True).first()
            WAV_audio = WAV_audio.download(output_path=fileLocationEntry.get())
            start, extension = os.path.splitext(WAV_audio)
            start += ".wav"
            os.rename(WAV_audio, start)
            congratsLabel.config(text=link.title + "\n has been successfully downloaded in .wav format!")
        except FileExistsError:
            response = messagebox.showwarning("Major RIP", "You already have a file in this format downloaded in this location!")
        except:
            response = messagebox.showerror("Major RIP", "Video was not able to be extracted/downloaded for unknown reasons!")
        if startHH.get().isdigit() and startMM.get().isdigit() and startSS.get().isdigit() and endHH.get().isdigit() and endMM.get().isdigit() and endSS.get().isdigit():
            try:
                VidPath = str((fileLocationEntry.get()) + "/")
                index = 0
                newTitle = ""
                newVidPath = ""
                Title = link.title
                for i in range(len(VidPath)):
                    checking = VidPath[index]
                    if checking != "/":
                        newVidPath += checking
                    elif checking == "/":
                        newVidPath += "\\"
                    index += 1
                for character in illegal:
                    Title = Title.replace(character, "")
                h = newVidPath + Title + ".wav"
                file = AudioFileClip(h)
                clipped = file.subclip(t_start=(int(startHH.get()), int(startMM.get()), int(startSS.get())),t_end=(int(endHH.get()), int(endMM.get()), int(endSS.get())))
                clipped.write_audiofile(newVidPath + Title + " clipped.wav")
                yesorno = messagebox.showwarning("Warning!","Warning: In order to clip your selected video, the program has saved 2 copies of the video:\nThe original, and the clipped version.\nThey can be diffrentiated via the filename.")
            except:
                noclip = messagebox.showerror("Error", "Video/audio was not able to be clipped!\nCheck to make sure you have set the proper timestamps!\nIf you did not get an error message about the original video, then rest assured that the original has been clipped properly")




    elif z == ".mp4":
        try:
            MP4_video = link.streams.get_highest_resolution()
            MP4_video = MP4_video.download(output_path=fileLocationEntry.get())
            congratsLabel.config(text=link.title + "\n has been successfully downloaded in .mp4 format!")
        except FileExistsError:
            response = messagebox.showerror("Major RIP","You already have a file in this format downloaded in this location!")
        except:
            response = messagebox.showerror("Major RIP","Video was not able to be extracted/downloaded for unknown reasons!")
        if startHH.get().isdigit() and startMM.get().isdigit() and startSS.get().isdigit() and endHH.get().isdigit() and endMM.get().isdigit() and endSS.get().isdigit():
            try:
                VidPath = str((fileLocationEntry.get()) + "/")
                index = 0
                newTitle = ""
                newVidPath = ""
                Title = link.title
                for i in range(len(VidPath)):
                    checking = VidPath[index]
                    if checking != "/":
                        newVidPath += checking
                    elif checking == "/":
                        newVidPath += "\\"
                    index += 1
                for character in illegal:
                        Title = Title.replace(character, "")
                h = newVidPath + Title + ".mp4"
                file = VideoFileClip(h)
                clipped = file.subclip(t_start=(int(startHH.get()), int(startMM.get()), int(startSS.get())), t_end = (int(endHH.get()), int(endMM.get()), int(endSS.get())))
                clipped.write_videofile(newVidPath + Title + " clipped.mp4")
                yesorno = messagebox.showwarning("Warning!","Warning: In order to clip your selected video, the program has saved 2 copies of the video:\nThe original, and the clipped version.\nThey can be diffrentiated via the filename.")
            except:
                noclip = messagebox.showerror("Error", "Video/audio was not able to be clipped!\nCheck to make sure you have set the proper timestamps!\nIf you did not get an error message about the original video, then rest assured that the original has been clipped properly")

    elif z == ".avi":
        try:
            AVI_video = link.streams.get_highest_resolution()
            AVI_video = AVI_video.download(output_path=fileLocationEntry.get())
            start, extension = os.path.splitext(AVI_video)
            start += ".avi"
            os.rename(AVI_video, start)
            congratsLabel.config(text=link.title + "\n has been successfully downloaded in .avi format!")
        except FileExistsError:
            response = messagebox.showerror("Major RIP","You already have a file in this format downloaded in this location!")
        except:
            response = messagebox.showerror("Major RIP","Video was not able to be extracted/downloaded for unknown reasons!")
        if startHH.get().isdigit() and startMM.get().isdigit() and startSS.get().isdigit() and endHH.get().isdigit() and endMM.get().isdigit() and endSS.get().isdigit():
            try:
                VidPath = str((fileLocationEntry.get()) + "/")
                index = 0
                newTitle = ""
                newVidPath = ""
                Title = link.title
                for i in range(len(VidPath)):
                    checking = VidPath[index]
                    if checking != "/":
                        newVidPath += checking
                    elif checking == "/":
                        newVidPath += "\\"
                    index += 1

                for character in illegal:
                        Title = Title.replace(character, "")
                h = newVidPath + Title + ".avi"
                file = VideoFileClip(h)
                clipped = file.subclip(t_start=(int(startHH.get()), int(startMM.get()), int(startSS.get())), t_end = (int(endHH.get()), int(endMM.get()), int(endSS.get())))
                clipped.write_videofile(newVidPath + Title + " clipped.avi")
                yesorno = messagebox.showwarning("Warning!","Warning: In order to clip your selected video, the program has saved 2 copies of the video:\nThe original, and the clipped version.\nThey can be diffrentiated via the filename.")
            except:
                noclip = messagebox.showerror("Error", "Video/audio was not able to be clipped!\nCheck to make sure you have set the proper timestamps!\nIf you did not get an error message about the original video, then rest assured that the original has been clipped properly")



def cancel():
    checkbox['state'] = NORMAL
    checkbox.deselect()
    clippingFrame.pack_forget()

def clear():
    startHH.delete(0, END), startMM.delete(0, END), startSS.delete(0, END), endHH.delete(0, END), endMM.delete(0,END), endSS.delete(0, END)
    startHH.insert(0, "0"), startMM.insert(0, "0"), startSS.insert(0, "0"), endHH.insert(0,"0"), endMM.insert(0, "0"), endSS.insert(0, "0")



def clipster():
    global clippingFrame
    global startHH
    global startMM
    global startSS
    global endHH
    global endMM
    global endSS
    checkbox['state'] = DISABLED
    clippingFrame = LabelFrame(text="Define Start and End Timestamps, Enter 0 In Place of Blank Spaces:", padx = 20, pady = 20, width = 100, height= 100)
    clippingFrame.pack(padx = 1, pady= 1, side = TOP)
    cancelButton = Button(clippingFrame, text = "Cancel", command = cancel)
    cancelButton.pack(side = RIGHT)
    clearButton = Button(clippingFrame, text = "Clear options", command = clear)
    clearButton.pack(side = BOTTOM)
    startHH = Entry(clippingFrame, width=7, borderwidth=2)
    startMM = Entry(clippingFrame, width=7, borderwidth=2)
    startSS = Entry(clippingFrame, width=7, borderwidth=2)
    endHH = Entry(clippingFrame, width=7, borderwidth=2)
    endMM = Entry(clippingFrame, width=7, borderwidth=2)
    endSS = Entry(clippingFrame, width=7, borderwidth=2)
    startHH.insert(0, "Hour"), startMM.insert(0, "Minute"), startSS.insert(0, "Second"),endHH.insert(0, "Hour"), endMM.insert(0, "Minute"), endSS.insert(0, "Second")
    toLabel = Label(clippingFrame, text="to")
    startHH.pack(side = LEFT), startMM.pack(side = LEFT), startSS.pack(side = LEFT), toLabel.pack(side=LEFT), endHH.pack(side=LEFT), endMM.pack(side=LEFT), endSS.pack(side=LEFT)


def retry():
    videoSearch['state'] = NORMAL
    lbl.destroy()
    videoTitle.destroy()
    for widget in extensionslist:
        widget.forget()
    linkentry.delete(0, END)
    frame2.place_forget()
    fileLocation.pack_forget()
    checkbox.pack_forget()
    clippingFrame.pack_forget()
    congratsLabel.pack_forget()

frame1 = LabelFrame(text = "Enter Youtube Link Here", padx = 20, pady = 20)
frame1.pack(padx = 20, pady = 20)

frame2 = LabelFrame(text = "Select Download Path", padx = 60, pady = 60)
frame1.pack(padx = 20, pady = 20)

videoSearch = Button(main, text = "Search video", command = find_video)
videoSearch.pack()


linkentry = Entry(frame1, width = 75, borderwidth = 5, fg = "Red")
linkentry.pack()

fileLocationEntry = Entry(frame2, width = 75, borderwidth = 5, state = DISABLED)

retryy = Button(main, text = "Reset All", command = retry)
retryy.pack()



congratsLabel = Label(main, text = "")


main.mainloop()
