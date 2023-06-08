from datamodels.types import Font

lowercase_letters = {
    " ": [0b00000, 0b00000, 0b00000, 0b00000, 0b00000, 0b00000, 0b00000],
    "a": [0b00000, 0b00000, 0b01110, 0b00001, 0b01111, 0b10001, 0b01111],
    "b": [0b10000, 0b10000, 0b10110, 0b11001, 0b10001, 0b10001, 0b10110],
    "c": [0b00000, 0b00000, 0b01110, 0b10000, 0b10000, 0b10001, 0b01110],
    "d": [0b00001, 0b00001, 0b01101, 0b10011, 0b10001, 0b10001, 0b01111],
    "e": [0b00000, 0b00000, 0b01110, 0b10001, 0b11111, 0b10000, 0b01110],
    "f": [0b00110, 0b01001, 0b01000, 0b11100, 0b01000, 0b01000, 0b01000],
    "g": [0b00000, 0b01111, 0b10001, 0b10001, 0b01111, 0b00001, 0b01110],
    "h": [0b10000, 0b10000, 0b10110, 0b11001, 0b10001, 0b10001, 0b10001],
    "i": [0b00100, 0b00000, 0b01100, 0b00100, 0b00100, 0b00100, 0b01110],
    "j": [0b00001, 0b00000, 0b00011, 0b00001, 0b00001, 0b01001, 0b00110],
    "k": [0b10000, 0b10000, 0b10010, 0b10100, 0b11100, 0b10010, 0b10001],
    "l": [0b01100, 0b00100, 0b00100, 0b00100, 0b00100, 0b00100, 0b01110],
    "m": [0b00000, 0b00000, 0b00000, 0b11010, 0b10101, 0b10001, 0b10001],
    "n": [0b00000, 0b00000, 0b10110, 0b11001, 0b10001, 0b10001, 0b10001],
    "o": [0b00000, 0b00000, 0b01110, 0b10001, 0b10001, 0b10001, 0b01110],
    "p": [0b00000, 0b11110, 0b10001, 0b10001, 0b11110, 0b10000, 0b10000],
    "q": [0b00000, 0b01110, 0b10001, 0b10001, 0b01111, 0b00001, 0b00001],
    "r": [0b00000, 0b00000, 0b10110, 0b11001, 0b10000, 0b10000, 0b10000],
    "s": [0b00000, 0b00000, 0b01111, 0b10000, 0b01110, 0b00001, 0b11110],
    "t": [0b01000, 0b01000, 0b11100, 0b01000, 0b01000, 0b01001, 0b00110],
    "u": [0b00000, 0b00000, 0b10001, 0b10001, 0b10001, 0b10011, 0b01101],
    "v": [0b00000, 0b00000, 0b10001, 0b10001, 0b01010, 0b01010, 0b00100],
    "w": [0b00000, 0b00000, 0b10001, 0b10001, 0b10101, 0b10101, 0b01010],
    "x": [0b00000, 0b00000, 0b10001, 0b01010, 0b00100, 0b01010, 0b10001],
    "y": [0b00000, 0b10001, 0b10001, 0b10001, 0b01111, 0b00001, 0b01110],
    "z": [0b00000, 0b00000, 0b11111, 0b00010, 0b00100, 0b01000, 0b11111],
}

