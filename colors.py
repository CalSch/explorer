reset = "\x1b[0m"

class invert:
    on = "\x1b[7m"
    off = "\x1b[27m"
class dim:
    on = "\x1b[2m"
    off = "\x1b[22m"

class bold:
    on = "\x1b[1m"
    off = "\x1b[22m"
class italic:
    on = "\x1b[3m"
    off = "\x1b[23m"

class fg:
    red     = "\x1b[31m"
    green   = "\x1b[32m"
    yellow  = "\x1b[33m"
    blue    = "\x1b[34m"
    magenta = "\x1b[35m"
    cyan    = "\x1b[36m"
    white   = "\x1b[37m"
    default = "\x1b[39m"
    grey    = "\x1b[38;5;0m" # 256-color

class bg:
    red     = "\x1b[41m"
    green   = "\x1b[42m"
    yellow  = "\x1b[43m"
    blue    = "\x1b[44m"
    magenta = "\x1b[45m"
    cyan    = "\x1b[46m"
    white   = "\x1b[47m"
    default = "\x1b[49m"
    grey    = "\x1b[48;5;0m" # 256-color