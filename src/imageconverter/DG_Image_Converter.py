import glob
from PIL import ImageTk
import PIL.Image
import PIL.ImageDraw
import PIL.ImageFont
import tkinter.filedialog
from tkinter import *
from tkinter.messagebox import showerror
import os
import multiprocessing
import sys
# from rawkit import Cr2
# import exif

# import threading
# class windowthread(threading.Thread):
#     def __init__(self):
#         threading.Thread.__init__(self)
#     def run(self):
#         pass

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)


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


def ProcessImage(source, dest, file, dest_format, source_format, watermark, resize_x, resize_y, prefix, suffix):
    im1 = PIL.Image.open(source+'/'+file)
    if source_format == '.PNG' and dest_format == '.JPG':
        im1 = im1.convert('RGB') 
    
    if resize_x == 0 and resize_y == 0:
        pass
    
    elif resize_x == 0 and resize_y != 0:
        width, height = im1.width, im1.height
        AR = height/width
        # maintian AR
        w_n = int(resize_y/height*width)
        
        # resize to height
        im1 = im1.resize((w_n, resize_y))
        
    elif resize_x != 0 and resize_y == 0:
        width, height = im1.width, im1.height
        AR = height/width
        #maintain AR
        h_n = int(resize_x/width*height)
        
        # resize to width
        im1 = im1.resize((resize_x, h_n))

    elif resize_x != 0 and resize_y != 0:
        # resize both
        im1 = im1.resize((resize_x, resize_y))
        
    if watermark != "":
        width, height = im1.width, im1.height
        
        font = PIL.ImageFont.truetype("Helvetica-Bold.ttf",int(height*0.025))
        w,h = font.getsize(watermark)
        
        w_margin = 0.02
        h_margin = 0.05
        
        draw = PIL.ImageDraw.Draw(im1)

        draw.rectangle(((width-w)-2*w_margin*w, (height-h)-2*h_margin*h, width, height), fill=(0,0,0))
        draw.text(((width-w)-w_margin*w,(height-h)-h_margin*h),watermark,fill=(255,255,255),font=font)
    
    im1.save(dest+'/'+prefix+os.path.splitext(file)[0]+suffix+dest_format)


def SetSourceFormat():
    config["source_format"] = source_format_var.get()


def SetDestFormat():
    config["dest_format"] = dest_format_var.get()


def RunImageConversion():
    files = config["files"]
    source = config["source"]
    dest = config["dest"]
    watermark = watermark_var.get()
    resize_x = resize_x_var.get()
    resize_y = resize_y_var.get()
    prefix = prefix_var.get()
    suffix = suffix_var.get()
    
    dest_format = dest_format_var.get()
    source_format = source_format_var.get()
    
    
    if source != '' and dest != '':
        run_label.config(text="Now Running")

        if int(multiprocessing_var.get()) > 1:
            try:
                source_tuple = [source]*len(files)
                dest_tuple = [dest]*len(files)
                files_tuple = files
                dest_format_tuple = [dest_format]*len(files)
                source_format_tuple = [source_format]*len(files)
                watermark_tuple = [watermark]*len(files)
                resize_x_tuple = [resize_x]*len(files)
                resize_y_tuple = [resize_y]*len(files)
                prefix_tuple = [prefix]*len(files)
                suffix_tuple = [suffix]*len(files)
                
                iter_var = [*zip(source_tuple, dest_tuple,
                                 files_tuple, dest_format_tuple, 
                                 source_format_tuple, watermark_tuple,
                                 resize_x_tuple, resize_y_tuple, 
                                 prefix_tuple, suffix_tuple)]

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
                ProcessImage(source, dest, file, dest_format, source_format, watermark, resize_x, resize_y, prefix, suffix)
            run_label.config(text="Done! Ready for next job.")

    else:
        showerror('Error', "Missing directory, try again.")


if __name__ == "__main__":
    config = {"source": '', "dest": '', 'multiprocessing': '1',
              "source_format": '.CR2', "dest_format": '.PNG', "files": [], "watermark": u"\u00A9", "resize_x": '', "resize_y": '', "prefix": '', "suffix": ''}
    
    metrix = {"num_in": 0}

    format_options = [".BLP", ".BMP", ".CR2", ".DDS", ".DIB", ".EPS", ".FLIF", ".ICNS",
                      ".ICO", ".IM", ".JPG", ".MSP", ".PCX", ".PNG", ".PPM", ".SGI", ".TIFF", ".TIF"]

    window = Tk()  # init window
    window.geometry("600x500")  # set window size
    window.configure(bg='black')
    window.resizable(True, True)

    source_format_var = StringVar(window)
    source_format_var.set(".CR2")
    
    dest_format_var = StringVar(window)
    dest_format_var.set(".PNG")
    
    multiprocessing_var = StringVar(window)
    multiprocessing_var.set("1")
    
    watermark_var = StringVar(window)
    watermark_var.set(u"\u00A9")
    
    prefix_var = StringVar(window)
    prefix_var.set("")
    suffix_var = StringVar(window)
    suffix_var.set("")
    
    window.title("DG Image Converter")
    
    window.iconbitmap(r'DGLogoWhiteBG.ico')
    
    img = ImageTk.PhotoImage(PIL.Image.open(
        r"DGLogoBlackBG.ico").resize((50, 50)))

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
    watermark_frame = Frame(window)
    watermark_frame.config(bg='black', pady=padding)
    watermark_frame.pack()
    resize_frame = Frame(window)
    resize_frame.config(bg='black', pady=padding)
    resize_frame.pack()
    naming_frame = Frame(window)
    naming_frame.config(bg='black', pady=padding)
    naming_frame.pack()
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
    multiprocessing_var.set(1)
    
    watermark_label = Label(
        watermark_frame, text="Watermark:", bg='black', fg='white')
    watermark_input = Entry(
        watermark_frame, width=30, textvariable=watermark_var)
    
    resize_x_var = IntVar()
    resize_y_var = IntVar()
    resize_label = Label(
        resize_frame, text="Resize image (0 will maintain AR):", bg='black', fg='white')
    resize_x_input = Entry(
        resize_frame, width=10, textvariable=resize_x_var)
    resize_label_2 = Label(
        resize_frame, text=" x ", bg='black', fg='white')
    resize_y_input = Entry(
        resize_frame, width=10, textvariable=resize_y_var)
    
    naming_label = Label(
        naming_frame, text="Prefix:", bg='black', fg='white')
    prefix_input = Entry(
        naming_frame, width=10, textvariable=prefix_var)
    naming_label_2 = Label(
        naming_frame, text="Suffix:", bg='black', fg='white')
    suffix_input = Entry(
        naming_frame, width=10, textvariable=suffix_var)
    
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

    watermark_label.grid(row=0, column=0)
    watermark_input.grid(row=0, column=1)
    
    resize_label.grid(row=0, column=0)
    resize_x_input.grid(row=0, column=1)
    resize_label_2.grid(row=0, column=2)
    resize_y_input.grid(row=0, column=3)
    
    naming_label.grid(row=0, column=0)
    prefix_input.grid(row=0, column=1)
    naming_label_2.grid(row=0, column=2)
    suffix_input.grid(row=0, column=3)
    
    run_button.grid(row=0, column=0)
    run_label.grid(row=1, column=0)

    window.mainloop()  # show window

    pass
