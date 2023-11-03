import select
import tty
import termios
import sys,time

init=termios.tcgetattr(sys.stdin)

def reset_term():
    termios.tcsetattr(0, termios.TCSADRAIN, init)

def getchar():
    ch = ""
    #Returns a single character from standard input
    try:
        tty.setraw(0,when=termios.TCSANOW)
        # ch = sys.stdin.read(1)
        i, o, e = select.select( [sys.stdin], [], [], 0.1)
        # print(i)
        if i:
            ch = (sys.stdin.buffer.raw.read(1)).decode('utf-8')
            # print(repr(ch))
            # time.sleep(0.5)
        else:
            reset_term()
            return None
    finally:
        reset_term()
    return ch

def getstr():
    s = ""
    ret = ""
    while ret != None:
        s += ret
        ret = getchar()
    return s

print("press b to break")

while True:
    s=getstr()
    if s=="":
        continue
    print("horray!",repr(s))
    # time.sleep(1)
    if s=="b":
        break
