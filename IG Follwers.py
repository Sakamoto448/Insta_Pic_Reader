import cv2
import pytesseract
import numpy as np
import pandas as pd
import os
import Header as h

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\\tesseract.exe'

"""
# Raw Follower Test Folder SC to Cropped SC on -> Cropped_Follwers Folder
def resize(counter,file_date):
    x = counter + 1
    img = cv2.imread("Raw Follower Pics/" + file_date + "(" + str(x) + ").png", cv2.IMREAD_UNCHANGED)
    Rimg = cv2.resize(img, (500, 500))
    cropped = Rimg[80:420, 100:350]
    #cv2.imshow("PIC", img)
    #cv2.imshow("resize", Rimg)
    #cv2.imshow("cropped", cropped)
    #cv2.waitKey(0)
    cv2.imwrite("Cropped_Follwers/" + str(counter) + ".png",cropped,params=None)

def img_section(img,names,database):
    Date = "10/21/2021"
    Recorder = "Aron"
    last = 0
    for x in range(1, 9):
        section = img[last: 42 * x, :]
        last = 42 * x
        cv2.imshow("sectioned", section)
        cv2.waitKey(0)


        hImg, wImg, _ = img.shape
        boxes = pytesseract.image_to_data(section)
        print(boxes)

        # create each identified word as a list
        for x, b in enumerate(boxes.splitlines()):
            if x != 0:
                b = b.split()
                #print(b)

                if len(b) == 12:
                    names.append(b[11])
                    database[len(names) - 1][0] = b[11]
                    database[len(names) - 1][2] = Date
                    database[len(names) - 1][3] = Recorder
                    #print(names)
                    break

names = []
database = np.empty([239, 4], dtype=object) # [Number of Followers, Attributes]
files = os.listdir("Raw Follower Pics")
file_date = "10_22_21 "

for i in range(len(files)): #start loop here
    resize(i,file_date) #cropped img to only names then saves it to Cropped_Follwers folder
    img = cv2.imread("Cropped_Follwers/" + str(i) + ".png", cv2.IMREAD_UNCHANGED)
    img_section(img, names, database)
# End Here
print(names)
"""

# HSV Mask to capture all Profile names only on img
def masked(img):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    lower = np.array([0, 0, 0])
    upper = np.array([179, 255, 145])
    mask = cv2.inRange(hsv, lower, upper)
    """
    # Horizontal Kernal and connect dialated text
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 3))
    dilate = cv2.dilate(mask, kernel, iterations=3)

    # Find contours and filter using aspect ratio
    # Remove non-text contours by filling in the contour
    cnts = cv2.findContours(dilate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    for c in cnts:
        x, y, w, h = cv2.boundingRect(c)
        ar = w / float(h)
        if ar < 5:
            cv2.drawContours(dilate, [c], -1, (0, 0, 0), -1)

    result = 255 - cv2.bitwise_and(dilate, mask)

    cv2.imshow("result", result)
    cv2.waitKey(0)
    return result
    """
    return mask

# Raw Follower Test Folder SC to Cropped SC on -> Cropped_Follwers Folder
def resize(counter,file_date):
    x = counter + 1
    img = cv2.imread("Raw Follower Pics/" + file_date + "(" + str(x) + ").png", cv2.IMREAD_UNCHANGED)
    #Rimg = cv2.resize(img, (500, 500))
    #cropped = Rimg[80:420, 100:350]
    cropped = img[350:1850, 220:850]

    #cv2.imshow("PIC", img)
    #cv2.imshow("resize", Rimg)
    #cv2.imshow("cropped", cropped)
    #cv2.waitKey(0)

    cv2.imwrite("Cropped_Followers/" + str(counter) + ".png", cropped, params=None)
    #cv2.imwrite("Cropped_Follwers/" + str(counter) + ".png",cropped,params=None)

def img_section(img,names,database, Recorded_date, Recorder):
    last = 0
    for y in range(1, 9):
        section = img[last: 180 * y, :]
        last = 180 * y
        mimg = masked(section)
        #cv2.imshow("sectioned HSV", mimg)
        #cv2.waitKey(0)

        hImg, wImg, _ = section.shape
        boxes = pytesseract.image_to_data(mimg)
        print(boxes)

        # create each identified word as a list
        for x, b in enumerate(boxes.splitlines()):
            if x != 0:
                b = b.split()
                #print(b)

                if len(b) == 12:
                    names.append(b[11])
                    database[len(names) - 1][0] = b[11]
                    database[len(names) - 1][2] = Recorded_date
                    database[len(names) - 1][3] = Recorder
                    #print(names)
                    break

names = []
database = np.empty([500, 4], dtype=object) # [Number of Followers, Attributes]
files = os.listdir("Raw Follower Pics")
file_date = "10_22_21 "
Recorded_date = "10/21/2021"
Recorder = "Aron"

for i in range(len(files)): #start loop here
    resize(i,file_date) #cropped img to only names then saves it to Cropped_Follwers folder
    img = cv2.imread("Cropped_Followers/" + str(i) + ".png", cv2.IMREAD_UNCHANGED)
    img_section(img, names, database, Recorded_date, Recorder)

df = pd.DataFrame(data=database,columns=["Follower", "Start Date", "Recorded Date", "Recorded By"])
df.to_csv("Instagram Followers " + file_date + ".csv", index=False)
