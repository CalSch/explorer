from text_pager import TextPager
from pygments import highlight
from pygments.lexers import get_lexer_for_mimetype
from pygments.lexers import PythonLexer
from pygments.formatters import TerminalFormatter
import magic
mime = magic.Magic(mime=True)

pager = TextPager(title="Cool File VERY big text")
with open("main.py",'r') as f:
    text=highlight(
        f.read(),
        PythonLexer(),
        TerminalFormatter()
    )
    pager.text=text
# print(text)
# input()
while True:
    print("\x1b[2J\x1b[H")
    pager.update()
    print(pager.view())
    input()
    pager.scroll_y+=1