import string_util as su
import colors
import re
import math

tab_regex = re.compile("(\t|    )")

class TextPager:
    def __init__(self,
            width=80,
            height=30,
    ):
        self.width=width
        self.height=height
        self.text="hello!"
        self.scroll_x=0
        self.scroll_y=0

    def get_line_count(self) -> int:
        return su.text_height(self.text)
    def get_text_height(self) -> int:
        return (
            self.height
            - 2 # borders
        )
    
    def update(self):
        self.scroll_y = max(min( self.scroll_y, self.get_line_count()-self.get_text_height()-2 ), 0)
    
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
        print("-"*self.width)
        return su.border(s,su.round_border)