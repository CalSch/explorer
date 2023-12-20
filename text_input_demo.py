import text_input
import sys,termios,tty,select
import keys

#region input stuff

stdin_fd = sys.stdin.fileno()
# print(f"stdin: {stdin_fd}")
# quit(0)
try:
    old_term_settings = termios.tcgetattr(stdin_fd)
except:
    old_term_settings = None

def reset_term():
    if old_term_settings == None:
        return
    termios.tcsetattr(stdin_fd, termios.TCSADRAIN, old_term_settings)

def getchar(timeout:float=0.01):
    ch = ""
    #Returns a single character from standard input
    try:
        tty.setraw(stdin_fd,when=termios.TCSANOW)
        # ch = sys.stdin.read(1)
        i, o, e = select.select( [sys.stdin], [], [], timeout)
        # print(i)
        if i:
            ch = (sys.stdin.buffer.raw.read(1)).decode('utf-8')
            # print(repr(ch))
            # time.sleep(0.5)
        else:
            return None
    finally:
        reset_term()
    return ch

def getstr():
    s = ""
    ret = ""
    timeout=1 # the first getchar has a big timeout
    while ret != None:
        s += ret
        ret = getchar(timeout)
        timeout=0.01 # subsequent getchars have a small timeout
    return s

#endregion

ti = text_input.TextInput(
    width=30,
    height=1,
    prompt="Type stuff:",
    placeholder="cool placeholder",
    use_border=False
)

ti.onfocus()

@ti.set_onsubmit
def onsubmit(self:text_input.TextInput):
    global running
    running=False
    print("Submitted!")
    print(f"'{self.text}'")


running=True
while running:
    print("\x1b[2J\x1b[H")
    print("Press escape to exit")
    print(ti.view())
    print("\n\n")
    text=getstr()
    if text==keys.escape:
        running=False
    if text!="":
        ti.input(text)