uppercase_letters = {
    " ": [0b00000, 0b00000, 0b00000, 0b00000, 0b00000, 0b00000, 0b00000],
    "A": [0b01110, 0b10001, 0b10001, 0b11111, 0b10001, 0b10001, 0b10001],
    "B": [0b11110, 0b10001, 0b10001, 0b11110, 0b10001, 0b10001, 0b11110],
    "C": [0b01110, 0b10001, 0b10000, 0b10000, 0b10000, 0b10001, 0b01110],
    "D": [0b11110, 0b10001, 0b10001, 0b10001, 0b10001, 0b10001, 0b11110],
    "E": [0b11111, 0b10000, 0b10000, 0b11110, 0b10000, 0b10000, 0b11111],
    "F": [0b11111, 0b10000, 0b10000, 0b11110, 0b10000, 0b10000, 0b10000],
    "G": [0b01110, 0b10001, 0b10000, 0b10011, 0b10001, 0b10001, 0b01110],
    "H": [0b10001, 0b10001, 0b10001, 0b11111, 0b10001, 0b10001, 0b10001],
    "I": [0b01110, 0b00100, 0b00100, 0b00100, 0b00100, 0b00100, 0b01110],
    "J": [0b00001, 0b00001, 0b00001, 0b00001, 0b00001, 0b10001, 0b01110],
    "K": [0b10001, 0b10010, 0b10100, 0b11000, 0b10100, 0b10010, 0b10001],
    "L": [0b10000, 0b10000, 0b10000, 0b10000, 0b10000, 0b10000, 0b11111],
    "M": [0b10001, 0b11011, 0b10101, 0b10101, 0b10001, 0b10001, 0b10001],
    "N": [0b10001, 0b10001, 0b11001, 0b10101, 0b10011, 0b10001, 0b10001],
    "O": [0b01110, 0b10001, 0b10001, 0b10001, 0b10001, 0b10001, 0b01110],
    "P": [0b11110, 0b10001, 0b10001, 0b11110, 0b10000, 0b10000, 0b10000],
    "Q": [0b01110, 0b10001, 0b10001, 0b10001, 0b10101, 0b10010, 0b01101],
    "R": [0b11110, 0b10001, 0b10001, 0b11110, 0b10100, 0b10010, 0b10001],
    "S": [0b01110, 0b10001, 0b10000, 0b01110, 0b00001, 0b10001, 0b01110],
    "T": [0b11111, 0b00100, 0b00100, 0b00100, 0b00100, 0b00100, 0b00100],
    "U": [0b10001, 0b10001, 0b10001, 0b10001, 0b10001, 0b10001, 0b01110],
    "V": [0b10001, 0b10001, 0b10001, 0b10001, 0b10001, 0b01010, 0b00100],
    "W": [0b10001, 0b10001, 0b10001, 0b10101, 0b10101, 0b10101, 0b01010],
    "X": [0b10001, 0b10001, 0b01010, 0b00100, 0b01010, 0b10001, 0b10001],
    "Y": [0b10001, 0b10001, 0b10001, 0b01110, 0b00100, 0b00100, 0b00100],
    "Z": [0b11111, 0b00001, 0b00010, 0b00100, 0b01000, 0b10000, 0b11111],
}

lowercase_numbers = {
    "0": [0b00000, 0b01110, 0b10001, 0b10001, 0b10001, 0b10001, 0b01110],
    "1": [0b00000, 0b00010, 0b00110, 0b00010, 0b00010, 0b00010, 0b01111],
    "2": [0b00000, 0b01110, 0b10001, 0b00001, 0b00010, 0b00100, 0b11111],
    "3": [0b00000, 0b01110, 0b10001, 0b00001, 0b00110, 0b00001, 0b11110],
    "4": [0b00000, 0b00001, 0b00011, 0b00101, 0b01001, 0b01111, 0b00001],
    "5": [0b00000, 0b11111, 0b10000, 0b11110, 0b00001, 0b00001, 0b11110],
    "6": [0b00000, 0b01110, 0b10001, 0b10000, 0b11110, 0b10001, 0b01110],
    "7": [0b00000, 0b11111, 0b00001, 0b00010, 0b00100, 0b01000, 0b10000],
    "8": [0b00000, 0b01110, 0b10001, 0b01110, 0b10001, 0b10001, 0b01110],
    "9": [0b00000, 0b01110, 0b10001, 0b10001, 0b01111, 0b00001, 0b01110],
}

