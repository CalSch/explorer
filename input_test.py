import select
import tty
import termios
import sys

init=termios.tcgetattr(sys.stdin)

def thing():
    tty.setraw(sys.stdin,termios.TCSANOW)
    i,o,e=select.select([sys.stdin],[],[],5)
    termios.tcsetattr(sys.stdin,termios.TCSANOW,init)
    # print("ok")
    if i:
        return sys.stdin.buffer.raw.read(1)

print(repr(thing()))
print(repr(thing()))
termios.tcsetattr(sys.stdin,termios.TCSANOW,init)
