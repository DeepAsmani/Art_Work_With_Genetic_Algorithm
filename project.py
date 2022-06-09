import io
import os
import PySimpleGUI as sg
import cv2
import numpy as np
import multiprocessing as mp
import shutil
from tkinter import font
from turtle import color
from PIL import Image
from matplotlib.pyplot import text
from numpy import size
import main_Project
import test


file_types = [("JPEG (*.jpg)", "*.jpg"),
              ("All files (*.*)", "*.*")]

sg.theme('LightBrown10')

def mainrun(imgcorp, name, shape):
    p = [i for i in range(0, len(imgcorp))]
    for i in range(0, len(imgcorp)):
        p[i] = mp.Process(target=main_Project.mainclass, args=(
            imgcorp[i], "Process : "+str(i+1), name, len(imgcorp), shape,))
        p[i].start()

def image_windows(filename, shape):
    # print(shape)

    layout = [
        [
            [
                sg.Text("Output :", font=('Helvetica', 20, 'bold')),
            ],
            [
                sg.Text("Marign of Error : ", key="-marerror-",font=('Helvetica', 20, 'bold')),
            ],
            [
                sg.HorizontalSeparator(),
            ],
            [[
            sg.Column(
                [
                    [
                        sg.Image(key="-INPUTIMAGE-",
                                 background_color='black', pad=(0, 0)),
                    ],
                ]
            ),
            sg.VSeperator(),
            sg.Column(
                [
                    [
                        sg.Image(key="-OUTPUTIMAGE-",pad=(0,0)),
                    ],
                ]
            ),],
            [
                sg.HorizontalSeparator(),
            ],
            [
                sg.Button("Save Video", font=(
                            'Helvetica', 11, 'bold'), size=(12, 2))
            ],
            ],
        ]
    ]

    cntmainrun = 0

    window = sg.Window("Artwork Using Genetic Algorithm", resizable=True, element_justification='center', size=(
        800, 600), margins=(50, 50), modal=True).Layout(layout)

    perverror=0

    while True:
        event, values = window.read(timeout=0)
        if event == "Exit" or event == sg.WIN_CLOSED:
            for i in range(0,len(imgcorp)):
              shutil.rmtree(name+"_OutPut//Part_"+str(i)+"//")
            break
        img = cv2.imread(filename)
        img = cv2.resize(img, (300, 300))
        bio = io.BytesIO(cv2.imencode(".png", img)[1])
        window["-INPUTIMAGE-"].update(data=bio.getvalue())
        if cntmainrun == 0:
            path = filename
            img = cv2.imread(path)
            img = cv2.resize(img, (300, 300))
            imgcorp = []
            part=75
            for r in range(0, img.shape[0], part):
                for c in range(0, img.shape[1], part):
                    imgcorp.append(img[r:r+part, c:c+part, :])
            #print(len(imgcorp))
            name = str(os.path.splitext(os.path.basename(path))[0])
            if os.path.exists(name+"_OutPut"):
                shutil.rmtree(name+"_Output//")
            os.mkdir(name+"_OutPut")
            for i in range(0, len(imgcorp)):
                os.mkdir(name+"_OutPut//Part_"+str(i))
            outprocess = mp.Process(
                target=mainrun, args=(imgcorp, name, shape,))
            outprocess.start()
            cntmainrun = 1
            tempimg = [i for i in range(0, len(imgcorp))]
            savecnt = 0
            savename = 0
            for i in range(0, len(imgcorp)):
                tempimg[i] = np.ones((imgcorp[0].shape), dtype=np.uint8) * 255
            cnt = [50 for i in range(0,len(imgcorp))]

        for i in range(0, len(imgcorp)):
            if os.path.exists(name+"_OutPut//Part_"+str(i)+"//"+str(cnt[i])+".png"):
                tempimg[i] = cv2.imread(
                    name+"_OutPut//Part_"+str(i)+"//"+str(cnt[i]-50)+".png")
                cnt[i] = cnt[i]+50
        conimg=[[0 for x in range(int(300/part))] for x in range(int(300/part))]
        #print(conimg)
        mcnt=0
        for i in range(0,int(300/part)):
            for j in range(0,int(300/part)):
                conimg[i][j]=tempimg[mcnt]
                mcnt=mcnt+1
                #print(mcnt)
        new=cv2.vconcat([cv2.hconcat(im_list_h) for im_list_h in conimg])
        new = cv2.resize(new, (300, 300))
        bio1 = io.BytesIO(cv2.imencode(".png", new)[1])

        err = np.sum((img.astype("float") -
                         new.astype("float")) ** 2)
        err /= float(img.shape[0] * new.shape[1])
        #err = cv2.absdiff(img, new)
        #err = err.astype(np.uint8)
        #err = (np.count_nonzero(err)*100)/err.size
        #err="{:.2f}".format(err)
        if err != perverror:
            perverror=err
            cv2.imwrite(
                name+"_OutPut//{}.png".format(savename), new)
            savename = savename+1
            savecnt = 0
        err="{:.2f}".format(err)
        window["-OUTPUTIMAGE-"].update(data=bio1.getvalue())
        window["-marerror-"].update("Fitness : "+str(err))
        if event=="Save Video":
            #video = mp.Process(
            #    target=test.save(), args=(name+"_OutPut",savename-1,))
            #video.start()
            test.save(name+"_OutPut",(savename-1))
    window.close()


