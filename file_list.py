import os,stat,subprocess
import colors

def format_size(num, suffix="B"):
    for unit in ("", "K", "M", "G", "T", "P", "E", "Z"):
        if abs(num) < 1000.0:
            return f"{num:3.1f}{unit}{suffix}"
        num /= 1000.0
    return f"{num:.1f}Y{suffix}"

file_flag_to_color = {
    "-": colors.fg.default,
    "d": colors.fg.blue,
    "c": colors.fg.yellow,
    "s": colors.fg.cyan,
    "l": colors.fg.cyan,
    "p": colors.fg.cyan,
    "b": colors.fg.magenta,
}

class File:
    def __init__(self,path:str):
        self.path=path
        self.update()
    
    def update(self):
        self.stat=os.stat(self.path)
    
    def get_permissions(self):
        return stat.filemode(self.stat.st_mode)
    
    def get_size(self):
        size = os.path.getsize(self.path)
        return format_size(size)

    def get_info(self):
        info = subprocess.check_output(["file",self.path])
        text = info.decode("utf-8")
        text = text.removeprefix(f"{self.path}: ")
        text = text.strip(" \t\n\r")
        return text
    
    def get_color(self):
        try:
            flag = self.get_permissions()[0]
            if self.stat.st_mode & stat.S_IEXEC:
                return colors.fg.green
            return file_flag_to_color[flag]
        except:
            print(self.path)
            print(self.get_permissions())

class FileList:
    def __init__(self,dir:str):
        self.dir=dir
        self.files=[]
        self.set_dir(dir)
        self.selected = 0
        self.height=15
        self.scroll=0
    
    def set_dir(self,dir:str):
        self.dir=dir
        self.files=os.listdir(dir)
        self.files.insert(0,"..")
        self.files.insert(0,".")
    
    def view(self) -> str:
        s = ""
        column_sizes={
            "perms": 0,
            "name": 0,
            "size": 0,
            "info": 0,
        }
        # get table sizes
        for fname in self.files:
            # get absolute file path
            path = os.path.join(self.dir,fname)
            file = File(path)

            # get file stuff
            perms=file.get_permissions()
            size=file.get_size()
            info=file.get_info()

            #update table sizes
            if len(perms) > column_sizes["perms"]:
                column_sizes["perms"] = len(perms)
            if len(size) > column_sizes["size"]:
                column_sizes["size"] = len(size)
            if len(fname) > column_sizes["name"]:
                column_sizes["name"] = len(fname)
            if len(info) > column_sizes["info"]:
                column_sizes["info"] = len(info)
        
        i = 0
        # display file table
        for fname in self.files:
            if i<self.scroll or i>=(self.scroll+self.height):
                continue
            # get absolute file path
            path = os.path.join(self.dir,fname)
            file = File(path)

            # get file stuff
            perms=file.get_permissions()
            size=file.get_size()
            info=file.get_info()

            if i == self.selected:
                s += colors.invert.on
            s += perms.ljust(column_sizes["perms"])
            s += "  "
            s += file.get_color()
            s += fname.ljust(column_sizes["name"])
            s += colors.fg.default
            s += "  "
            s += size.rjust(column_sizes["size"])
            s += "  "
            s += info.ljust(column_sizes["info"])

            if i == self.selected:
                s += colors.invert.off
            
            s += "\n"

            i += 1
        
        return s

            
