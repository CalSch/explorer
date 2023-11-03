#!/usr/bin/env python3
import os,sys,argparse,termios,tty,time,signal
import file_list
import text_pager
import string_util as su
import colors
import view_layout
import select

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

def getchar():
    ch = ""
    #Returns a single character from standard input
    try:
        tty.setraw(stdin_fd,when=termios.TCSANOW)
        # ch = sys.stdin.read(1)
        i, o, e = select.select( [sys.stdin], [], [], 0.01)
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
    while ret != None:
        s += ret
        ret = getchar()
    return s

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
pager = text_pager.TextPager()
pager.show = False
show_pager = False
pager_focused = False

layout = view_layout.ViewLayout([
    [ files, pager ]
])

running = True

if args.once:
    running = False

def update_files():
    files.set_dir(path)

def update():
    try:
        term_size = os.get_terminal_size()
        files.height = term_size.lines - 15
        if show_pager:
            files.width = int(term_size.columns/2 - 1)
        else:
            files.width = term_size.columns - 1
        pager.width = int(term_size.columns/2)
    except OSError:
        # term_size = os.terminal_size([],{})
        pass
    pager.border_style = su.normal_border if pager_focused else su.dashed_border
    pager.border_style.color = colors.fg.default if pager_focused else colors.dim.on
    pager.update()
    files.update_table()

def view():
    s = "\x1b[2J\x1b[H\x1b[0m"
    if iteration%2==0:
        s += "#"
    else:
        s += " "
    s += f"==== {path} ====\n"
    s += f"{len(files.get_files())} files, "
    s += f"{len(files.get_folders())} folders, "
    s += f"{len(files.get_links())} links"
    s += "\n"
    s += f"{files.table.width}x{files.table.height}"
    s += "\n\n"
    
    # if show_pager:
    #     # s += pager.view()
    #     s += su.join_horizontal(files.view(),pager.view(),padding_char="|")
    # else:
    #     s += files.view()
    s += layout.view()

    # s+=f"\n\n{files.selected} {files.scroll} {files.height}"

    return s

def handle_input(char):
    global running,path,show_pager,pager_focused
    f=open('char','a')
    f.write(str(char))
    f.close()
    if char=="\x03": #Ctrl-C
        running=False
    elif char=="\x1b[A":
        if pager_focused:
            pager.scroll_y -= 1
        else:
            files.table.selected-=1
    elif char=="\x1b[B":
        if pager_focused:
            pager.scroll_y += 1
        else:
            files.table.selected+=1
    elif char=="\x1b[C":
        layout.move_focus(-1,0)
    elif char=="\r":
        file = files.files[files.table.selected]
        show_pager=False
        if os.path.isdir(os.path.realpath(file.path)): # use os.path.realpath to follow symlinks
            path = os.path.abspath( os.path.join( path, file.get_name() ) )
            update_files()
            if file.get_name() == "..": # if going up, then select the previous folder
                new_files=files.table.get_field("name")
                # print(new_files)
                index = new_files.index( os.path.basename(os.path.dirname(file.path)) )
                files.table.selected = index
        elif os.path.isfile(os.path.realpath(file.path)):
            pager.show=True
            # pager_focused=True
            pager.load_from_file(file)

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
        tty.setraw(stdin_fd,when=termios.TCSANOW) # set tty back to raw mode for input
    signal.signal(signal.SIGWINCH,sigwinch_handle)
    update()
    print(view())
    while running:
        if args.iterations > 0 and iteration >= args.iterations:
            running=False
        if not args.batch:
            text = getstr()
            handle_input(text)
        update()

        # print("Loading...")
        print(view())
        iteration += 1