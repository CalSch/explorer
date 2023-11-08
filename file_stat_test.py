import os,subprocess,sys

folder=sys.argv[1]
files=os.listdir(folder)
stat={}
mime={}

for f in files:
    stat[f]=subprocess.check_output(["/usr/bin/file",folder+"/"+f])
    mime[f]=subprocess.check_output(["/usr/bin/file","-i",folder+"/"+f])

print(stat)