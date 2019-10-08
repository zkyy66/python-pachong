import cv2

img_head = cv2.imread('head.jpg')
img_flag = cv2.imread('guoqi.png')

w_head, h_head = img_head.shape[:2]
w_flag, h_flag = img_flag.shape[:2]

scale = w_head / w_flag / 4

img_flag = cv2.resize(img_flag, (0, 0), fx=scale, fy=scale)

w_flag, h_flag = img_flag.shape[:2]

for c in range(0, 3):
    img_head[w_head - w_flag:, h_head - h_flag:, c] = img_flag[:, :, c]
    
cv2.imwrite('new_head.jpg', img_head)
