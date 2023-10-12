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

def clampSelection():
    files.selected=max(0,min(len(files.files)-1, files.selected)) # min: 0  max: # of files - 1

def updateScroll():
    # center the view around the selected item, but clamp it to not go out of bounds
    files.scroll = int(max(
        0,
        min(
            len(files.files)-files.height,
            files.selected-files.height/2
        )
    ))

def view():
    s = "\x1b[2J\x1b[H"
    s += f"==== {path} ====\n"
    s += f"{len(files.get_files())} files, "
    s += f"{len(files.get_folders())} folders, "
    s += f"{len(files.get_links())} links"
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
            files.selected-=1
        elif char2=="B":
            files.selected+=1
    elif char=="\r":
        file = files.files[files.selected]
        if os.path.isdir(os.path.realpath(file.path)): # use os.path.realpath to follow symlinks
            path = os.path.abspath( os.path.join( path, file.get_name() ) )
            update_files()
            if file.get_name() == "..": # if going up, then select the previous folder
                index = os.listdir(path).index( os.path.basename(os.path.dirname(file.path)) )
                files.selected = index
    elif char=="q":
        running=False
    else:
        # print(char)
        # time.sleep(1)
        pass

if __name__ == "__main__":
    print(view())
    while running:
        char = getchar()
        handle_input(char)
        clampSelection()
        updateScroll()

        # print("Loading...")
        print(view())
        # print(f"Cool '{char}'")