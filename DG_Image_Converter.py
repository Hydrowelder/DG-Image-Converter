import glob
from PIL import ImageTk
import PIL.Image
import tkinter.filedialog
from tkinter import *
from tkinter.messagebox import showerror
import os
import multiprocessing
# import threading

# class windowthread(threading.Thread):
#     def __init__(self):
#         threading.Thread.__init__(self)
#     def run(self):
#         pass


def GetSourceFolder():
    source = tkinter.filedialog.askdirectory()
    config["source"] = source
    source_format = source_format_var.get()
    if source == '':
        source_label.config(text="No Source Folder Selected")
    else:
        if len(source) > 71:
            source_label.config(text='...'+source[-70:])
        else:
            source_label.config(text=source)
        files = [os.path.basename(x)
                 for x in glob.glob(source+'/*'+source_format)]
        metrix["num_in"] = len(files)
        config['files'] = files
        source_count_label.config(text=str(metrix["num_in"])+" files found")


def GetDestFolder():
    dest = tkinter.filedialog.askdirectory()
    config["dest"] = dest
    if dest == '':
        dest_label.config(text="No Source Folder Selected")
    else:
        if len(dest) > 71:
            dest_label.config(text='...'+dest[-70:])
        else:
            dest_label.config(text=dest)


def ProcessImage(source, dest, file, dest_format):
    im1 = PIL.Image.open(source+'/'+file)
    im1.save(dest+'/'+os.path.splitext(file)[0]+dest_format)


def SetSourceFormat():
    config["source_format"] = source_format_var.get()


def SetDestFormat():
    config["dest_format"] = dest_format_var.get()


def RunImageConversion():
    files = config["files"]
    source = config["source"]
    dest = config["dest"]
    dest_format = dest_format_var.get()

    if source != '' and dest != '':
        run_label.config(text="Now Running")

        if int(multiprocessing_var.get()) > 1:
            try:
                source_tuple = [source]*len(files)
                dest_tuple = [dest]*len(files)
                files_tuple = files
                dest_format_tuple = [dest_format]*len(files)

                iter_var = [*zip(source_tuple, dest_tuple,
                                 files_tuple, dest_format_tuple)]

                pool = multiprocessing.Pool(int(multiprocessing_var.get()))
                pool.starmap(ProcessImage, iterable=iter_var)

            except Exception as e:
                print(e)
                showerror('Error', "Multiprocessing error")
            finally:
                pool.close()
                pool.join()
                run_label.config(text="Done! Ready for next job.")

        elif int(multiprocessing_var.get()) <= 0:
            showerror('Error', "Invalid core count (cannot be 0).")
            run_label.config(text="Not Running.")

        else:
            for file in files:
                ProcessImage(source, dest, file, dest_format)
            run_label.config(text="Done! Ready for next job.")

    else:
        showerror('Error', "Missing directory, try again.")


if __name__ == "__main__":
    config = {"source": '', "dest": '', 'multiprocessing': '1',
              "source_format": '.CR2', "dest_format": '.PNG', "files": []}
    metrix = {"num_in": 0}

    format_options = [".BLP", ".BMP", ".CR2", ".DDS", ".DIB", ".EPS", ".ICNS",
                      ".ICO", ".IM", ".JPEG", ".MSP", ".PCX", ".PNG", ".PPM", ".SGI", ".TIFF", ".TIF"]

    window = Tk()  # init window
    window.geometry("600x400")  # set window size
    window.configure(bg='black')
    window.resizable(True, True)

    source_format_var = StringVar(window)
    source_format_var.set(".CR2")
    dest_format_var = StringVar(window)
    dest_format_var.set(".PNG")
    multiprocessing_var = StringVar(window)
    multiprocessing_var.set("1")

    window.title("DG Image Converter")
    window.iconbitmap('DGLogoWhiteBG.ico')

    img = ImageTk.PhotoImage(PIL.Image.open(
        "DGLogoBlackBG.png").resize((50, 50)))

    logo_frame = Frame(window, width=2, height=2)
    logo_label = Label(logo_frame, image=img, relief="solid")
    logo_frame.pack()
    logo_label.pack()

    padding = 10

    welcome = Label(window, text="Welcome to DG Image Converter",
                    bg='black', fg='white').pack()
    config_frame = Frame(window)
    config_frame.config(bg='black', pady=padding)
    config_frame.pack()
    source_frame = Frame(window)
    source_frame.config(bg='black', pady=padding)
    source_frame.pack()
    dest_frame = Frame(window)
    dest_frame.config(bg='black', pady=padding)
    dest_frame.pack()
    multiprocessing_frame = Frame(window)
    multiprocessing_frame.config(bg='black', pady=padding)
    multiprocessing_frame.pack()
    run_frame = Frame(window)
    run_frame.config(bg='black', pady=padding)
    run_frame.pack()

    source_format_dropdown = OptionMenu(
        config_frame, source_format_var, *format_options, command=SetSourceFormat())
    dest_format_dropdown = OptionMenu(
        config_frame, dest_format_var, *format_options, command=SetDestFormat())
    config_label = Label(config_frame, text=" ----->", bg='black', fg='white')
    source_format_dropdown["highlightthickness"] = 0
    dest_format_dropdown["highlightthickness"] = 0

    source_label = Label(
        source_frame, text="No Source Folder Selected", bg='black', fg='white')
    source_button = Button(source_frame, text="Browse",
                           fg="black", command=GetSourceFolder)
    source_count_label = Label(
        source_frame, text="0 files found", bg='black', fg='white')

    dest_label = Label(
        dest_frame, text="No Destination Folder Selected", bg='black', fg='white')
    dest_button = Button(dest_frame, text="Browse",
                         fg="black", command=GetDestFolder)

    multiprocessing_var = IntVar()
    multiprocessing_label = Label(
        multiprocessing_frame, text="Number of Cores (max "+str(os.cpu_count())+"):", bg='black', fg='white')
    multiprocessing_input = Entry(
        multiprocessing_frame, width=2, textvariable=multiprocessing_var)
    # multiprocessing_input.insert(0,"0")

    run_label = Label(run_frame, text="Not Running.", bg='black', fg='white')
    run_button = Button(run_frame, text="Convert Files",
                        fg="black", command=RunImageConversion)

    source_format_dropdown.grid(row=0, column=0)
    config_label.grid(row=0, column=1)
    dest_format_dropdown.grid(row=0, column=2)

    source_label.grid(row=0, column=0)
    source_button.grid(row=0, column=1)
    source_count_label.grid(row=1, column=0)

    dest_label.grid(row=0, column=0)
    dest_button.grid(row=0, column=1)

    multiprocessing_label.grid(row=0, column=0)
    multiprocessing_input.grid(row=0, column=1)

    run_button.grid(row=0, column=0)
    run_label.grid(row=1, column=0)

    window.mainloop()  # show window

    pass
