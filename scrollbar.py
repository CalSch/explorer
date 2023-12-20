import component
import colors
import math

class Scrollbar(component.Component):
    def __init__(self, parent: component.Component, width:int, height: int, view_height:int, view_scroll: int, total_hight: int, name: str="Scrollbar"):
        super().__init__(width, height, name, parent)
        self.view_height=view_height
        self.view_scroll=view_scroll
        self.total_height=total_hight
    def view(self,view_scroll:int=None):
        if view_scroll != None:
            self.view_scroll=view_scroll
        scroll_pos = int(self.view_scroll/self.total_height * self.height)
        scroll_height = math.ceil(self.view_height/self.total_height*self.height)
        s = ""
        for i in range(self.height):
            s += colors.bg.white if i>=scroll_pos and i<=scroll_pos + scroll_height else colors.bg.grey
            s += " "*self.width
            s += colors.reset
            s += "\n"
        return s.removesuffix("\n")