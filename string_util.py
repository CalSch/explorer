import re,math
from enum import Enum

class TextJustify(Enum):
    Left = 0
    Right = 1
    Center = 2

ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')

def strip_ansi(s: str):
    return ansi_escape.sub('',s)

def text_width(s: str):
    width=0
    for line in s.splitlines():
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
    lines = s.splitlines()
    for i in range(len(lines)):
        l=lines[i]
        index=horizontal_position_to_index(l,maxwidth)
        lines[i]=lines[i][:index]
    
    return "\n".join(lines)
def horizontal_position_to_index(s:str,x:int):
    # i don't think this works when `x` is inside an ANSI escape sequence
    for i in range(len(s)):
        new_str=s[:i]
        if text_width(new_str) == x:
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
    new_str = ""
    s1_lines=s1.splitlines()
    s2_lines=s2.splitlines()
    for i in range(h1):
        line1=s1_lines[i]
        line2=s2_lines[i]
        new_str += justify(line1,w1,s1_justify,s1_justify_char)
        new_str += padding_char * padding
        new_str += justify(line2,w2,s2_justify,s2_justify_char)
        new_str += "\n"
    return new_str
    