import cv2
import numpy as np
import pandas as pd
from tkinter import *

# Initialize window
root = Tk()
root.geometry('500x300')
root.resizable(0, 0)
root['background'] = '#90EE90'
root.title("Color Detection")
Label(root, text='Please enter your image path', font='david 16 bold', bg='#90EE90').place(x=110, y=30)

# Getting image path from user
img_path = StringVar()
Entry(root, font='david 10', textvariable=img_path, width=40, bg='ghost white').place(x=120, y=80)


# Function to show image
def showImage():
    # Reading the image with opencv
    global img
    img = cv2.imread(img_path.get())
    while 1:
        getImage()
        # Break the loop when user hits 'esc' key
        if cv2.waitKey(20) & 0xFF == 27:
            break


Button(root, font='david 10 bold', text='Get image', width=8, height=2, padx=2, bg='#3CB371', command=showImage).place(x=150, y=120)

# Declaring global variables (are used later on)
clicked = False
r = g = b = xpos = ypos = 0

# Reading csv file with pandas and giving names to each column
index = ["color", "color_name", "hex", "R", "G", "B"]
csv = pd.read_csv('colors.csv', names=index, header=None)


# Function to calculate minimum distance from all colors and get the most matching color
def getColorName(R, G, B):
    minimum = 10000
    for i in range(len(csv)):
        d = abs(R - int(csv.loc[i, "R"])) + abs(G - int(csv.loc[i, "G"])) + abs(B - int(csv.loc[i, "B"]))
        if d <= minimum:
            minimum = d
            cname = csv.loc[i, "color_name"]
    return cname


# Function to get x,y coordinates of mouse double click
def draw_function(event, x, y, flags, param):
    global img
    if event == cv2.EVENT_LBUTTONDBLCLK:
        global b, g, r, xpos, ypos, clicked
        clicked = True
        xpos = x
        ypos = y
        b, g, r = img[y, x]
        b = int(b)
        g = int(g)
        r = int(r)


# Auxiliary function to show image
def getImage():
    global img
    cv2.imshow("image", img)
    cv2.namedWindow('image')
    cv2.setMouseCallback('image', draw_function)
    global clicked
    if clicked:

        # cv2.rectangle(image, startpoint, endpoint, color, thickness)-1 fills entire rectangle
        cv2.rectangle(img, (20, 20), (750, 60), (b, g, r), -1)

        # Creating text string to display( Color name and RGB values )
        text = getColorName(r, g, b) + ' R=' + str(r) + ' G=' + str(g) + ' B=' + str(b)

        # cv2.putText(img,text,start,font(0-7),fontScale,color,thickness,lineType )
        cv2.putText(img, text, (50, 50), 2, 0.8, (255, 255, 255), 2, cv2.LINE_AA)

        # For very light colours we will display text in black colour
        if r + g + b >= 600:
            cv2.putText(img, text, (50, 50), 2, 0.8, (0, 0, 0), 2, cv2.LINE_AA)
        clicked = False


# Function to exit window
def Exit():
    cv2.destroyAllWindows()
    root.destroy()


# exit button
Button(root, font='david 10 bold', text='Exit', width=8, height=2, padx=2, command=Exit, bg='#3CB371').place(x=250,
                                                                                                           y=120)
root.mainloop()
