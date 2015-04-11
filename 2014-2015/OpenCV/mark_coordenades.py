import cv2

img = cv2.imread('edi uveitis previa 11.png')
window_title = 'img'

def show_img():
    cv2.imshow(window_title, img)


def mouse_event(event, x, y, flags, params):
    global img
    if event == cv2.EVENT_MOUSEMOVE:
        print x, y
    if event == cv2.EVENT_LBUTTONDOWN:
        cv2.circle(img, (x, y), 1, (0, 0, 255), 3)
        cv2.putText(img, '(' + str(x) + ',' + str(y) + ')', (x, y), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (255, 0, 255), 1, cv2.CV_AA)
        show_img()

if __name__ == '__main__':
        show_img()
        cv2.setMouseCallback(window_title, mouse_event)
        cv2.waitKey(0) & 0xFF
