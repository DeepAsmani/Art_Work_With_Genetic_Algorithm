import glob
import os
import cv2
from PIL import Image


def save(filename1,lastname):
    img_array = []
    i = 0
    j = 0
    for filename in glob.glob(".//"+filename1+"//*.png"):
        if os.path.exists(".//"+filename1+"//"+str(i)+".png") and i<lastname:
            img = Image.open(".//"+filename1+"//"+str(i)+".png")
            img_array.append(img)
            i = i+j
            j = j+1
        else:
            img = Image.open(".//"+filename1+"//"+str(lastname)+".png")
            img_array.append(img)
            break
    frame_one = img_array[0]
    frame_one.save(filename1+".gif", format="GIF",
                   append_images=img_array, save_all=True, duration=100, loop=0)
    print("////////////////////////////")


#if __name__ == "__main__":
#    save("landscape_OutPut",7136)
