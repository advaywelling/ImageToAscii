import tkinter as tk
from tkinter import filedialog
from PIL import Image

ASCII_CHARS = ["@", "#", "S", "%", "?", "*", "+", ";", ":", ",", "."]


def resImg(image, width2):
    width, height = image.size
    ratio = height / width / 1.65
    height2 = int(width2 * ratio)
    resizedImg = image.resize((width2, height2))
    return resizedImg


def makeGray(image):
    grayImg = image.convert("L")
    return grayImg


def pixToAsc(image):
    pixels = image.getdata()
    ascii_str = "".join([ASCII_CHARS[pixel // 25] for pixel in pixels])
    return ascii_str


def convToAsc(imgPath, new_width):
    try:
        image = Image.open(imgPath)
    except Exception as e:
        print(f"Error opening image: {e}")
        return ""

    image = resImg(image, new_width)
    image = makeGray(image)
    asciiStr = pixToAsc(image)
    numPixel = len(asciiStr)
    asciiImg = "\n".join([asciiStr[index:index + new_width]
                          for index in range(0, numPixel, new_width)])

    return asciiImg


def openImg():
    file_path = filedialog.askopenfilename()
    if file_path:
        print(f"Selected file: {file_path}")
        new_width = int(width_entry.get())
        ascii_img = convToAsc(file_path, new_width=new_width)
        if ascii_img:
            text_widget.config(state=tk.NORMAL)
            text_widget.delete("1.0", tk.END)
            text_widget.insert(tk.END, ascii_img)
            text_widget.config(state=tk.DISABLED)
            print("ASCII art generated and inserted into the text widget.")
        else:
            print("Failed to generate ASCII art.")


app = tk.Tk()
app.title("Image to ASCII Converter")
app.geometry("1000x700")
frame = tk.Frame(app)
frame.pack(padx=10, pady=10, expand=True, fill='both')
open_button = tk.Button(frame, text="Open Image", command=openImg)
open_button.pack(pady=10)
width_label = tk.Label(frame, text="Size:")
width_label.pack(pady=5)
width_entry = tk.Entry(frame)
width_entry.insert(0, "250")
width_entry.pack(pady=5)
text_frame = tk.Frame(frame)
text_frame.pack(expand=True, fill='both')
text_widget = tk.Text(text_frame, wrap=tk.NONE, font=("Courier", 8))
text_widget.pack(side=tk.LEFT, expand=True, fill='both')
scroll_y = tk.Scrollbar(text_frame, orient='vertical', command=text_widget.yview)
scroll_y.pack(side='right', fill='y')
scroll_x = tk.Scrollbar(frame, orient='horizontal', command=text_widget.xview)
scroll_x.pack(side='bottom', fill='x')
text_widget.configure(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)
app.mainloop()