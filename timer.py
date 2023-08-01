import curses
import time
import logging

logging.basicConfig(filename='clock.log', encoding='utf-8', level=logging.DEBUG)


def timer(win, second:int):
    win.clear()
    end_time = second + time.time()

    while True:
        second = int(end_time - time.time())
        logging.debug('%f', second)
        win.clear
        win.addstr(0, 0, f"{second//3600}:{(second//60)%60}:{second % 60}")
        win.refresh()
        second -= 1
        time.sleep(1)
        if second <= 0:
            break


def get_time(stdscr):
    curses.curs_set(1)
    stdscr.clear()
    ch_list = []
    stdscr.addstr(0, 0, "请输入计时器时间:")
    while True:
        x = stdscr.getch()
        logging.debug("%d", x)
        if x > 0x1f and x < 0x7f:
            ch_list.append(chr(x))
            stdscr.addch(x)
        if x == 263:  # 退格键
            y, x = stdscr.getyx()
            if x > 0 and y > 0:
                stdscr.move(y, x-1)
                stdscr.delch()
        if x == 10:  # 27 = ESC = 0x1b
            break
    curses.curs_set(0)
    return "".join(ch_list)


def get_second(t: str):
    '''
    不在意有没有0
    :param t: str 时间字符串
    '''
    # string = string.spli
    t = t.split(":")
    if len(t) == 1:
        return int(t[0])
    if len(t) == 2:
        return int(t[0])*60
    if len(t) == 3:
        return int(t[0])*3600 + int(t[1])*60 + int(t[2])
    raise "请输入数字"


def quit_timer(stdscr, height, width):

    stdscr.clear()
    win = curses.newwin(height//2+1, width//2+10, height //
                        2-1, width//2-5)
    win.addstr(0, 0, "时间到了")
    win.addstr(3, 0, "按空格退出")
    win.refresh()
    while True:
        if win.getch() == 32:
            break


def main(stdscr):
    # 初始化
    curses.curs_set(0)
    stdscr.clear()
    stdscr.nodelay(1)

    # 创建一个窗口
    height, width = stdscr.getmaxyx()  # 获取屏幕的高度和宽度
    
    win = curses.newwin(height//2, width//2 + 5, height //
                        2, width//2 - 5)  # 创建了一个新窗口,居中
    t = get_time(win)
    logging.info("time:%s", t)
    t = get_second(t)
    timer(win, t)

    # 清理资源
    curses.endwin()


# 运行主函数
curses.wrapper(main)
