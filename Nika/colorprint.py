# http://ozzmaker.com/add-colour-to-text-in-python/

def gray(msg):
    print("\033[1;30m" + msg + "\033[0m")


def red(msg):
    print("\033[1;31m" + msg + "\033[0m")


def green(msg):
    print("\033[1;32m" + msg + "\033[0m")


def yellow(msg):
    print("\033[1;33m" + msg + "\033[0m")


def blue(msg):
    print("\033[1;34m" + msg + "\033[0m")


def magenta(msg):
    print("\033[1;35m" + msg + "\033[0m")


def cyan(msg):
    print("\033[1;36m" + msg + "\033[0m")


WHITE = "\033[1;30m{}\033[0m"
RED = "\033[1;31m{}\033[0m"
GREEN = "\033[1;32m{}\033[0m"
YELLOW = "\033[1;33m{}\033[0m"
BLUE = "\033[1;34m{}\033[0m"
MAGENTA = "\033[1;35m{}\033[0m"
CYAN = "\033[1;36m{}\033[0m"


def pr(*args, c=None, sep=' ', end='\n'):
    """
    w, r, g, y, b, m, c
    """

    msg = ""
    cnt = 0
    for i in args:
        cnt += 1
        if c is None:
            msg += str(i) + sep
        else:
            color = get_color_from_str(c, cnt)
            if color == 'w':
                msg += WHITE.format(i) + sep
            elif color == 'r':
                msg += RED.format(i) + sep
            elif color == 'g':
                msg += GREEN.format(i) + sep
            elif color == 'y':
                msg += YELLOW.format(i) + sep
            elif color == 'b':
                msg += BLUE.format(i) + sep
            elif color == 'm':
                msg += MAGENTA.format(i) + sep
            elif color == 'c':
                msg += CYAN.format(i) + sep
            else:
                msg += str(i) + sep
    msg += end
    print(msg, sep='', end='')


def get_color_from_str(p_str, pos):
    tmp_str = p_str.replace(" ", '').replace(",", '')
    if len(tmp_str) < pos:
        False
    else:
        return tmp_str[pos-1:pos]


# gray('12345')
# red('12345')
# green('12345')
# yellow('12345')
# blue('12345')
# magenta('12345')
# cyan('12345')
# pr("test", 1, True, "test2", "test3", "test4", "test5", "test6", c='r,w,b,g,y,m,c')
