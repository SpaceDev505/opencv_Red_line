import os, cv2
import numpy as np

def get_mask(thermal_frame):
    b, g, r = cv2.split(thermal_frame)


    g = g.astype(np.int8)
    b = b.astype(np.int8)
    r = r.astype(np.int8)

    mask1, mask2 = np.abs(r - g - 110), np.abs(b - g - 5)
    t1_mask1 = mask1 < 25
    t2_mask1 = mask2 < 15
    mask = np.bitwise_and(np.array(t1_mask1), np.array(t2_mask1)).astype(np.uint8) * 255
    cv2.imshow("t1_mask1", t1_mask1.astype(np.uint8) * 255)
    cv2.imshow("t2_mask1", t2_mask1.astype(np.uint8) * 255)
    cv2.waitKey(0)
    # kernel = np.ones((31, 31), np.uint8)
    # closed_mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    closed_mask = mask
    print(mask)
    return closed_mask

def get_correct_contours(mask):
    (h, w) = mask.shape
    # cv2.imshow('mask', mask)
    contours, _ = cv2.findContours(mask, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
    centers = []
    if len(contours) != 0:
        for contour in contours:
            x, y, ww, hh = cv2.boundingRect(contour)
            # if x < w // 7 or x > w // 7 * 6: continue
            # if y < h // 7 or y > h // 7 * 6: continue
            
            centers.append([w + x + ww // 2, y + hh // 2])
    print(centers)
    return centers

def _main():
    frame = cv2.imread('1.png')
    frame = cv2.resize(frame, (800, 600))
    mask = get_mask(frame)
    cv2.imshow('framwere', mask)
    centers = get_correct_contours(mask)
    
    for center in centers:
        cv2.circle(img=frame, center=center, radius=3, thickness=6, color=[0, 255, 0])

    # if i > 2000:
    # cv2.imshow('mask', mask)
    # cv2.imshow('b_r', g)
    # cv2.imshow('colored_frame', colored_frame)
    cv2.imshow('frame', frame)
    cv2.waitKey(0)


if __name__ == "__main__":
    _main()