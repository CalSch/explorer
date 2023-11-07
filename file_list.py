import os,stat,subprocess,string_util
import colors
import table
import component
import keys
import time

def format_size(num, suffix="B"):
    for unit in (" ", "K", "M", "G", "T", "P", "E", "Z"):
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

file_info_cache: dict[str,str]={}
file_mime_cache: dict[str,str]={}

class File:
    def __init__(self,path:str):
        self.path=path
        self.info=""
        self.mime=""
        self.broken=False
        self.update()
    
    def update(self):
        if not os.path.exists(self.path):
            self.broken=True
        self.info=self.get_info()
        self.mime=self.get_mime()
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
        if os.path.isdir(self.path):
            return "directory"
        
        if self.path in file_info_cache.keys():
            return file_info_cache[self.path]
        
        info = subprocess.check_output(["file","-e","elf","-b",self.path])
        text = info.decode("utf-8")
        text = text.strip("\n")

        file_info_cache[self.path]=text
        return text

    def get_mime(self) -> str:
        if self.broken:
            return ""
        
        if self.path in file_mime_cache.keys():
            return file_mime_cache[self.path]
        
        info = subprocess.check_output(["file","-i","-b",self.path])
        text = info.decode("utf-8")
        text = text.strip("\n")

        file_mime_cache[self.path]=text
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

    def get_as_row_data(self) -> dict[str,str]:
        return {
            "path": self.path,
            "name": self.get_color() + self.get_name() + colors.fg.default,
            "perms": self.get_permissions(),
            "size": self.get_size(),
            "info": self.info,
            "mime": self.mime,
        }

class FileList(component.Component):
    def __init__(self,dir:str,width:int=120,height:int=15,name:str="FileList"):
        super().__init__(width,height,name)
        self.dir = dir
        self.files: list[File]=[]
        self.selected = 0
        self.scroll = 0

        self.table = table.Table(
            title = self.dir,
            width = self.width,
            height = self.height,
            columns = ["path","name","size","perms","info","mime"],
            column_order = ["perms","name","size","info"],
            column_justifies = {
                "path": string_util.TextJustify.Left,
                "name": string_util.TextJustify.Left,
                "size": string_util.TextJustify.Right,
                "perms": string_util.TextJustify.Left,
                "info": string_util.TextJustify.Left,
                "mime": string_util.TextJustify.Left,
            },
            column_separator = "  ",
            scroll = self.scroll,
            show_title = False,
        )
        self.set_dir(dir)
        @self.table.set_filter
        def _(row: table.TableRow):
            # name=string_util.strip_ansi(row.data["name"])
            return True
    
    def set_dir(self,dir:str):
        self.dir=dir
        file_names=os.listdir(dir)
        file_names.sort(key=lambda x: x.lower())
        file_names.insert(0,"..")
        file_names.insert(0,".")

        self.files=[]

        for fname in file_names:
            self.files.append(File(os.path.join(self.dir, fname)))
        
        self.update_table()

    def update_table(self):
        self.table.title=self.dir
        self.table.clear()
        for f in self.files:
            self.table.add_row(f.get_as_row_data(),dont_recalc_sizes=True)
        self.table.update_disp_rows()
    
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
    
    def input(self, text: str):
        if text==keys.up:
            self.selected -= 1
        elif text==keys.down:
            self.selected += 1
        elif text==keys.page_up:
            self.selected -= self.height
        elif text==keys.page_down:
            self.selected += self.height
        self.table.update_view()

    def view(self) -> str:
        s:str = ""

        self.table.scroll = self.scroll
        self.table.selected = self.selected
        self.table.width = self.width
        self.table.height = self.height
        self.table.calc_column_sizes()
        self.table.update_view()
        self.selected=self.table.selected
        self.scroll=self.table.scroll

        s += self.table.view()


        # debug stuff
        s += "\n"
        s += f"selected={self.table.selected}"
        s += f" scroll={self.table.scroll}"
        s += f" height={self.table.height}"
        s += f" width={self.width}"
        s += f" rows={len(self.table.rows)}"
        
        return s

            
