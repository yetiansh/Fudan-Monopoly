import cv2 as cv
im = cv.imread('handout/materials/map.jpg')
cv.imwrite('map.png', im)
