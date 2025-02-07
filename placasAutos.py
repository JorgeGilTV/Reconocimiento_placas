import cv2
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Users\Python Scripts\tesseract'
placa = []
image = cv2.imread('C:/Users/Python Scripts/Placas/carrito3.jpg')

cv2.imshow('',image)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
gray = cv2.blur(gray,(3,3))
canny = cv2.Canny(gray,150,200)

cv2.imshow('',canny)
canny = cv2.dilate(canny,None,iterations=1)
cv2.imshow('',canny)

#_,cnts,_ = cv2.findContours(canny,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
cnts,_ = cv2.findContours(canny,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
#cv2.drawContours(image,cnts,-1,(0,255,0),2)
for c in cnts:
  area = cv2.contourArea(c)
  x,y,w,h = cv2.boundingRect(c)
  epsilon = 0.09*cv2.arcLength(c,True)
  approx = cv2.approxPolyDP(c,epsilon,True)
  if len(approx)>1 and area>7000 and area<15000 and x>0 and y>0 and w>0 and h>0:
    print('area=',area)
    cv2.drawContours(image,[approx],0,(0,255,0),3)
    aspect_ratio = float(w)/h
    print(aspect_ratio)
    print(x,y,w,h)
    if aspect_ratio>2:
      placa = gray[y:y+h,x:x+w]
      text = pytesseract.image_to_string(placa,config='--psm 11')
      print('PLACA: ',text)
      cv2.imshow('PLACA',placa)
      cv2.moveWindow('PLACA',780,10)
      cv2.rectangle(image,(x,y),(x+w,y+h),(0,255,0),3)
      cv2.putText(image,text,(x-20,y-10),1,2.2,(0,255,0),3)
      
cv2.imshow('Image',image)
cv2.moveWindow('Image',45,10)
cv2.waitKey(0)  
