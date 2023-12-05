from typing import Union
from component import Component
import string_util as su
import debug
import keys

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
        debug.log(f"Moved focus to {self.focus} '{self.get_focused_component().name}'")
    def set_focus(self,x:int,y:int):
        self.get_focused_component().onunfocus()
        row_columns = self.get_row_columns(self.focus[1])
        self.focus[0] = x % row_columns
        self.focus[1] = y % len(self.structure)
        self.get_focused_component().onfocus()
        debug.log(f"Set focus to {self.focus} '{self.get_focused_component().name}'")
    
    def get_focused_component(self) -> Component:
        return self.structure[self.focus[1]][self.focus[0]]
    
    def input(self,text:str):
        if text==keys.ctrl_up:
            self.move_focus(0,-1)
        elif text==keys.ctrl_down:
            self.move_focus(0,1)
        elif text==keys.ctrl_left:
            self.move_focus(-1,0)
        elif text==keys.ctrl_right:
            self.move_focus(1,0)
        else:
            focused_comp=self.get_focused_component()
            debug.log(f"{focused_comp.name} got {repr(text)}")
            focused_comp.input(text,self)
    
    def view(self) -> str:
        s = ""
        for row in self.structure:
            row_str = ""
            for comp in row:
                if not comp.show:
                    continue
    
                row_str = su.join_horizontal(
                    row_str,
                    su.set_height(
                        su.set_width(
                            comp.view(),
                            comp.width
                        ),
                        comp.height
                    ),
                    padding_char=f" {su.normal_border.left} "
                )
            s += su.normal_border.top*su.text_width(row_str)
            s += "\n"
            s += row_str
        s += "\n"
        s += f"focus.x={self.focus[0]}"
        s += f" focus.y={self.focus[1]}"
        return s