from tkinter import *
from PIL import ImageTk, Image  

app = Tk()
app.title("Welcome")
img =Image.open('/home/mohamed/GL4/WeChat/assets/bg_login_2.jpg')
bg = ImageTk.PhotoImage(img)

app.geometry("650x450")

# Add image
label = Label(app, image=bg)
# label.place(x = 0,y = 0)
label.pack(fill="both")

# Add text
label2 = Label(app, text = "Hello kittens",
               font=("Times New Roman", 24))

label2.pack(pady = 50)

# Execute tkinter
app.mainloop()