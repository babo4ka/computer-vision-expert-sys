import os
import tkinter as tk
from tkinter import filedialog as fd
from tkinter import *

from PIL import ImageTk, Image
from imageai.Detection import ObjectDetection

width = 500
height = 250

exec_path = os.getcwd()

# модель для распознавания
detector = ObjectDetection()
detector.useCPU()
detector.setModelTypeAsRetinaNet()
detector.setModelPath(os.path.join(exec_path, "retina.pth"))
detector.loadModel()

# пользовательский интерфейс
window = tk.Tk()
window.geometry('800x600')

header = tk.Label(text="Распознавание объектов на фотографии",
                  font=100)
header.pack()

objects = {}

def detectObjects():
    filename = fd.askopenfilename()

    print(filename)
    detections = detector.detectObjectsFromImage(
        input_image=filename,
        output_image_path="detected.png",
        minimum_percentage_probability=30, output_type="file")

    for item in detections:
        if item['name'] not in objects.keys():
            objects[item['name']] = 0
        objects[item['name']] += 1

        print(item)
    print(len(detections))
    print(objects)

    inputImageFile = Image.open(filename)
    inputImageFile = inputImageFile.resize((width, height))
    inputImagePhoto = ImageTk.PhotoImage(inputImageFile)
    inputImage.config(image=inputImagePhoto)
    inputImage.image = inputImagePhoto

    outputImageFile = Image.open("detected.png")
    outputImageFile = outputImageFile.resize((width, height))
    outputImagePhoto = ImageTk.PhotoImage(outputImageFile)
    outputImage.config(image=outputImagePhoto)
    outputImage.image = outputImagePhoto

    text = ""
    for key in objects.keys():
        text += str(key) + ": " + str(objects[key]) + "\n"
    objectsCountLabel.config(text=text)
    objectsCountLabel.text = text
    print(text)



fileChooser = tk.Button(text="Выбери файл", command=detectObjects)
fileChooser.pack(anchor='n')

objectsCountLabel = tk.Label(text="ds")
objectsCountLabel.pack(anchor=NW)

inputImage = tk.Label(window, width=width, height=height)
inputImage.pack(anchor=W)

outputImage = tk.Label(window, width=width, height=height)
outputImage.pack(anchor=E)

window.mainloop()
