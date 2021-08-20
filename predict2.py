from PIL import Image
import os
from yolo import YOLO

class Pred():
    def __init__(self):
        self.savepath = "./imageoutput"

    def get_img(self,img_path):
        yolo = YOLO()
        mode = "predict"
        img = str(img_path)
        image_name = img.split('/')[2]
        try:
            image = Image.open(img)
        except:
            print('Open Error! Try again!')
        # 輸出圖片資訊，r_image為經過yolo模組後判定並標示後的圖片；c_image包含label及box座標資訊；c_name為加工後的label名稱
        r_image = yolo.detect_image(image)
        r_image.save(os.path.join(self.savepath, image_name))

    def get_pred(self,img_path):
        yolo = YOLO()
        mode = "predict"
        img = str(img_path)
        try:
            image = Image.open(img)
        except:
            print('Open Error! Try again!')
        # 輸出圖片資訊，r_image為經過yolo模組後判定並標示後的圖片；c_image包含label及box座標資訊；c_name為加工後的label名稱
        c_name = yolo.class_image(image)
        return (c_name)
