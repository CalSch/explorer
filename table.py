import string_util
import colors
import component

class TableRow:
    def __init__(self,
                 data: dict[str,str],
                 justify: dict[str,string_util.TextJustify],
                 column_separator: str = " "
                 ):
        self.data=data
        self.justify=justify
        self.column_separator=column_separator

    def view(self, sizes: dict[str,int], order: list[str]) -> str:
        s = ""
        for col in order:
            text = self.data[col]
            width = sizes[col]
            if self.justify[col] == string_util.TextJustify.Left:
                s += string_util.ljust(text,width)
            elif self.justify[col] == string_util.TextJustify.Center:
                s += string_util.cjust(text,width)
            elif self.justify[col] == string_util.TextJustify.Right:
                s += string_util.rjust(text,width)
            if order[-1] != col: # dont print the separator on the last column
                s += self.column_separator
        return s

class Table(component.Component):
    def __init__(self,
                 title: str,
                 height: int,
                 width: int,
                 columns: list[str],
                 column_order: list[str],
                 column_justifies: dict[str,string_util.TextJustify],
                 column_separator: str = " ",
                 scroll: int = 0,
                 show_title: bool = True,
                 name:str="Table"
        ):
        super().__init__(width,height,name)
        self.title=title
        self.columns=columns
        self.column_order=column_order
        self.column_sizes: dict[str,int]={}
        self.column_justifies: dict[str, string_util.TextJustify] = column_justifies
        self.rows: list[TableRow]=[]
        self.column_separator = column_separator
        self.scroll = scroll
        self.selected = 0
        self.show_title=show_title
        self.filter=lambda s : True
        self.disp_rows: list[TableRow]=[]
    
    def add_row(self, data: dict[str,str], dont_recalc_sizes: bool = False):
        row = TableRow(data,self.column_justifies,self.column_separator)
        self.rows.append(row)
        if not dont_recalc_sizes:
            self.calc_column_sizes()
    
    def set_filter(self,func):
        self.filter=func
        self.update_disp_rows()
    
    def update_disp_rows(self):
        self.disp_rows=[]
        for row in self.rows:
            if self.filter(row):
                self.disp_rows.append(row)
    
    def clear(self):
        self.rows = []
        self.update_disp_rows()
    
    def calc_column_sizes(self):
        for col in self.columns:
            self.column_sizes[col] = string_util.text_width(col)
        for row in self.rows:
            for col in self.columns:
                width = string_util.text_width(row.data[col])
                if width > self.column_sizes[col]:
                    self.column_sizes[col] = width
    
    def get_total_width(self) -> int:
        width = 0
        for col in self.column_order:
            width += self.column_sizes[col]
            width += string_util.text_width(self.column_separator)
        width -= string_util.text_width(self.column_separator) # remove the last column separator
        return width

    def get_field(self, field: str) -> list[str]:
        l = []
        for row in self.rows:
            l.append(string_util.strip_ansi(row.data[field]))
        return l
    
    def update_view(self):
        # Clamp selection
        self.selected=max(0,min(len(self.disp_rows)-1, self.selected)) # min: 0  max: # of files - 1

        # Update scrolling
        # center the view around the selected item, but clamp it to not go out of bounds
        self.scroll = int(max(
            0,
            min(
                len(self.disp_rows)-self.height,
                # 100000000000000,
                self.selected-self.height/2
            )
        ))

    def view(self) -> str:
        s = ""
        if self.show_title:
            s += self.title
            s += "\n\n"
        for col in self.column_order:
            s += string_util.ljust(col.upper(), self.column_sizes[col])
            if self.column_order[-1] != col: # dont print the separator on the last column
                s += self.column_separator
        s += "\n"
        s += "-" * self.get_total_width()
        s += "\n"
        if self.scroll>0:
            s += "... "
        s += "\n"
        i = 0
        for row in self.disp_rows:
            if (
                i<self.scroll or
                i>self.scroll+self.height-1
            ):
                i += 1
                continue
            s += "\x1b[0m"
            if i == self.selected:
                s += colors.invert.on

            s += row.view(self.column_sizes,self.column_order)

            if i == self.selected:
                s += colors.invert.off
            s += "\n"

            i += 1
        if self.scroll+self.height < len(self.disp_rows)-1:
            s += "... "
        s += "\n"
        s += "\x1b[0m"

        return string_util.set_maxwidth(s,self.width)