import cv2
import pytesseract
import numpy as np
import pandas as pd
import os

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\\tesseract.exe'

# HSV Mask to capture all Profile names only on img
def masked(img):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    lower = np.array([0, 0, 0])
    upper = np.array([179, 255, 145])
    mask = cv2.inRange(hsv, lower, upper)
    return mask

# Raw Follower Test Folder SC to Cropped SC on -> Cropped_Follwers Folder
def resize(counter,file_name):
    x = counter + 1
    img = cv2.imread("Raw Pics/" + file_name + "(" + str(x) + ").png", cv2.IMREAD_UNCHANGED)
    #Rimg = cv2.resize(img, (500, 500))
    #cropped = Rimg[80:420, 100:350]
    cropped = img[200:1900, 220:755]

    #cv2.imshow("PIC", img)
    #cv2.imshow("resize", Rimg)
    #cv2.imshow("cropped", cropped)
    #cv2.waitKey(0)

    cv2.imwrite("Cropped_Pics/" + str(counter) + ".png", cropped, params=None)

def img_section(img,names,database, Recorded_date, Recorder):
    last = 0
    for y in range(1, 10):
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
                    if b[11] not in database:
                        names.append(b[11])
                        database[len(names) - 1][4] = b[11]
                        database[len(names) - 1][6] = Recorded_date
                        database[len(names) - 1][7] = Recorder
                        #print(names)
                        break

names = []
database = np.empty([500, 8], dtype=object) # [Number of Followers, Attributes]
files = os.listdir("Raw Pics")
#Only Changes Needed are these Below
# ------------------------------------------------
Post = "Test"
Type = "Video"
Detail = "Lilian Intro"
file_name = "Lilian " # Make sure there is a extra space in the end for this one
Recorded_date = "11/10/2021"
Recorder = "Aron"
# -----------------------------------------------
database[0][0] = Post
database[0][1] = Type
database[0][2] = Detail
database[0][3] = Detail

for i in range(len(files)): #start loop here
    resize(i,file_name) #cropped img to only names then saves it to Cropped_Follwers folder
    img = cv2.imread("Cropped_Pics/" + str(i) + ".png", cv2.IMREAD_UNCHANGED)
    img_section(img, names, database, Recorded_date, Recorder)

df = pd.DataFrame(data=database,columns=["Post", "Type", "Title", "Detail", "Liker", "Liked Date", "Recorded Date", "Recorded By"])
df.to_csv("Instagram Post " + file_name + "Likes.csv", index=False)
