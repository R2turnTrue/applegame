import pyautogui
import time

#pyautogui.PAUSE = 0

# w=17, h=10 board

def autosolve(board, BOARD_OFFSET_START):
    def solve(x_start, y_start, width, height):
        x_off = BOARD_OFFSET_START[0] + 32.7 * x_start
        y_off = BOARD_OFFSET_START[1] + 32.3 * y_start
        pyautogui.moveTo(x_off, y_off)
        pyautogui.mouseDown(button='left')
        pyautogui.moveTo(x_off + 32.7 * width, y_off + 32.3 * height, duration=0.25)
        time.sleep(0.05)
        pyautogui.moveTo(x_off + 32.7 * width + 5, y_off + 32.3 * height + 5, duration=0.1)
        time.sleep(0.1)
        pyautogui.mouseUp(button='left')

    print('solving')

    total_solutions = 0

    while True:
        solve_count = 0

        for y in range(10):
            for x in range(17):
                #print('===newcell')
                #print('{}/{}'.format(x, y))
                add = 0
                height = 1
                width = 1
                while True:
                    if x + width >= 17 + 1:
                        break
                    for xx in range(x, x + width):
                        num = board[y][xx]
                        add += num
                    
                    if add > 10:
                        break

                    add = 0

                    while True:
                        nonum_detected = False

                        #print('///it')
                        if x + width >= 17 + 1:
                            #print('BREAK! (w)')
                            break
                        if y + height >= 10 + 1:
                            #print('BREAK! (h)')
                            break
                        
                        for xx in range(x, x + width):
                            for yy in range(y, y + height):
                                num = board[yy][xx]

                                if num < 0:
                                    nonum_detected = True
                                    break

                                add += num

                                #print('{}/{}/{}'.format(x, yy, add))
                            
                            if nonum_detected:
                                break
                        
                        if add >= 10:
                            break

                        height += 1
                        add = 0
                    
                    if add > 10:
                        pass
                    elif add == 10: # add == 10

                        for xx in range(x, x + width):
                            for yy in range(y, y + height):
                                board[yy][xx] = 0

                        print('min: {} {} / max: {} {}'.format(x + 1, y + 1, x + 1 + width - 1, y + 1 + height - 1))

                        solve(x, y, width, height)

                        solve_count += 1
                        total_solutions += 1
                        break
                    
                    add = 0
                    width += 1
                    height = 1
        
        if solve_count == 0:
            for y in range(10):
                print(' '.join(map(str, board[y])))
            print('Solve end with total solutions: {}'.format(total_solutions))
            break

if __name__ == '__main__':
    # board[y][x]
    board = []

    for y in range(10):
        board.append(list(map(int, input().split())))
    
    autosolve(board, (2563, 167))