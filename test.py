import string_util,table,colors,random

cols = ["thing1","thing2","is cool"]

t = table.Table(
    "hello",
    15,
    cols,
    ["thing2", "is cool", "thing1"],
    {
        "thing1": string_util.TextJustify.Left,
        "thing2": string_util.TextJustify.Right,
        "is cool": string_util.TextJustify.Center,
    },
    " | "
)

t.add_row({
    "thing1": "banana",
    "thing2": "apple",
    "is cool": "yes",
})
t.add_row({
    "thing1": "orange",
    "thing2": "carrot",
    "is cool": "no",
})
t.add_row({
    "thing1": "carpet",
    "thing2": "very long string of text",
    "is cool": "maybe",
})

for i in range(30):
    t.add_row({
        "thing1":  str(random.randint(-100,100)),
        "thing2":  str(random.randint(-1000,1000)),
        "is cool": random.choice(["yes","no","maybe"]),
    })

t.calc_column_sizes()

while True:
    print(t.view())
    t.scroll += 1
    input()