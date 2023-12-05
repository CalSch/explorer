import component
import string_util as su
import colors
import keys
from typing import Callable

class TextInput(component.Component):
    def __init__(self,
                 width: int,
                 height: int,
                 prompt: str="",
                 placeholder: str="",
                 name: str="TextInput",
                 use_border: bool=False
                ):
        super().__init__(width, height, name)
        self.use_border=use_border
        self.prompt=prompt
        self.placeholder=placeholder
        self.text=""
        self.cursor=0
    
    def onsubmit(self,_):
        pass

    def setonsubmit(self,func:Callable):
        self.onsubmit=func

    def updateCursor(self):
        self.cursor = max(0,min(len(self.text),self.cursor))

    def input(self, text: str,layout):
        if text == keys.left:
            self.cursor -= 1
        elif text == keys.right:
            self.cursor += 1
        elif text == keys.backspace:
            if self.cursor!=0:
                self.text=self.text[:self.cursor-1] + self.text[self.cursor:] # remove the character at `self.cursor-1`
                self.cursor -= 1
        elif text == keys.delete:
            if self.cursor!=len(self.text):
                self.text=self.text[:self.cursor] + self.text[self.cursor+1:] # remove the character at `self.cursor-1`
        elif text == keys.enter:
            self.onsubmit(self)
        elif text in [keys.up,keys.down]:
            pass
        else:
            self.text = self.text[:self.cursor] + text + self.text[self.cursor:] # insert the character into `self.cursor`
            self.cursor += len(text)
        self.updateCursor()
    
    def view(self) -> str:
        s = ""
        s += " "
        s += self.prompt
        s += " "
        text = self.text+" " if self.text else self.placeholder

        if not self.text:
            s += colors.dim.on

        s += text[:self.cursor]
        if self.focused:
            s += colors.invert.on
        s += text[self.cursor] # highlight the cursor position
        if self.focused:
            s += colors.invert.off
        s += text[self.cursor+1:]

        if not self.text:
            s += colors.dim.off
        # else:
        #     s += colors.dim.on + self.placeholder + colors.dim.off
        s += " "
        # if self.text:
        #     s += f"\n{repr(self.text)}"
        
        if self.use_border:
            s = su.border(s,su.round_border)
        
        return s
