import string_util as su
import colors
import component
import scrollbar
import math

class TableRow:
    def __init__(self,
                 data: dict[str,str],
                 justify: dict[str,su.TextJustify],
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
            if self.justify[col] == su.TextJustify.Left:
                s += su.ljust(text,width)
            elif self.justify[col] == su.TextJustify.Center:
                s += su.cjust(text,width)
            elif self.justify[col] == su.TextJustify.Right:
                s += su.rjust(text,width)
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
                 column_justifies: dict[str,su.TextJustify],
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
        self.column_justifies: dict[str, su.TextJustify] = column_justifies
        self.rows: list[TableRow]=[]
        self.column_separator = column_separator
        self.scroll = scroll
        self.selected = 0
        self.show_title=show_title
        self.filter=lambda s : True
        self.disp_rows: list[TableRow]=[]
        self.scrollbar = scrollbar.Scrollbar( 1, self.height, 0, 0, 0 )
        self.update_scrollbar()
    
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
    
    def update_scrollbar(self):
        self.scrollbar.height = self.height
        self.scrollbar.view_height = self.get_shown_rows()
        self.scrollbar.view_scroll = self.scroll
        self.scrollbar.total_height = len(self.disp_rows)
    
    def clear(self):
        self.rows = []
        self.update_disp_rows()
    
    def calc_column_sizes(self):
        for col in self.columns:
            self.column_sizes[col] = su.text_width(col)
        for row in self.rows:
            for col in self.columns:
                width = su.text_width(row.data[col])
                if width > self.column_sizes[col]:
                    self.column_sizes[col] = width
    
    def get_total_width(self) -> int:
        width = 0
        for col in self.column_order:
            width += self.column_sizes[col]
            width += su.text_width(self.column_separator)
        width -= su.text_width(self.column_separator) # remove the last column separator
        return width

    def get_field(self, field: str) -> list[str]:
        l = []
        for row in self.rows:
            l.append(su.strip_ansi(row.data[field]))
        return l
    
    def update_view(self):
        # Clamp selection
        self.selected=max(0,min(len(self.disp_rows)-1, self.selected)) # min: 0  max: # of files - 1

        # Update scrolling
        # center the view around the selected item, but clamp it to not go out of bounds
        self.scroll = int(max(
            0,
            min(
                len(self.disp_rows)-self.get_shown_rows(),
                # 100000000000000,
                self.selected-math.ceil(self.get_shown_rows()/2)
            )
        ))
    

    def get_shown_rows(self):
        return (self.height
            - int(self.show_title)*2 # 2 lines for the title
            - 2 # column names and horizontal separator
            - 2 # "..." lines
        )

    def view(self) -> str:
        show_scrollbar = self.get_shown_rows()<len(self.disp_rows)
        self.update_scrollbar()
        s = ""
        if self.show_title:
            s += self.title
            s += "\n\n"
        for col in self.column_order:
            s += su.ljust(col.upper(), self.column_sizes[col])
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
                i>self.scroll+self.get_shown_rows()-1
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
        if self.scroll+self.get_shown_rows() < len(self.disp_rows)-1:
            s += "... "
        s += "\n"
        s = su.set_maxwidth(s, self.width - 2)
        if show_scrollbar:
            s = su.join_horizontal(s, self.scrollbar.view())
        s += "\x1b[0m"

        return su.set_maxwidth(s,self.width)