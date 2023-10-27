import string_util as su

str1="""i am a multiline string
new line
wowzers"""

str2="""i also am a multiline string
but with more lines
what will happen?
nobody knows!"""

print("\n=== Justifying ===")
print("+"+"-"*20+"+")
print("|"+su.justify("left",20,su.TextJustify.Left)+"|")
print("|"+su.justify("center",20,su.TextJustify.Center)+"|")
print("|"+su.justify("right",20,su.TextJustify.Right)+"|")
print("+"+"-"*20+"+")

print("\n\n=== Join Horizontal ===")
print(f"First string:\n{str1}\n")
print(f"Second string:\n{str2}\n")
print("Combined (with padding=5):")
print(su.join_horizontal(str1,str2,padding=5))

print("\n\n")
print(
    su.join_horizontal(
        su.join_horizontal(
            str1," | \n"*5
        ),
        str2
    )
)

print("\n\n=== Borders ===")
print(su.border(str1,su.retro_border))
print(su.border(str1,su.normal_border))
print(su.border(str1,su.round_border))