uppercase_numbers = {
    "0": [0b01110, 0b10001, 0b10001, 0b10001, 0b10001, 0b10001, 0b01110],
    "1": [0b01100, 0b00100, 0b00100, 0b00100, 0b00100, 0b00100, 0b01110],
    "2": [0b11110, 0b00001, 0b00001, 0b00010, 0b00100, 0b01000, 0b11111],
    "3": [0b11110, 0b00001, 0b00001, 0b00110, 0b00001, 0b00001, 0b11110],
    "4": [0b10001, 0b10001, 0b10001, 0b11111, 0b00001, 0b00001, 0b00001],
    "5": [0b11111, 0b10000, 0b10000, 0b11110, 0b00001, 0b00001, 0b11110],
    "6": [0b01110, 0b10000, 0b10000, 0b11110, 0b10001, 0b10001, 0b01110],
    "7": [0b11111, 0b00001, 0b00001, 0b00010, 0b00100, 0b01000, 0b10000],
    "8": [0b01110, 0b10001, 0b10001, 0b01110, 0b10001, 0b10001, 0b01110],
    "9": [0b01110, 0b10001, 0b10001, 0b01111, 0b00001, 0b00001, 0b01110],
}

symbols = {
    ".": [0b00000, 0b00000, 0b00000, 0b00000, 0b00000, 0b01100, 0b01100],
    ",": [0b00000, 0b00000, 0b00000, 0b00000, 0b0000, 0b01000, 0b10000],
    '"': [0b00000, 0b00000, 0b10001, 0b10001, 0b01010, 0b01010, 0b00100],
    "'": [0b00000, 0b00000, 0b00100, 0b00100, 0b01000, 0b00000, 0b00000],
    "?": [0b01110, 0b10001, 0b00001, 0b00010, 0b00100, 0b00000, 0b00100],
    "!": [0b00100, 0b00100, 0b00100, 0b00100, 0b00100, 0b00000, 0b00100],
    "@": [0b01110, 0b10001, 0b10101, 0b10111, 0b10100, 0b10001, 0b01110],
    "_": [0b00000, 0b00000, 0b00000, 0b00000, 0b00000, 0b00000, 0b11111],
    "*": [0b00100, 0b10101, 0b01110, 0b10101, 0b00100, 0b00000, 0b00000],
    "#": [0b01010, 0b01010, 0b11111, 0b01010, 0b11111, 0b01010, 0b01010],
    "$": [0b00010, 0b01111, 0b10100, 0b01110, 0b00101, 0b11110, 0b00100],
    "%": [0b11000, 0b11001, 0b00010, 0b00100, 0b01000, 0b10011, 0b00011],
    "&": [0b00110, 0b01001, 0b01001, 0b00110, 0b10011, 0b10011, 0b01101],
    "(": [0b00010, 0b00100, 0b01000, 0b01000, 0b01000, 0b00100, 0b00010],
    ")": [0b01000, 0b00100, 0b00010, 0b00010, 0b00010, 0b00100, 0b01000],
    "+": [0b00000, 0b00100, 0b00100, 0b11111, 0b00100, 0b00100, 0b00000],
    "-": [0b00000, 0b00000, 0b00000, 0b11111, 0b00000, 0b00000, 0b00000],
    "/": [0b00000, 0b00001, 0b00010, 0b00100, 0b01000, 0b10000, 0b00000],
    ":": [0b00000, 0b00100, 0b00000, 0b00000, 0b00100, 0b00000, 0b00000],
    ";": [0b00000, 0b00100, 0b00000, 0b00000, 0b00100, 0b00100, 0b00000],
    "<": [0b00010, 0b00100, 0b01000, 0b10000, 0b01000, 0b00100, 0b00010],
}

default_font = Font(
    character_to_bytes={
        **lowercase_letters,
        **uppercase_letters,
        **lowercase_numbers,
        **uppercase_numbers,
        **symbols,
    },
    character_width=5,
    character_height=7,
    dropdown_letters=["g", "j", "p", "q", "y"],
)
