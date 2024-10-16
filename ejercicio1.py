import cv2
import numpy as np

img = cv2.imread('moneditas.JPEG')

gris = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
pimg = cv2.GaussianBlur(gris, (3, 3), 0)

circ = cv2.HoughCircles(
    pimg,
    cv2.HOUGH_GRADIENT,
    1,
    150,
    param1=145,
    param2=65,
    minRadius=50,
    maxRadius=120
)

monedas = {
    .01: 1626,
    .02: 1875,
    .05: 2125,
    .1: 1975,
    .2: 2225,
    .5: 2425,
    1: 2325,
    2: 2575
}

def distance(circle, x, y):
    return np.sqrt((x - circle[0]) ** 2 + (y - circle[1]) ** 2)

def click_event(event, x, y, a, b):
    if event == cv2.EVENT_LBUTTONDOWN:
        x *= 2.5
        y *= 2.5
        for c in circ[0]:
            if distance(c, x, y) <= c[2]:
                count_money(c[2])
                return

def count_money(euro1radius):
    correlation = monedas[1] / euro1radius
    result = {
        .01: 0,
        .02: 0,
        .05: 0,
        .1: 0,
        .2: 0,
        .5: 0,
        1: 0,
        2: 0
    }
    for c in circ[0]:
        radius = c[2]
        moneda = min(monedas, key=lambda x:abs(monedas[x] - (correlation * radius)))
        result[moneda] += 1

    count_result(result)

def count_result(result):
    total_money = 0
    for k, v in result.items():
        if v > 0:
            print(f"Hay {v} monedas de {k}€")
            total_money += v * k * 100
    print(f"Hay {total_money / 100}€")

def draw_and_show(nimg):
    for det in circ[0]:
        x_coor, y_coor, det_radio = det
        cv2.circle(nimg, (int(x_coor), int(y_coor)),
                   int(det_radio), (0, 255, 0), 2)
    cv2.imshow('Monedas', cv2.resize(nimg, (0, 0), fx=0.4, fy=0.4))
    cv2.setMouseCallback('Monedas', click_event)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


draw_and_show(img)

