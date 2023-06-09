# Workshop 2 Group 3
# Group Members:
# 1) Sue Chen Xiang B032010034
# 2. Fatin Najdah binti Najmi Ismail B032010201 
# 3. Nur Afiqah binti Anuar B032010114 
# 4. Ken Prameswari Caesarella B032010461 
# 5. Mohammad Irsyad bin Mohd Shahril B032010242

import cv2
import numpy as np
import os
import threading
import queue

INPUT_WIDTH = 640
INPUT_HEIGHT = 640
THRESHOLD = 0.25
CLASSES = ['ApolloChocolateCake', 'ApolloChocolateWaferCream', 'ChipsMoreMini', 'GardeniaCreamRoll', 'JuliePeanutButterSandwich', 'MaggiCurry', 'OralBToothBrush']
np.random.seed(42)

###################### use product_counting method to get product data ##########################
#### data = {'ApolloChocolateCake': 0, 'GardeniaCreamRoll': 0, 'MaggiCurry': 1, 'OralBToothBrush': 0}
#### data["ApolloChocolateCake"] can be used to get the quantity of ApolloChocolateCake 

class ProductDetection:
    def __init__(self):
        self.currentdir = os.path.dirname(os.path.realpath(__file__))
        self.net = cv2.dnn.readNetFromONNX(os.path.join(self.currentdir,"product_detection_model.onnx"))
        self.colors = np.random.uniform(0, 255, size=(len(CLASSES), 3))
        self.product_count = {label:0 for label in CLASSES if label != "JuliePeanutButterSandwich"}
        self.class_ids = []
        self.stop_program_event = threading.Event()
        self.wait = True
        self.frames = queue.Queue()

    def start(self, src=0, test=False):
        thread = threading.Thread(target=self.start_program, args=(src, test), daemon=True)
        thread.start()

    def start_program(self, source=0, test=False):
        cam = cv2.VideoCapture(source)
        # cam = cv2.VideoCapture("http://192.168.3.25:4747/video")
        # cam.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        # cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 640)

        while not self.stop_program_event.is_set():
            ret, frame = cam.read()

            if not ret:
                break

            pred = self.detect(frame)

            class_ids, confidences, boxes = self.analyse_detection(frame, pred[0])
            print(boxes)

            frame = self.draw_box(frame, class_ids, confidences, boxes)

            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            if not self.frames.empty():
                try:
                    self.frames.get_nowait()
                except queue.Empty:
                    pass
            self.frames.put(frame_rgb)

            if self.wait:
                self.wait = False

            k = cv2.waitKey(20)

            if test:
                cv2.imshow("detect", frame)
                if k == ord("q"):
                    break

            if self.stop_program_event.is_set():
                break

            self.class_ids = class_ids

        cam.release()
        cv2.destroyAllWindows()

    def get_frame(self):
        return self.frames.get()

    def end_program(self):
        self.stop_program_event.set()
        return self.product_count

    def product_counting(self):
        for id in self.class_ids:
            class_name = CLASSES[id]
            self.product_count[class_name] += 1
        print(self.product_count)
        return self.product_count
    
    def reset_product_counting(self):
        self.product_count = {label:0 for label in CLASSES if label != "JuliePeanutButterSandwich"}

    def detect(self, img):
        blob = cv2.dnn.blobFromImage(img, 1/255.0, (640,640), swapRB=True)
        self.net.setInput(blob)
        preds = self.net.forward()
        # print(preds[0])
        return preds

    def analyse_detection(self, frame, output_data):
        class_ids = []
        confidences = []
        boxes = []

        rows = output_data.shape[0]

        img_width, img_height, _ = frame.shape

        x_factor = img_width / INPUT_WIDTH
        y_factor = img_height / INPUT_HEIGHT

        for r in range(rows):
            row = output_data[r]
            confidence = row[4]

            if confidence >= THRESHOLD:
                classes_scores = row[5:]
                _, _, _, max_indx = cv2.minMaxLoc(classes_scores)
                print(f"max_indx {max_indx}")
                class_id = max_indx[1]

                if(classes_scores[class_id] > 0.25):
                    if class_id == 4: continue
                    confidences.append(confidence)
                    class_ids.append(class_id)

                    x, y, w, h = row[0].item(), row[1].item(), row[2].item(), row[3].item()
                    xmin = int((x - w/2) * x_factor)
                    ymin = int((y - h/2) * y_factor)
                    xmax = int((x + w/2) * x_factor)
                    ymax = int((y + h/2) * y_factor)
                    box = np.array([xmin, ymin, xmax, ymax])
                    boxes.append(box)

        indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.25, 0.45) 

        result_class_ids = []
        result_confidences = []
        result_boxes = []

        for i in indexes:
            result_confidences.append(confidences[i])
            result_class_ids.append(class_ids[i])
            print(CLASSES[class_ids[i]])
            result_boxes.append(boxes[i])
            print("old old", boxes[i])

        return result_class_ids, result_confidences, result_boxes

    def draw_box(self, frame, class_ids, confidences, bboxes):
        for box_num, box in enumerate(bboxes):
            # Need the image height and width to denormalize
            # the bounding box coordinates
            h, w, _ = frame.shape
            print(f"h:{h} w:{w}")

            xmin, ymin, xmax, ymax = box
            print(box, "buibiu", xmin, ymin,xmax,ymax)

            print("new new",xmin,ymin,xmax,ymax)

            if xmin < 0:
                xmin = 15
            elif ymin < 0:
                ymin = 15
            elif xmax > w:
                xmax = w - 15
            elif ymax > h:
                ymax = h - 15

            class_name = CLASSES[int(class_ids[box_num])]

            cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), self.colors[int(class_ids[box_num])], thickness=3)
            
            font_scale = 0.5
            font_thickess = 1

            pt1 = (int(xmin), int(ymin))
            pt2 = (int(xmax), int(ymax))

            text_width, text_height = cv2.getTextSize(f"{class_name} {'{:.2f}'.format(confidences[box_num])}", 0, fontScale=font_scale, thickness=font_thickess)[0]
            print(f"text w: {text_width} text h: {text_height}")

            pt2 = pt1[0] + text_width + 20, pt1[1] + -text_height - 10

            cv2.rectangle(frame, pt1, pt2, color=self.colors[int(class_ids[box_num])], thickness=-1)

            cv2.putText(frame, f"{class_name} {'{:.2f}'.format(confidences[box_num])}", (xmin+1, ymin-10), cv2.FONT_HERSHEY_COMPLEX, font_scale, (255,255,255), thickness=font_thickess)

        return frame

    def test(self):
        path = os.path.join(self.currentdir, "model_training/yolov5/inference_images/1.jpg")
        frame = cv2.imread(path)
        pred = self.detect(frame)
        class_ids, confidences, boxes = self.analyse_detection(frame, pred[0])
        frame = self.draw_box(frame, class_ids, confidences, boxes)
        cv2.imshow("detect", frame)
        k = cv2.waitKey(0)
        self.product_counting() 
        cv2.destroyAllWindows()

if __name__ == "__main__":
    app = ProductDetection()
    app.start_program(test=True)
    app.product_counting()
    print(os.path.dirname(os.path.realpath(__file__)))
