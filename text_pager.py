import string_util as su
import colors
import re
import math
import pygments
from pygments.lexers import get_lexer_for_mimetype,get_lexer_for_filename,guess_lexer
from pygments.formatters import TerminalFormatter
from pygments.util import ClassNotFound
from file_list import File
import component
import keys
import debug
import scrollbar

tab_regex = re.compile("(\t|    )")

def get_file_lexer(mime,name,text):
    try:
        return (get_lexer_for_filename(name),"filename")
    except ClassNotFound:
        pass
    try:
        return (guess_lexer(text),"guess")
    except ClassNotFound:
        pass
    try:
        return (get_lexer_for_mimetype(mime),"mimetype")
    except ClassNotFound:
        pass
    return (None,"none")


class TextPager(component.Component):
    def __init__(self,
            width=80,
            height=30,
            title:str="",
            name:str="TextPager"
    ):
        super().__init__(width,height,name)
        self.text="hello!\n"
        self.title=title
        self.scroll_x=0
        self.scroll_y=0
        self.border_style: su.BorderStyle = su.normal_border
        self.onunfocus()
        self.scrollbar = scrollbar.Scrollbar(1, self.get_text_height(), self.get_text_height(), 0, self.get_line_count())
        # self.update_highlight()

    def get_line_count(self) -> int:
        return su.text_height(self.text)
    def get_text_height(self) -> int:
        return (
            min(
                self.get_line_count(),
                self.height
                            - 2 # borders
                            - (self.title!="") # title (not if empty)
            )
        )
    
    def update(self):
        self.scroll_y = max(min( self.scroll_y, self.get_line_count()-self.get_text_height() ), 0)
        self.scrollbar.view_scroll=self.scroll_y
    
    def update_highlight(self,mime:str="",name:str=""):
        self.text=su.strip_ansi(self.text)
        lexer, method = get_file_lexer(mime,name,self.text)
        self.lexer=lexer
        if lexer != None:
            self.text=pygments.highlight(self.text,lexer,TerminalFormatter())
        # debug.debug_text += f"Loaded {type(lexer)}\n"
        # debug.debug_text += f"Method {method}\n"
        debug.log(f"{self.name} loaded {type(lexer)} with method '{method}'")
    
    def load_from_file(self,file: File):
        try:
            with open(file.path,'r') as f:
                self.text=f.read()
        except UnicodeDecodeError:
            with open(file.path,'rb') as f:
                self.text=f.read().decode(errors="replace")
        self.update_highlight(file.mime,file.get_name())
        self.scrollbar.view_height=self.get_text_height()        
        self.scrollbar.height=self.get_text_height()        
        self.scrollbar.total_height=self.get_line_count()   

    def input(self, text: str,layout):
        if text==keys.up:
            self.scroll_y -= 1
        elif text==keys.down:
            self.scroll_y += 1
        elif text==keys.page_up:
            self.scroll_y -= self.get_text_height()
        elif text==keys.page_down:
            self.scroll_y += self.get_text_height()

    def onfocus(self):
        self.border_style = su.normal_border
        self.border_style.color = colors.fg.default
    
    def onunfocus(self):
        self.border_style = su.dashed_border
        self.border_style.color = colors.dim.on

    def view(self):
        s = ""

        line_count = self.get_line_count()
        line_number_digits = len(str(line_count))
        lines = self.text.split("\n")

        text_height = self.get_text_height()

        has_scroll_y_bar = line_count>text_height

        text_width = (
            self.width
            - 2 # borders
            - 3 # padding/scrollbar (theres only right padding w/o a scrollbar, so this is always 2)
            - line_number_digits # line numbers
            - 3 # line number separator
        )

        if self.title!="":
            s += colors.bold.on
            s += su.cjust(self.title+colors.bold.off,self.width-10) #idk why I did -10, it just looks right
            s += "\n"

        line_index = 1
        y = 0
        for line in lines:
            if line_index < self.scroll_y+1 or line_index > self.scroll_y + text_height:
                line_index += 1
                continue
            line = re.sub(tab_regex,colors.dim.on+"⎸   "+colors.dim.off,line)
            line = su.set_maxwidth(line,text_width)
            # if i%2==0:
            #     s += colors.bg.
            s += "  " #padding

            #line number
            s += colors.fg.yellow
            s += su.rjust(str(line_index),line_number_digits)
            s += colors.reset

            #spacer
            s += " "
            s += colors.dim.on
            s += " "
            s += colors.dim.off

            s += su.set_maxwidth(
                su.ljust(
                    line+colors.reset,
                    text_width
                ),
                text_width
            )

            if not has_scroll_y_bar:
                s += " " #add padding
            s += "\n"

            line_index += 1
            y += 1
        s = s.removesuffix("\n")
        s = su.join_horizontal(s, self.scrollbar.view(), padding=0)
        # print("-"*self.width)

        # debug stuff
        s += "\n"
        # s += f"selected={self.selected}"
        s += f" scroll={self.scroll_y}"
        s += f" width={self.width}"
        s += f" height={self.height}"
        s += f" lines={self.get_line_count()}"
        s += f" text_width={text_width}"
        s += f" text_height={self.get_text_height()}"
        # s += f"\n{type(self.lexer)}"

        return su.border(s,self.border_style)