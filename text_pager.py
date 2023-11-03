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

tab_regex = re.compile("(\t|    )")

def get_file_lexer(mime,name,text):
    try:
        return get_lexer_for_mimetype(mime)
    except ClassNotFound:
        pass
    try:
        return guess_lexer(text)
    except ClassNotFound:
        pass
    try:
        return get_lexer_for_filename(name)
    except ClassNotFound:
        pass
    return None


class TextPager(component.Component):
    def __init__(self,
            width=80,
            height=30,
    ):
        super().__init__(width,height)
        self.text="hello!"
        self.scroll_x=0
        self.scroll_y=0
        self.border_style: su.BorderStyle = su.normal_border

    def get_line_count(self) -> int:
        return su.text_height(self.text)
    def get_text_height(self) -> int:
        return (
            min(
                self.get_line_count(),
                self.height - 2 # borders
            )
        )
    
    def update(self):
        self.scroll_y = max(min( self.scroll_y, self.get_line_count()-self.get_text_height()-2 ), 0)
    
    def update_highlight(self,mime:str="",name:str=""):
        self.text=su.strip_ansi(self.text)
        lexer = get_file_lexer(mime,name,self.text)
        self.lexer=lexer
        if lexer != None:
            self.text=pygments.highlight(self.text,lexer,TerminalFormatter())
    
    def load_from_file(self,file: File):
        try:
            with open(file.path,'r') as f:
                self.text=f.read()
        except UnicodeDecodeError:
            with open(file.path,'rb') as f:
                self.text=f.read().decode(errors="replace")
        self.update_highlight(file.mime,file.get_name())
        

    def view(self):
        s = ""

        line_count = self.get_line_count()
        line_number_digits = len(str(line_count))
        lines = self.text.split("\n")

        text_height = self.get_text_height()

        has_scroll_y_bar = line_count>text_height
        scroll_y_pos = int(self.scroll_y/line_count * text_height)
        scroll_y_height = math.ceil(text_height/line_count*text_height)

        text_width = (
            self.width
            - 2 # borders
            - 2 # padding (theres only right padding w/o a scrollbar, so this is always 2)
            - line_number_digits # line numbers
            - 3 # line number separator
        )


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

            s += su.ljust(line+colors.reset,text_width)

            if has_scroll_y_bar:
                s += colors.bg.white if y>=scroll_y_pos and y<=scroll_y_pos+scroll_y_height else colors.bg.grey
                s += " "
                s += colors.reset
            else:
                s += " " #more padding
            s += "\n"

            line_index += 1
            y += 1
        s = s.removesuffix("\n")
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
        s += f"\n{type(self.lexer)}"

        s = su.set_maxwidth(s,text_width)
        return su.border(s,self.border_style)