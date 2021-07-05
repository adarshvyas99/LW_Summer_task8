import cv2
import numpy as np
import imutils
import easyocr
import requests
import xmltodict
import json

def model(image_location):
    img = cv2.imread(image_location)
    print(img.shape)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    bfilter = cv2.bilateralFilter(gray, 11, 17, 17)     #Noise reduction
    edged = cv2.Canny(bfilter, 30, 200) #Edge detection
    keypoints = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours = imutils.grab_contours(keypoints)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)[:10]
    location = None
    for contour in contours:
        approx = cv2.approxPolyDP(contour, 10, True)
        if len(approx) == 4:
         location = approx
         break
    mask = np.zeros(gray.shape, np.uint8)
    print(mask)
    print(type(mask))
    #new_image = cv2.drawContours(mask, [location], 0,255, -1)
    #new_image = cv2.bitwise_and(img, img, mask=mask)
    (x,y) = np.where(mask==[[255]])
    (x1, y1) = (np.min(x), np.min(y))
    (x2, y2) = (np.max(x), np.max(y))
    cropped_image = gray[x1:x2+1, y1:y2+1]
    reader = easyocr.Reader(['en'])
    result = reader.readtext(cropped_image)
    global text
    text = result[0][-2]
    return text
    #font = cv2.FONT_HERSHEY_SIMPLEX
    #res = cv2.putText(img, text=text, org=(approx[0][0][0], approx[1][0][1]+60), fontFace=font, fontScale=1, color=(0,255,0), thickness=2, lineType=cv2.LINE_AA)
    #res = cv2.rectangle(img, tuple(approx[0][0]), tuple(approx[2][0]), (0,255,0),3)
    
    
image_location="car11.jpeg"
number=model(image_location)



def m_get_vehicle_info(text):
    r = requests.get("http://www.regcheck.org.uk/api/reg.asmx/CheckIndia?RegistrationNumber={0}&username=Adarsh".format(str(text)))
    data = xmltodict.parse(r.content)
    jdata = json.dumps(data)
    df = json.loads(jdata)
    df1 = json.loads(df['Vehicle']['vehicleJson'])
    return df1



x=m_get_vehicle_info(number)


print(number)
print(x)

