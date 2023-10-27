#!/usr/bin/env python3
import os,sys,argparse,termios,tty,time,signal
import file_list

stdin_fd = sys.stdin.fileno()
print(f"stdin: {stdin_fd}")
# quit(0)
try:
    old_term_settings = termios.tcgetattr(stdin_fd)
except:
    old_term_settings = None

def reset_term():
    if old_term_settings == None:
        return
    termios.tcsetattr(stdin_fd, termios.TCSADRAIN, old_term_settings)

def getchar():
    #Returns a single character from standard input
    try:
        tty.setraw(stdin_fd)
        ch = sys.stdin.read(1)
    finally:
        reset_term()
    return ch

parser = argparse.ArgumentParser(
    prog='Explorer',
    description='Explores folders',
    epilog='Schpaloingus!')

parser.add_argument('dir', nargs='?', default=os.getcwd())
parser.add_argument('-o', '--once', action='store_true')
parser.add_argument('-b', '--batch', action='store_true')
parser.add_argument('-n', '--iterations', type=int, default=-1)

args = parser.parse_args()

path = args.dir
files = file_list.FileList(path)

running = True

if args.once:
    running = False

def update_files():
    files.set_dir(path)

def update():
    try:
        term_size = os.get_terminal_size()
        files.height = term_size.lines - 15
        files.width = term_size.columns - 1
    except OSError:
        # term_size = os.terminal_size([],{})
        pass
    files.update_table()

def view():
    s = "\x1b[2J\x1b[H\x1b[0m"
    s += f"==== {path} ====\n"
    s += f"{len(files.get_files())} files, "
    s += f"{len(files.get_folders())} folders, "
    s += f"{len(files.get_links())} links"
    s += "\n"
    s += f"{files.table.width}x{files.table.height}"
    s += "\n\n"
    
    s += files.view()

    # s+=f"\n\n{files.selected} {files.scroll} {files.height}"

    return s

def handle_input(char):
    global running,path
    f=open('char','a')
    f.write(char)
    f.close()
    if char=="\x03": #Ctrl-C
        running=False
    elif char=="\x1b":
        getchar() #skip [
        char2=getchar()
        if char2=="A":
            files.table.selected-=1
        elif char2=="B":
            files.table.selected+=1
    elif char=="\r":
        file = files.files[files.table.selected]
        if os.path.isdir(os.path.realpath(file.path)): # use os.path.realpath to follow symlinks
            path = os.path.abspath( os.path.join( path, file.get_name() ) )
            update_files()
            if file.get_name() == "..": # if going up, then select the previous folder
                new_files=files.table.get_field("name")
                # print(new_files)
                index = new_files.index( os.path.basename(os.path.dirname(file.path)) )
                files.table.selected = index

    elif char=="q":
        running=False
    else:
        # print(char)
        # time.sleep(1)
        pass

if __name__ == "__main__":
    iteration = 0
    def sigwinch_handle(signum,frame):
        reset_term() # reset terminal to not mess up printing
        update()
        print(view())
        tty.setraw(stdin_fd) # set tty back to raw mode for input
    signal.signal(signal.SIGWINCH,sigwinch_handle)
    update()
    print(view())
    while running:
        if args.iterations > 0 and iteration >= args.iterations:
            running=False
        if not args.batch:
            char = getchar()
            handle_input(char)
        update()

        # print("Loading...")
        print(view())
        iteration += 1