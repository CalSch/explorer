import os,stat,subprocess
import colors

def format_size(num, suffix="B"):
    for unit in ("", "K", "M", "G", "T", "P", "E", "Z"):
        if abs(num) < 1000.0:
            return f"{num:3.1f}{unit}{suffix}"
        num /= 1000.0
    return f"{num:.1f}Y{suffix}"

file_flag_to_color = {
    # "-": colors.fg.default,
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
        self.broken=False
        self.update()
    
    def update(self):
        if not os.path.exists(self.path):
            self.broken=True
        self.info=self.get_info()
        self.stat=os.lstat(self.path) # use lstat to follow symlinks
    
    def get_permissions(self) -> str:
        if self.broken:
            return ""
        return stat.filemode(self.stat.st_mode)
    
    def get_size(self) -> str:
        if self.broken:
            return ""
        size = os.path.getsize(self.path)
        return format_size(size)

    def get_info(self) -> str:
        if self.broken:
            return ""
        info = subprocess.check_output(["file","-e","elf","-b",self.path])
        text = info.decode("utf-8")
        text = text.strip(" \t\n\r")
        return text
    
    def get_color(self) -> str:
        if self.broken:
            return colors.fg.red
        try:
            flag = self.get_permissions()[0]

            if flag in file_flag_to_color.keys():
                return file_flag_to_color[flag]
            
            if self.stat.st_mode & stat.S_IEXEC:
                return colors.fg.green
            
            return colors.fg.default
        except:
            print(self.path)
            print(self.get_permissions())
    
    def get_name(self) -> str:
        return os.path.basename(self.path)

class FileList:
    def __init__(self,dir:str):
        self.dir=dir
        self.files: list[File]=[]
        self.set_dir(dir)
        self.selected = 0
        self.height=30
        self.scroll=0
    
    def set_dir(self,dir:str):
        self.dir=dir
        file_names=os.listdir(dir)
        file_names.sort(key=lambda x: x.lower())
        file_names.insert(0,"..")
        file_names.insert(0,".")

        self.files=[]

        for fname in file_names:
            self.files.append(File(os.path.join(self.dir, fname)))
    
    def get_files(self):
        files=[]
        for file in self.files:
            if os.path.isfile(file.path):
                files.append(file)
        return files
    def get_folders(self):
        folders=[]
        for file in self.files:
            if os.path.isdir(file.path):
                folders.append(file)
        return folders
    def get_links(self):
        links=[]
        for file in self.files:
            if os.path.islink(file.path):
                links.append(file)
        return links
    
    def view(self) -> str:
        s:str = ""
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
                i += 1
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

            # s = s.rstrip()

            s += "\n"

            if i == self.selected:
                s += colors.invert.off

            i += 1
        
        return s

            
