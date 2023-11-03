from typing import Union
from component import Component
import string_util as su

class ViewLayout:
    def __init__(self,structure:list[list[Component]]):
        self.structure=structure
        self.focus=[0,0]
    
    def get_row_columns(self,row:int) -> int:
        i = 0
        for comp in self.structure[row]:
            if comp.show:
                i += 1
        return i

    def move_focus(self,dx:int,dy:int):
        row_columns = self.get_row_columns(self.focus[0])
        self.focus[0] = (self.focus[0] + dx) % row_columns
        self.focus[1] = (self.focus[1] + dy) % len(self.structure)
    
    def view(self) -> str:
        s = ""
        for row in self.structure:
            row_str = ""
            for comp in row:
                if not comp.show:
                    continue
                row_str = su.join_horizontal(row_str,comp.view(),padding_char=" | ")
            s += "-"*su.text_width(row_str)
            s += "\n"
            s += row_str
        return s