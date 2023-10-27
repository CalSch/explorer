import string_util as su

str1="""i am a multiline string
new line
wowzers"""

str2="""i also am a multiline string
but with more lines
what will happen?
nobody knows!"""

print(su.justify("left",20,su.TextJustify.Left))
print(su.justify("center",20,su.TextJustify.Center))
print(su.justify("right",20,su.TextJustify.Right))

print(su.join_horizontal(str1,str2))