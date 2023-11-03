from typing import Union
from component import Component
import string_util as su
import debug

class ViewLayout(Component):
    def __init__(self,
            structure:list[list[Component]],
            width:int,
            height:int,
            name:str="ViewLayout",
    ):
        super().__init__(width,height,name)
        self.structure=structure
        self.focus=[0,0]
    
    def get_row_columns(self,row:int) -> int:
        i = 0
        for comp in self.structure[row]:
            if comp.show:
                i += 1
        return i

    def move_focus(self,dx:int,dy:int):
        self.get_focused_component().onunfocus()
        row_columns = self.get_row_columns(self.focus[1])
        self.focus[0] = (self.focus[0] + dx) % row_columns
        self.focus[1] = (self.focus[1] + dy) % len(self.structure)
        self.get_focused_component().onfocus()
        debug.debug_log += f"Moved focus to {self.focus} '{self.get_focused_component().name}'\n"
    
    def get_focused_component(self) -> Component:
        return self.structure[self.focus[1]][self.focus[0]]
    
    def input(self,text:str):
        focused_comp=self.get_focused_component()
        focused_comp.input(text)
        debug.debug_log += f"{focused_comp.name} got {repr(text)}\n"
    
    def view(self) -> str:
        s = ""
        for row in self.structure:
            row_str = ""
            for comp in row:
                if not comp.show:
                    continue
    
                row_str = su.join_horizontal(
                    row_str,
                    su.set_maxheight(
                        su.set_maxwidth(
                            comp.view(),
                            comp.width
                        ),
                        comp.height
                    ),
                    padding_char=" | "
                )
            s += "-"*su.text_width(row_str)
            s += "\n"
            s += row_str
        s += "\n"
        s += f"focus.x={self.focus[0]}"
        s += f" focus.y={self.focus[1]}"
        return s