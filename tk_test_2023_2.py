from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image

tehai_count = 0

def display_tehai( img ):

    global tehai_count
    canvas.create_image(tehai_count * 40 + 3, 3, image = img, anchor = NW)

    tehai_count = tehai_count + 1


if __name__ == '__main__':

    root = Tk()
    root.title("my first app")

    img_5p_aka = Image.open('./img/_5p_aka.png')
    photo_5p_aka = ImageTk.PhotoImage(img_5p_aka)

    canvas = Canvas(root, bg = "white", width = 40 * 14 + 50, height = 40 + 6)

    frame1 = ttk.Frame(root, padding = 16)
    label1 = ttk.Label(frame1, text = '手牌')
    button1 = ttk.Button(
        frame1,
        image = photo_5p_aka,
        command = lambda: display_tehai(photo_5p_aka)
    )
    button2 = ttk.Button(
        frame1,
        image = photo_5p_aka,
        command = lambda: display_tehai(photo_5p_aka)
    )

    # frame1.grid(row = 1, column = 0)
    # # canvas.grid(row = 1, column = 0)
    # label1.grid(row = 2, column = 0)
    # canvas.grid(row = 0, column = 0)
    # # entry1.pack(side = LEFT)
    # button1.grid(row = 3, column = 0)
    # # canvas.pack(side = TOP)

    frame1.pack(side = BOTTOM)
    label1.pack(side = TOP)
    button1.pack(side = LEFT)
    button2.pack(side = LEFT)
    canvas.pack(side = TOP)





    root.mainloop()