def main():
    layout = [
        [
            sg.Column(
                [
                    [
                        sg.Text("Image File: ", font=(
                            'Helvetica', 14, 'bold')),
                        sg.Input(size=(25, 1), key="-FILE-"),
                        sg.FileBrowse(file_types=file_types, font=('Helvetica', 11,
                                                                   'bold'), size=(12, 1)),
                        sg.Button("Load Image", font=('Helvetica', 11,
                                  'bold'), size=(12, 1)),
                    ],
                    # [

                    # ],
                    [
                        sg.Text("Select Shape : ", font=(
                            'Helvetica', 14, 'bold')),
                        sg.Radio('Polygon', 'filtertpye',
                                 enable_events=True, default=True, key="Polygon", font=('Helvetica', 13, 'bold')),
                        sg.Radio('Ellipse', 'filtertpye',size=(14,2),
                                 enable_events=True, key="Ellipse", font=('Helvetica', 13, 'bold')),
                    ],
                    [
                        sg.HorizontalSeparator(),
                    ],
                    [
                        sg.Image(key="-IMAGE-", background_color="yellow",pad=(10,10))
                    ],
                    [
                        sg.HorizontalSeparator(),
                    ],
                    [
                        sg.Button("Create", font=(
                            'Helvetica', 11, 'bold'), size=(12, 2))
                    ]
                ],
            element_justification='center'),
        ]
    ]

    window = sg.Window("Arkwork using Genetic Algorithm", resizable=True, element_justification='center', size=(
        600, 500), margins=(20, 20)).Layout(layout)

    shape = "Polygon"
    filename = ""

    cnt = 0
    img = np.ones((300, 300, 3), dtype=np.uint8) * 255
    font = cv2.FONT_HERSHEY_SIMPLEX
    img = cv2.putText(img, 'Select Image', (50,150), font, 
                   1, (0,0,0), 2, cv2.LINE_AA)

    while True:
        event, values = window.read(timeout=0)
        if event == "Exit" or event == sg.WIN_CLOSED:
            break
        if event == "Load Image":
            filename = values["-FILE-"]
            if os.path.exists(filename):
                img = cv2.imread(filename)
                img = cv2.resize(img, (300, 300))
                cnt = 1
        bio = io.BytesIO(cv2.imencode(".png", img)[1])
        window["-IMAGE-"].update(data=bio.getvalue())
        if values["Ellipse"]:
            shape = "Ellipse"
        else:
            shape = "Polygon"
        if event == "Create":
            if cnt == 1:
                if os.path.exists(filename):
                    window.close()
                    image_windows(filename, shape)
            
    window.close()


if __name__ == "__main__":
    main()
