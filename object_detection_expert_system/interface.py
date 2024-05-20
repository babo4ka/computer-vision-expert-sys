import os
import tkinter as tk
from tkinter import *
from tkinter import filedialog as fd

from PIL import ImageTk, Image
from imageai.Detection import ObjectDetection

width = 600
height = 400

exec_path = os.getcwd()

# модель для распознавания
detector = ObjectDetection()
detector.useCPU()
detector.setModelTypeAsRetinaNet()
detector.setModelPath(os.path.join(exec_path, "retina.pth"))
detector.loadModel()




def detectObjects():
    filename = fd.askopenfilename()

    print(filename)
    detections = detector.detectObjectsFromImage(
        input_image=filename,
        output_image_path="detected.png",
        minimum_percentage_probability=30, output_type="file")

    objects = {}

    for item in detections:
        if item['name'] not in objects.keys():
            objects[item['name']] = 0
        objects[item['name']] += 1

        print(item)
    print(len(detections))
    print(objects)

    global input_photo_showed, input_photo, output_photo, button_showed

    inputImageFile = Image.open(filename)
    inputImageFile = inputImageFile.resize((width, height))
    inputImagePhoto = ImageTk.PhotoImage(inputImageFile)
    input_photo = inputImagePhoto
    imageToShow.config(image=inputImagePhoto)
    imageToShow.image = inputImagePhoto
    input_photo_showed = True

    outputImageFile = Image.open("detected.png")
    outputImageFile = outputImageFile.resize((width, height))
    outputImagePhoto = ImageTk.PhotoImage(outputImageFile)
    output_photo = outputImagePhoto

    text = "Найдено объектов: \n"
    for key in objects.keys():
        print(str(key) + ": " + str(objects[key]))
        text += str(key) + ": " + str(objects[key]) + "\n"
    objectsCountLabel.config(text=text)
    objectsCountLabel.text = text

    if not button_showed:
        swap_image_btn = tk.Button(text="Поменять фото", command=change_photo)
        swap_image_btn.pack(anchor=N)
        button_showed = True


def change_photo():
    global input_photo_showed
    if input_photo_showed:
        imageToShow.config(image=output_photo)
        imageToShow.image = output_photo
        input_photo_showed = False
    else:
        imageToShow.config(image=input_photo)
        imageToShow.image = input_photo
        input_photo_showed = True


button_showed = False

input_photo = None
output_photo = None

input_photo_showed = True

# пользовательский интерфейс
window = tk.Tk()
window.geometry('1200x600')

header_frame = LabelFrame(window)
header_frame.pack()
header = tk.Label(header_frame, text="Распознавание объектов на фотографии",
                  font=100)
header.pack()

fileChooser = tk.Button(text="Выбери файл", command=detectObjects)
fileChooser.pack()

objectsCountLabel = tk.Label(text="Найдено объектов:", justify=LEFT, font=500)
objectsCountLabel.pack(anchor=NW)


content_frame = LabelFrame(window)
content_frame.pack()

# content_frame.columnconfigure(0, weight=1)
# content_frame.columnconfigure(1, weight=1)

imageToShow = tk.Label(content_frame)
imageToShow.pack()

window.mainloop()
