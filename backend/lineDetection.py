
import sys
import math
import cv2 as cv
from sklearn.cluster import KMeans
import numpy as np


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


def main(argv):

    default_file = 'IMG_20191110_052530.jpg'
    filename = argv[0] if len(argv) > 0 else default_file
    # Loads an image
    src = cv.imread(cv.samples.findFile(filename), cv.IMREAD_GRAYSCALE)
    src = cv.resize(src, (720, 480))
    # Check if image is loaded fine
    if src is None:
        print('Error opening image!')
        print(
            'Usage: hough_lines.py [image_name -- default ' + default_file + '] \n')
        return -1

    src = cv.adaptiveThreshold(src, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY, 11, 2)


    dst = cv.Canny(src, 50, 150, None, 3)
    cdst = cv.cvtColor(dst, cv.COLOR_GRAY2BGR)
    cdstP = np.copy(cdst)

    lines = cv.HoughLines(dst, 1, np.pi / 180, 150, None, 0, 0)
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
            # cv.line(cdst, pt1, pt2, (0, 0, 255), 3, cv.LINE_AA)
    circles = []
    for i in range(len(line)):
        for j in range(len(line)):
            if j > i:
                x, y = line_intersection(line[i], line[j])
                circles.append((x, y))
                cv.circle(cdst, (int(x), int(y)), 1, (0, 0, 255), 2)

    circles = list(filter(lambda x: x[0] < 1000 and x[1] < 1000, circles))

    # print(len(circles))
    point_dict = {}
    # for c in circles:
    #     print(c)

    taken = set()
    for _c in range(len(circles)):
        taken.add(_c)
        for _c2 in range(_c + 1, len(circles)):
            _dist = math.sqrt((circles[_c][0] - circles[_c2][0]) ** 2 + \
                (circles[_c][1] - circles[_c2][1]) ** 2)
            if _dist < 10 and _c2 not in taken:
                taken.add(_c2)

                if str(_c) not in point_dict:
                    point_dict[str(_c)] = []
                point_dict[str(_c)].append(_c2)

    more_than_one = 0
    listIntersection = []

    for k, v in point_dict.items():

        # print(k, len(v), v)
        if len(v) > 1:
            more_than_one += 1

            tmp_x = circles[int(k)][0]
            tmp_y = circles[int(k)][1]

            denom = 1
            for t in v:
                tmp_x += circles[t][0]
                tmp_y += circles[t][1]
                denom += 1

            tmp_x = tmp_x / denom
            tmp_y = tmp_y / denom

            listIntersection.append((tmp_x, tmp_y))

    listIntersection = list(sorted(listIntersection))
    listIntersection.pop(0)
    print(len(listIntersection))

    for li in listIntersection:
        print(li)

    for li in listIntersection:
        cv.circle(cdst, (int(li[0]), int(li[1])), 1, (0, 255, 0), 10)


    cv.imshow("Detected Lines (in red) - Standard Hough Line Transform", cdst)
    cv.waitKey()
    return 0


if __name__ == "__main__":
    main(sys.argv[1:])
