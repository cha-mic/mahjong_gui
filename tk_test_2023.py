from textwrap import dedent
from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image

def main():

    root = Tk()
    root.title("my first app")

    img_5p_aka = Image.open('./img/_5p_aka.png')
    # global photo_5p_aka
    photo_5p_aka = ImageTk.PhotoImage(img_5p_aka)
    global canvas
    canvas = Canvas(root, bg = "white", width = 200, height  =200)

    frame1 = ttk.Frame(root, padding = 16)
    label1 = ttk.Label(frame1, text = 'Your name')
    t = StringVar()
    entry1 = ttk.Entry(frame1, textvariable = t)
    button1 = ttk.Button(
        frame1,
        text = 'OK',
        command = lambda: display_image(photo_5p_aka)
    )

    frame1.pack()
    label1.pack(side = LEFT)
    entry1.pack(side = LEFT)
    button1.pack(side = RIGHT)


    root.mainloop()


def display_image( img ):

    # img_5p_aka = Image.open('./img/_5p_aka.png')
    # global photo_5p_aka
    # photo_5p_aka = ImageTk.PhotoImage(img)
    

    canvas.create_image(0, 0, image = img, anchor = NW)
    canvas.pack()

if __name__ == '__main__':
    main()