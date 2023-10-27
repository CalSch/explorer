import string_util as su

class TextPager:
    def __init__(self,
            width=80,
            height=30,
    ):
        self.width=width
        self.height=height
        self.text="hello!"

    def view(self):
        return su.border(self.text,su.round_border)