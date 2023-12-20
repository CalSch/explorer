class Component:
    pass
class Component:
    def __init__(self,width:int,height:int,name:str,parent:Component):
        self.width=width
        self.height=height
        self.name=name
        self.visible: bool=True
        self.focused: bool=False
        self.parent=parent

        self.is_view_layout: bool = False
    
    # Handle input
    def input(self,text:str):
        pass

    def onfocus(self):
        self.focused=True
    
    def onunfocus(self):
        self.focused=False

    def show(self):
        self.visible=True
    def hide(self):
        self.visible=False
    
    def get_layout(self):
        if self.parent == None:
            return None
        if self.parent.is_view_layout:
            return self.parent
        else:
            return self.parent.get_layout()
    
    # Render the component
    def view(self) -> str:
        return "Hello World!"