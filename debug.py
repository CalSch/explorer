import string_util as su

# debug_log=text_pager.TextPager(60,12,title="Debug Log")
# debug_log.onfocus()
debug_text=""
debug_mode=False
logfile="debug.txt"
def log(text:str):
    debug_log += text+"\n"
    with open(logfile,'w') as f:
        f.write(debug_log)
# debug_log=""