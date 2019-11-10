import cv2 as cv
import numpy as np
import math


def line_intersection(line1, line2):
    xdiff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
    ydiff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1])

    def det(a, b):
        return a[0] * b[1] - a[1] * b[0]

    div = det(xdiff, ydiff)
    if div == 0:
        return 0, 0

    d = (det(*line1), det(*line2))
    x = det(d, xdiff) / div
    y = det(d, ydiff) / div
    return x, y


def houghlineShow(lines, img):
    line = []
    if lines is not None:
        for i in range(0, len(lines)):
            rho = lines[i][0][0]
            theta = lines[i][0][1]
            a = math.cos(theta)
            b = math.sin(theta)
            x0 = a * rho
            y0 = b * rho
            pt1 = (int(x0 + 1000 * (-b)), int(y0 + 1000 * (a)))
            pt2 = (int(x0 - 1000 * (-b)), int(y0 - 1000 * (a)))
            line.append((pt1, pt2))
            cv.line(img, pt1, pt2, (0, 0, 255), 3, cv.LINE_AA)
    return line


snapshot = cv.imread("snapshot.jpg")
cdst = cv.cvtColor(snapshot, cv.COLOR_BGR2GRAY)
dst = cv.Canny(cdst, 50, 200, None, 3)
cdst = cv.cvtColor(dst, cv.COLOR_GRAY2BGR)
cv.imwrite("EdgeDetected.jpg", cdst)
lines = cv.HoughLines(dst, 1, np.pi / 180, 150, None, 0, 0)
line1 = houghlineShow(lines, cdst)
circles = []
# for i in range(len(line)):
#     for j in range(len(line)):
#         if j > i:
#             x, y = line_intersection(line[i], line[j])
#             circles.append((x, y))
# cv.circle(cdst, (int(x), int(y)), 1, (0, 0, 255), 2)
snapshot2 = cv.imread("snapshot2.jpg")
cdst2 = cv.cvtColor(snapshot2, cv.COLOR_BGR2GRAY)
dst2 = cv.Canny(cdst2, 50, 200, None, 3)
cdst2 = cv.cvtColor(dst2, cv.COLOR_GRAY2BGR)
lines2 = cv.HoughLines(dst, 1, np.pi / 180, 150, None, 0, 0)
line2 = houghlineShow(lines2, cdst2)
xor = cv.bitwise_xor(cdst, cdst2)
# cv.imwrite("HoughTransform-2.jpg", cdst2)
font = cv.FONT_HERSHEY_SIMPLEX
print(line1.sort())
cv.imshow("Snapshot", cdst2)
cv.waitKey()
