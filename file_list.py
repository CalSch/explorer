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
        self.info=""
        self.update()
    
    def update(self):
        self.info=self.get_info()
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
    
    def get_name(self):
        return os.path.basename(self.path)

class FileList:
    def __init__(self,dir:str):
        self.dir=dir
        self.files: list[File]=[]
        self.set_dir(dir)
        self.selected = 0
        self.height=15
        self.scroll=0
    
    def set_dir(self,dir:str):
        self.dir=dir
        file_names=os.listdir(dir)
        file_names.insert(0,"..")
        file_names.insert(0,".")

        self.files=[]

        for fname in file_names:
            self.files.append(File(os.path.join(self.dir, fname)))
    
    def view(self) -> str:
        s = ""
        column_sizes={
            "perms": 0,
            "name": 0,
            "size": 0,
            "info": 0,
        }
        # get table sizes
        for file in self.files:
            # get file stuff
            perms=file.get_permissions()
            size=file.get_size()
            info=file.info

            #update table sizes
            if len(perms) > column_sizes["perms"]:
                column_sizes["perms"] = len(perms)
            if len(size) > column_sizes["size"]:
                column_sizes["size"] = len(size)
            if len(file.get_name()) > column_sizes["name"]:
                column_sizes["name"] = len(file.get_name())
            if len(info) > column_sizes["info"]:
                column_sizes["info"] = len(info)
        
        i = 0
        # display file table
        for file in self.files:
            if i<self.scroll or i>=(self.scroll+self.height):
                continue

            # get file stuff
            perms=file.get_permissions()
            size=file.get_size()
            info=file.info

            if i == self.selected:
                s += colors.invert.on
            s += perms.ljust(column_sizes["perms"])
            s += "  "
            s += file.get_color()
            s += file.get_name().ljust(column_sizes["name"])
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

            
