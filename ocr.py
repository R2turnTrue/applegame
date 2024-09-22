import pyautogui
import cv2
import pytesseract
import re
import numpy as np
import solve
from tqdm import tqdm

off_x = 0
off_y = 0

board = []

fail = 0

print('Set your cursor position to topleft of the board and press Enter!')
input()

BOARD_OFFSET_START = pyautogui.position()
BOARD_OFFSET_START = (BOARD_OFFSET_START.x, BOARD_OFFSET_START.y)

for y in tqdm(range(10), desc="ocr"):
    row = []
    fail_row = 0
    for x in tqdm(range(17), desc="        row"):
        #img = pyautogui.screenshot(region=(2563, 167, 3122 - 2563, 494 - 167), allScreens=True)
        img = pyautogui.screenshot(region=(int(BOARD_OFFSET_START[0] + off_x), int(BOARD_OFFSET_START[1] + off_y), 32, 32), allScreens=True)
        img = cv2.cvtColor(np.asarray(img), cv2.COLOR_RGB2BGR)
        img = cv2.resize(img, dsize=(0, 0), fx=6.0, fy=6.0, interpolation=cv2.INTER_AREA)

        #h, w, c = img.shape
        #print('{}:{}'.format(w, h))

        #cv2.imshow('', img)
        #cv2.waitKey(0)
        #img = cv2.cvtColor(np.asarray(img), cv2.COLOR_RGB2GRAY)
        #img = np.invert(img)

        #white = np.array([23, 150, 226])
        #white2 = np.array([30, 153, 250])

        #mask = cv2.inRange(img, white, white2)
        #res = cv2.bitwise_and(img, img, mask=mask)

        pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract'

        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        text = pytesseract.image_to_string(img, config='--psm 10 --oem 1')

        numbers = [int(s) for s in re.findall(r'\b\d+\b', text)]

        if len(numbers) <= 0:
            #print('FAIL!! {}:{}'.format(x, y))
            fail_row += 1
            cv2.imwrite('temp/fail_{}_{}.png'.format(x, y), img)
            row.append(-1)
        else:
            row.append(numbers[0])
        
        off_x += 32 + 1
    off_y += 32 + 1
    off_x = 0

    print('\nrow finished with {}/{} ({} fails)\n'.format(17 - fail_row, 17, fail_row))

    fail += fail_row

    board.append(row)

print('\ocr finished with {}/{} ({} fails)\n'.format(10 * 17 - fail, 10 * 17, fail))

solve.autosolve(board, BOARD_OFFSET_START)