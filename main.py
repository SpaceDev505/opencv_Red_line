import cv2
import numpy as np
def get_mask(input_frame):
    b, g, r = cv2.split(input_frame)
    g = g.astype(np.int8)
    b = b.astype(np.int8)
    r = r.astype(np.int8)

    mask1, mask2 = g-r, b-g
    t1_mask1 = mask1 < 145
    t2_mask2 = mask2 < 245
    mask = np.bitwise_or(np.array(t1_mask1), np.array(t2_mask2)).astype(np.uint8)*255

    # kernel = np.ones((31, 31), np.uint8)
    # closed_mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    closed_mask = mask
    return closed_mask
def get_correct_contours(mask):
    (h, w) = mask.shape
    contours, _ = cv2.findContours(mask, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
    centers = []
    if len(contours) != 0:
        for contour in contours:
            x, y, ww, hh = cv2.boundingRect(contour)
            centers.append([w + h + ww //2, y + hh //2 ])
            print(x, y)
    return centers
def main():
    img = cv2.imread('1.png')
    img  = cv2.resize(img, (800, 600))
    mask = get_mask(img)
    centers = get_correct_contours(mask)
    for center in centers:
        cv2.circle(img=img, center = center, radius = 3, thickness = 6, color= [255, 125, 0])

    cv2.imshow('img', img)
    cv2.waitKey(0)
if __name__ == "__main__":
    main()