from imageai.Detection import ObjectDetection
import os

exec_path = os.getcwd()

detector = ObjectDetection()
detector.useCPU()
detector.setModelTypeAsRetinaNet()
detector.setModelPath(os.path.join(exec_path, "retina.pth"))
detector.loadModel()
detections = detector.detectObjectsFromImage(
    input_image="objs.jpg",
    output_image_path="image2new.jpg",
    minimum_percentage_probability=30, output_type="file")


for eachObject in detections:
    print(eachObject["name"] , " : ", eachObject["percentage_probability"], " : ", eachObject["box_points"] )
    print("--------------------------------")
