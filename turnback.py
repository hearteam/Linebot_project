from predict2 import Pred
import os

if __name__=="__main__":
    IMG = os.listdir("./img")
    for I in IMG:
        filepath = "./img"+"/"+ I
        classname = Pred().get_pred(filepath)
        print(classname)
        Pred().get_img(filepath)
        os.remove(filepath)

