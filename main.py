from tkinter import *
from tkinter import filedialog
from PIL import Image ,ImageDraw ,ImageFont,ImageTk
import webbrowser
import cv2
import random

def upload_file():
    filename = filedialog.askopenfilename(title="select Image",filetypes=[
                    ("image", ".jpeg"),
                    ("image", ".png"),
                    ("image", ".jpg"),
                ])
    upload_entry.delete(0,END)
    upload_entry.insert(0,string=filename)
    change_canvas_image(filename)

    print(filename)

def add_watermark():
    filepath = upload_entry.get()
    watermark_text = watermark_entry.get()
    image = Image.open(filepath).copy()
    width, height = image.size

    draw = ImageDraw.Draw(image)
    text = watermark_text
    font_size = round(height / 10)
    font = ImageFont.truetype('arial.ttf', font_size)
    textwidth, textheight = draw.textsize(text, font)

    # calculate the x,y coordinates of the text
    margin = 10
    x = width - textwidth - margin
    y = height - textheight - margin
    # draw watermark in the bottom right corner
    draw.text((x,y), text, font=font,fill="red")

    # Save watermarked image
    image.save('watermarked_image.png')
    change_canvas_image("watermarked_image.png")

    #using opencv
    # img = cv2.imread(filepath)
    # font = cv2.FONT_HERSHEY_SIMPLEX
    # cv2.putText(img,watermark_text,(100,200), font, 1,(255,10,255),2,cv2.LINE_AA)
    # cv2.imshow("Display Image",img)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    # cv2.imwrite(f"watermarked_image({random.randint(0,100)}).jpg",img)


def change_canvas_image(filepath):
    naive_img = Image.open(filepath)
    new_img = ImageTk.PhotoImage(naive_img.resize((600, 300)))
    image_a = canvas.create_image(300, 150, image=new_img)
    canvas.itemconfig(show_image, image=image_a)


def save_image():
    save_path = filedialog.asksaveasfile(initialfile="watermarked_image.png",
                                         title="save path",
                                         defaultextension=".png",
                                         filetypes=[("All Files", "*.*")],
                                         ).name
    final_image = Image.open("watermarked_image.png")
    final_image.save(save_path)
    webbrowser.open(save_path)

window = Tk()
window.title("waternmarking on image app")
window.config(padx=100,pady=50,bg="skyblue",highlightthickness=0)
window.minsize(width=800,height=600)

title_label = Label(text="Image",font=("Arial",24,"bold"),fg="GREEN",bg="skyblue")
title_label.grid(column=1,row=0)

canvas = Canvas(width=600,height=300)
img = Image.open("start_image.png")
title_image = ImageTk.PhotoImage(img.resize((600,300)))
show_image = canvas.create_image(300,150,image=title_image)
canvas.grid(column=0,row=1,pady=30,columnspan=3)

upload_label = Label(text="Image path:" ,font=("Arial",15,"bold"),bg="skyblue")
upload_label.grid(column=0,row=2)

upload_entry = Entry(width=30)
upload_entry.grid(column=1,row=2)

upload_btn = Button(text="Upload" ,width=15,command=upload_file)
upload_btn.grid(column=2,row=2)


watermark_label = Label(text="watermark text:" ,font=("Arial",15,"bold"),bg="skyblue")
watermark_label.grid(column=0,row=3)

watermark_entry = Entry(width=30)
watermark_entry.grid(column=1,row=3)

watermark_add_btn = Button(text="Add",width=15,command=add_watermark)
watermark_add_btn.grid(column=2,row=3)

save_btn = Button(text="SAVE",command=save_image,width=25,pady=5)
save_btn.grid(column=1,row=4,pady=10)

window.mainloop()
