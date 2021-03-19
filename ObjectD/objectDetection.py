import torch
import cv2 as cv


def response(result):
    out = {}
    for i, (img, pred) in enumerate(zip(result.imgs, result.pred)):
        if pred is not None:
            for c in pred[:, -1].unique():
                n = (pred[:, -1] == c).sum()  # detections per class
                out[result.names[int(c)]] = int(n)
    return out


class Detection:
    def __init__(self, path):
        self.image_path = path

    def detection(self):
        model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)
        image = cv.imread(self.image_path)
        results = model(image)
        dic = response(results)
        return dic


def detection(path):
    o = ObjectDetection("/home/muhammad-usman/thrift/bus.jpg")
    return o.detection()


if __name__ == '__main__':
    o = ObjectDetection("/home/muhammad-usman/thrift/bus.jpg")
    print(o.detection())
