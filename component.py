class Component:
    def __init__(self,width:int,height:int):
        self.width=width
        self.height=height
        self.show: bool=True
    
    # Handle input
    def input(self,text:str):
        pass
    
    # Render the component
    def view(self) -> str:
        return "Hello World!"