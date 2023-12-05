import re,math
from enum import Enum
import colors

class TextJustify(Enum):
    Left = 0
    Right = 1
    Center = 2

class BorderStyle:
    def __init__(self,
        top: str,
        bottom: str,
        left: str,
        right: str,
        #corners
        tl: str,
        tr: str,
        bl: str,
        br: str,
        color: str = colors.fg.default
    ):
        self.top=top
        self.bottom=bottom
        self.left=left
        self.right=right
        self.tl=tl
        self.tr=tr
        self.bl=bl
        self.br=br
        self.color=color
def make_simple_border(horiz:str,vert:str,corner:str) -> BorderStyle:
    return BorderStyle(
        horiz,horiz,
        vert,vert,
        corner,corner,corner,corner
    )

retro_border = make_simple_border("-","|","+")
normal_border = BorderStyle(
    "─","─","│","│",
    "┌","┐","└","┘"
)
round_border = BorderStyle(
    "─","─","│","│",
    "╭","╮","╰","╯"
)
bold_border = BorderStyle(
    "━","━","┃","┃",
    "┏","┓","┗","┛"
)
dashed_border = BorderStyle(
    "╌","╌","┆","┆",
    "┌","┐","└","┘"
)

ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')

def strip_ansi(s: str):
    return ansi_escape.sub('',s)

def text_width(s: str):
    width=0
    for line in s.split("\n"):
        width=max(width,len(strip_ansi(line)))
    return width

def text_height(s: str):
    return s.count("\n")+1

def ljust(s: str, width: int, fill: str = " "):
    return s + fill*(width-text_width(s))
def rjust(s: str, width: int, fill: str = " "):
    return fill*(width-text_width(s)) + s
def cjust(s: str, width: int, fill: str = " "):
    return fill*math.floor((width-text_width(s))/2) + s + fill*math.ceil((width-text_width(s))/2)

def justify(s: str, width: int, direction: TextJustify, fill: str = " "):
    if direction == TextJustify.Left:
        return ljust(s,width,fill)
    elif direction == TextJustify.Right:
        return rjust(s,width,fill)
    elif direction == TextJustify.Center:
        return cjust(s,width,fill)

def set_maxwidth(s:str,maxwidth:int):
    if maxwidth<0:
        return s
    if text_width(s)<=maxwidth:
        return s
    lines = s.split("\n")
    for i in range(len(lines)):
        l=lines[i]
        index=horizontal_position_to_index(l,maxwidth)
        lines[i]=lines[i][:index]
    
    return "\n".join(lines)
def set_minwidth(s:str,minwidth:int) -> str:
    if minwidth<0:
        return s
    if text_width(s)>=minwidth:
        return s
    lines=s.split("\n")
    for i in range(len(lines)):
        lines[i]=ljust(lines[i],minwidth)
    return "\n".join(lines)

def set_maxheight(s:str,height:int) -> str:
    if height<0:
        return s
    if text_height(s)>=height:
        return s
    lines=s.split("\n")
    return "\n".join(lines[:height-1])
def set_minheight(s:str,height:int) -> str:
    return s + "\n"*max(0,height-text_height(s))

def set_width(s:str,width:int) -> str:
    s = set_maxwidth(s, width)
    s = set_minwidth(s, width)
    return s
def set_height(s:str,height:int) -> str:
    s = set_maxheight(s, height)
    s = set_minheight(s, height)
    return s

def horizontal_position_to_index(s:str,x:int):
    # go from right to left (it makes it work better and i dont want to explain it here)
    for i in range(len(s)-1,-1,-1):
        new_str=s[:i]
        if text_width(new_str) == x:
            # print("|",i,"|",new_str,";;\x1b[0m;;")
            return i

def join_horizontal(
        s1: str,
        s2: str,
        padding: int = 1,
        s1_justify: TextJustify = TextJustify.Left,
        s2_justify: TextJustify = TextJustify.Left,
        padding_char: str = " ",
        s1_justify_char: str = " ",
        s2_justify_char: str = " ",
    ) -> str:
    if s1=="":
        return s2
    if s2=="":
        return s1
    w1=text_width(s1)
    w2=text_width(s2)
    h1=text_height(s1)
    h2=text_height(s2)
    #make the height the same
    if h1>h2:
        for i in range(h1-h2):
            s2+="\n"
    elif h2>h1:
        for i in range(h2-h1):
            s1+="\n"
    # redo text_heights
    h1=text_height(s1)
    h2=text_height(s2)

    new_str = ""
    s1_lines=s1.split("\n")
    s2_lines=s2.split("\n")
    for i in range(h1):
        line1=s1_lines[i]
        line2=s2_lines[i]
        new_str += justify(line1,w1,s1_justify,s1_justify_char)
        new_str += colors.reset
        new_str += padding_char * padding
        new_str += justify(line2,w2,s2_justify,s2_justify_char)
        new_str += "\n"
    return new_str

def border(text:str,style:BorderStyle) -> str:
    lines=text.split("\n")
    width=text_width(text)
    s = ""
    s += style.color
    s += style.tl
    s += style.top * width
    s += style.tr
    s += colors.reset
    s += "\n"

    for line in lines:
        s += style.color
        s += style.left + colors.reset + ljust(line,width) + style.color + style.right
        s += colors.reset
        s += "\n"
    
    s += style.color
    s += style.bl
    s += style.bottom * width
    s += style.br
    s += colors.reset
    return s

def float_text(s:str):
    width=text_width(s)
    s=set_minwidth(s,width)
    s=s.replace("\n",f"\x1b[1B\x1b[{width}D")
    return s

def goto(col:int,row:int) -> str:
    return f"\x1b[{row};{col}H"