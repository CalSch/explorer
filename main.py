import os,sys,argparse,termios,tty,time
import file_list

def getchar():
   #Returns a single character from standard input
   fd = sys.stdin.fileno()
   old_settings = termios.tcgetattr(fd)
   try:
      tty.setraw(sys.stdin.fileno())
      ch = sys.stdin.read(1)
   finally:
      termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
   return ch

parser = argparse.ArgumentParser(
    prog='Explorer',
    description='Explores folders',
    epilog='Schpaloingus!')

parser.add_argument('dir', nargs='?', default=os.getcwd())

args = parser.parse_args()

path = args.dir
files = file_list.FileList(path)

running = True

def update_files():
    files.set_dir(path)

def view():
    s = "\x1b[2J\x1b[H"
    s += f"{path}\n\n"
    s += files.view()

    return s

def handle_input(char):
    global running
    if char=="\x03": #Ctrl-C
        running=False
    elif char=="\x1b":
        getchar() #skip [
        char2=getchar()
        if char2=="A":
            files.selected-=1
        elif char2=="B":
            files.selected+=1
    elif char=="q":
        running=False
    else:
        print(char)
        time.sleep(1)

if __name__ == "__main__":
    while running:
        print(view())
        char = getchar()
        handle_input(char)
        # print(f"Cool '{char}'")