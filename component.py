class Component:
    def __init__(self,width:int,height:int,name:str):
        self.width=width
        self.height=height
        self.name=name
        self.show: bool=True
        self.focused: bool=False
    
    # Handle input
    def input(self,text:str,layout):
        pass

    def onfocus(self):
        self.focused=True
    
    def onunfocus(self):
        self.focused=False
    
    # Render the component
    def view(self) -> str:
        return "Hello World!"