from datamodels.types import Character, Font


def parse_raw_font(raw_font: dict) -> Font:
    characters = []
    for char_key, char_values in raw_font.items():
        characters.append(
            Character(
                character_key=char_key,
                character_value=char_values["bytes"],
                width_px=char_values["width"],
                dropdown=char_values["dropdown"],
            )
        )

    return Font(characters=characters, height_px=7)


default_font_raw = {
    " ": {
        "bytes": [0b000, 0b000, 0b000, 0b000, 0b000, 0b000, 0b000],
        "width": 3,
        "dropdown": False,
    },
    "a": {
        "bytes": [0b00000, 0b00000, 0b01110, 0b00001, 0b01111, 0b10001, 0b01111],
        "width": 5,
        "dropdown": False,
    },
    "b": {
        "bytes": [0b10000, 0b10000, 0b10110, 0b11001, 0b10001, 0b10001, 0b10110],
        "width": 5,
        "dropdown": False,
    },
    "c": {
        "bytes": [0b00000, 0b00000, 0b01110, 0b10000, 0b10000, 0b10001, 0b01110],
        "width": 5,
        "dropdown": False,
    },
    "d": {
        "bytes": [0b00001, 0b00001, 0b01101, 0b10011, 0b10001, 0b10001, 0b01111],
        "width": 5,
        "dropdown": False,
    },
    "e": {
        "bytes": [0b00000, 0b00000, 0b01110, 0b10001, 0b11111, 0b10000, 0b01110],
        "width": 5,
        "dropdown": False,
    },
    "f": {
        "bytes": [0b00110, 0b01001, 0b01000, 0b11100, 0b01000, 0b01000, 0b01000],
        "width": 5,
        "dropdown": False,
    },
    "g": {
        "bytes": [0b00000, 0b01111, 0b10001, 0b10001, 0b01111, 0b00001, 0b01110],
        "width": 5,
        "dropdown": False,
    },
    "h": {
        "bytes": [0b10000, 0b10000, 0b10110, 0b11001, 0b10001, 0b10001, 0b10001],
        "width": 5,
        "dropdown": False,
    },
    "i": {
        "bytes": [0b010, 0b000, 0b110, 0b010, 0b010, 0b010, 0b111],
        "width": 3,
        "dropdown": False,
    },
    "j": {
        "bytes": [0b0001, 0b0000, 0b0011, 0b0001, 0b0001, 0b1001, 0b0110],
        "width": 4,
        "dropdown": False,
    },
    "k": {
        "bytes": [0b10000, 0b10000, 0b10010, 0b10100, 0b11100, 0b10010, 0b10001],
        "width": 5,
        "dropdown": False,
    },
    "l": {
        "bytes": [0b110, 0b010, 0b010, 0b010, 0b010, 0b010, 0b111],
        "width": 3,
        "dropdown": False,
    },
    "m": {
        "bytes": [0b00000, 0b00000, 0b00000, 0b11010, 0b10101, 0b10001, 0b10001],
        "width": 5,
        "dropdown": False,
    },
    "n": {
        "bytes": [0b00000, 0b00000, 0b10110, 0b11001, 0b10001, 0b10001, 0b10001],
        "width": 5,
        "dropdown": False,
    },
    "o": {
        "bytes": [0b00000, 0b00000, 0b01110, 0b10001, 0b10001, 0b10001, 0b01110],
        "width": 5,
        "dropdown": False,
    },
    "p": {
        "bytes": [0b00000, 0b11110, 0b10001, 0b10001, 0b11110, 0b10000, 0b10000],
        "width": 5,
        "dropdown": False,
    },
    "q": {
        "bytes": [0b00000, 0b01110, 0b10001, 0b10001, 0b01111, 0b00001, 0b00001],
        "width": 5,
        "dropdown": False,
    },
    "r": {
        "bytes": [0b00000, 0b00000, 0b10110, 0b11001, 0b10000, 0b10000, 0b10000],
        "width": 5,
        "dropdown": False,
    },
    "s": {
        "bytes": [0b00000, 0b00000, 0b01111, 0b10000, 0b01110, 0b00001, 0b11110],
        "width": 5,
        "dropdown": False,
    },
    "t": {
        "bytes": [0b01000, 0b01000, 0b11100, 0b01000, 0b01000, 0b01001, 0b00110],
        "width": 5,
        "dropdown": False,
    },
    "u": {
        "bytes": [0b00000, 0b00000, 0b10001, 0b10001, 0b10001, 0b10011, 0b01101],
        "width": 5,
        "dropdown": False,
    },
    "v": {
        "bytes": [0b00000, 0b00000, 0b10001, 0b10001, 0b01010, 0b01010, 0b00100],
        "width": 5,
        "dropdown": False,
    },
    "w": {
        "bytes": [0b00000, 0b00000, 0b10001, 0b10001, 0b10101, 0b10101, 0b01010],
        "width": 5,
        "dropdown": False,
    },
    "x": {
        "bytes": [0b00000, 0b00000, 0b10001, 0b01010, 0b00100, 0b01010, 0b10001],
        "width": 5,
        "dropdown": False,
    },
    "y": {
        "bytes": [0b00000, 0b10001, 0b10001, 0b10001, 0b01111, 0b00001, 0b01110],
        "width": 5,
        "dropdown": False,
    },
    "z": {
        "bytes": [0b00000, 0b00000, 0b11111, 0b00010, 0b00100, 0b01000, 0b11111],
        "width": 5,
        "dropdown": False,
    },
    "A": {
        "bytes": [0b01110, 0b10001, 0b10001, 0b11111, 0b10001, 0b10001, 0b10001],
        "width": 5,
        "dropdown": False,
    },
    "B": {
        "bytes": [0b11110, 0b10001, 0b10001, 0b11110, 0b10001, 0b10001, 0b11110],
        "width": 5,
        "dropdown": False,
    },
    "C": {
        "bytes": [0b01110, 0b10001, 0b10000, 0b10000, 0b10000, 0b10001, 0b01110],
        "width": 5,
        "dropdown": False,
    },
    "D": {
        "bytes": [0b11110, 0b10001, 0b10001, 0b10001, 0b10001, 0b10001, 0b11110],
        "width": 5,
        "dropdown": False,
    },
    "E": {
        "bytes": [0b11111, 0b10000, 0b10000, 0b11110, 0b10000, 0b10000, 0b11111],
        "width": 5,
        "dropdown": False,
    },
    "F": {
        "bytes": [0b11111, 0b10000, 0b10000, 0b11110, 0b10000, 0b10000, 0b10000],
        "width": 5,
        "dropdown": False,
    },
    "G": {
        "bytes": [0b01110, 0b10001, 0b10000, 0b10011, 0b10001, 0b10001, 0b01110],
        "width": 5,
        "dropdown": False,
    },
    "H": {
        "bytes": [0b10001, 0b10001, 0b10001, 0b11111, 0b10001, 0b10001, 0b10001],
        "width": 5,
        "dropdown": False,
    },
    "I": {
        "bytes": [0b111, 0b010, 0b010, 0b010, 0b010, 0b010, 0b111],
        "width": 3,
        "dropdown": False,
    },
    "J": {
        "bytes": [0b00001, 0b00001, 0b00001, 0b00001, 0b00001, 0b10001, 0b01110],
        "width": 5,
        "dropdown": False,
    },
    "K": {
        "bytes": [0b10001, 0b10010, 0b10100, 0b11000, 0b10100, 0b10010, 0b10001],
        "width": 5,
        "dropdown": False,
    },
    "L": {
        "bytes": [0b10000, 0b10000, 0b10000, 0b10000, 0b10000, 0b10000, 0b11111],
        "width": 5,
        "dropdown": False,
    },
    "M": {
        "bytes": [0b10001, 0b11011, 0b10101, 0b10101, 0b10001, 0b10001, 0b10001],
        "width": 5,
        "dropdown": False,
    },
    "N": {
        "bytes": [0b10001, 0b10001, 0b11001, 0b10101, 0b10011, 0b10001, 0b10001],
        "width": 5,
        "dropdown": False,
    },
    "O": {
        "bytes": [0b01110, 0b10001, 0b10001, 0b10001, 0b10001, 0b10001, 0b01110],
        "width": 5,
        "dropdown": False,
    },
    "P": {
        "bytes": [0b11110, 0b10001, 0b10001, 0b11110, 0b10000, 0b10000, 0b10000],
        "width": 5,
        "dropdown": False,
    },
    "Q": {
        "bytes": [0b01110, 0b10001, 0b10001, 0b10001, 0b10101, 0b10010, 0b01101],
        "width": 5,
        "dropdown": False,
    },
    "R": {
        "bytes": [0b11110, 0b10001, 0b10001, 0b11110, 0b10100, 0b10010, 0b10001],
        "width": 5,
        "dropdown": False,
    },
    "S": {
        "bytes": [0b01110, 0b10001, 0b10000, 0b01110, 0b00001, 0b10001, 0b01110],
        "width": 5,
        "dropdown": False,
    },
    "T": {
        "bytes": [0b11111, 0b00100, 0b00100, 0b00100, 0b00100, 0b00100, 0b00100],
        "width": 5,
        "dropdown": False,
    },
    "U": {
        "bytes": [0b10001, 0b10001, 0b10001, 0b10001, 0b10001, 0b10001, 0b01110],
        "width": 5,
        "dropdown": False,
    },
    "V": {
        "bytes": [0b10001, 0b10001, 0b10001, 0b10001, 0b10001, 0b01010, 0b00100],
        "width": 5,
        "dropdown": False,
    },
    "W": {
        "bytes": [0b10001, 0b10001, 0b10001, 0b10101, 0b10101, 0b10101, 0b01010],
        "width": 5,
        "dropdown": False,
    },
    "X": {
        "bytes": [0b10001, 0b10001, 0b01010, 0b00100, 0b01010, 0b10001, 0b10001],
        "width": 5,
        "dropdown": False,
    },
    "Y": {
        "bytes": [0b10001, 0b10001, 0b10001, 0b01110, 0b00100, 0b00100, 0b00100],
        "width": 5,
        "dropdown": False,
    },
    "Z": {
        "bytes": [0b11111, 0b00001, 0b00010, 0b00100, 0b01000, 0b10000, 0b11111],
        "width": 5,
        "dropdown": False,
    },
    #
    # lowercase numbers
    #
    # "0": {
    #     "bytes": [0b00000, 0b01110, 0b10001, 0b10001, 0b10001, 0b10001, 0b01110],
    #     "width": 5,
    #     "dropdown": False,
    # },
    # "1": {
    #     "bytes": [0b00000, 0b00010, 0b00110, 0b00010, 0b00010, 0b00010, 0b01111],
    #     "width": 5,
    #     "dropdown": False,
    # },
    # "2": {
    #     "bytes": [0b00000, 0b01110, 0b10001, 0b00001, 0b00010, 0b00100, 0b11111],
    #     "width": 5,
    #     "dropdown": False,
    # },
    # "3": {
    #     "bytes": [0b00000, 0b01110, 0b10001, 0b00001, 0b00110, 0b00001, 0b11110],
    #     "width": 5,
    #     "dropdown": False,
    # },
    # "4": {
    #     "bytes": [0b00000, 0b00001, 0b00011, 0b00101, 0b01001, 0b01111, 0b00001],
    #     "width": 5,
    #     "dropdown": False,
    # },
    # "5": {
    #     "bytes": [0b00000, 0b11111, 0b10000, 0b11110, 0b00001, 0b00001, 0b11110],
    #     "width": 5,
    #     "dropdown": False,
    # },
    # "6": {
    #     "bytes": [0b00000, 0b01110, 0b10001, 0b10000, 0b11110, 0b10001, 0b01110],
    #     "width": 5,
    #     "dropdown": False,
    # },
    # "7": {
    #     "bytes": [0b00000, 0b11111, 0b00001, 0b00010, 0b00100, 0b01000, 0b10000],
    #     "width": 5,
    #     "dropdown": False,
    # },
    # "8": {
    #     "bytes": [0b00000, 0b01110, 0b10001, 0b01110, 0b10001, 0b10001, 0b01110],
    #     "width": 5,
    #     "dropdown": False,
    # },
    # "9": {
    #     "bytes": [0b00000, 0b01110, 0b10001, 0b10001, 0b01111, 0b00001, 0b01110],
    #     "width": 5,
    #     "dropdown": False,
    # },
    "0": {
        "bytes": [0b01110, 0b10001, 0b10001, 0b10001, 0b10001, 0b10001, 0b01110],
        "width": 5,
        "dropdown": False,
    },
    "1": {
        "bytes": [0b110, 0b010, 0b010, 0b010, 0b010, 0b010, 0b111],
        "width": 3,
        "dropdown": False,
    },
    "2": {
        "bytes": [0b11110, 0b00001, 0b00001, 0b00010, 0b00100, 0b01000, 0b11111],
        "width": 5,
        "dropdown": False,
    },
    "3": {
        "bytes": [0b11110, 0b00001, 0b00001, 0b00110, 0b00001, 0b00001, 0b11110],
        "width": 5,
        "dropdown": False,
    },
    "4": {
        "bytes": [0b10001, 0b10001, 0b10001, 0b11111, 0b00001, 0b00001, 0b00001],
        "width": 5,
        "dropdown": False,
    },
    "5": {
        "bytes": [0b11111, 0b10000, 0b10000, 0b11110, 0b00001, 0b00001, 0b11110],
        "width": 5,
        "dropdown": False,
    },
    "6": {
        "bytes": [0b01110, 0b10000, 0b10000, 0b11110, 0b10001, 0b10001, 0b01110],
        "width": 5,
        "dropdown": False,
    },
    "7": {
        "bytes": [0b11111, 0b00001, 0b00001, 0b00010, 0b00100, 0b01000, 0b10000],
        "width": 5,
        "dropdown": False,
    },
    "8": {
        "bytes": [0b01110, 0b10001, 0b10001, 0b01110, 0b10001, 0b10001, 0b01110],
        "width": 5,
        "dropdown": False,
    },
    "9": {
        "bytes": [0b01110, 0b10001, 0b10001, 0b01111, 0b00001, 0b00001, 0b01110],
        "width": 5,
        "dropdown": False,
    },
    ".": {
        "bytes": [0b00, 0b00, 0b00, 0b00, 0b00, 0b11, 0b11],
        "width": 2,
        "dropdown": False,
    },
    ",": {
        "bytes": [0b00, 0b00, 0b00, 0b00, 0b00, 0b01, 0b10],
        "width": 2,
        "dropdown": False,
    },
    '"': {
        "bytes": [0b00000, 0b00000, 0b10001, 0b10001, 0b01010, 0b01010, 0b00100],
        "width": 5,
        "dropdown": False,
    },
    "'": {
        "bytes": [0b00000, 0b00000, 0b00100, 0b00100, 0b01000, 0b00000, 0b00000],
        "width": 5,
        "dropdown": False,
    },
    "?": {
        "bytes": [0b01110, 0b10001, 0b00001, 0b00010, 0b00100, 0b00000, 0b00100],
        "width": 5,
        "dropdown": False,
    },
    "!": {
        "bytes": [0b00100, 0b00100, 0b00100, 0b00100, 0b00100, 0b00000, 0b00100],
        "width": 5,
        "dropdown": False,
    },
    "@": {
        "bytes": [0b01110, 0b10001, 0b10101, 0b10111, 0b10100, 0b10001, 0b01110],
        "width": 5,
        "dropdown": False,
    },
    "_": {
        "bytes": [0b00000, 0b00000, 0b00000, 0b00000, 0b00000, 0b00000, 0b11111],
        "width": 5,
        "dropdown": False,
    },
    "*": {
        "bytes": [0b00100, 0b10101, 0b01110, 0b10101, 0b00100, 0b00000, 0b00000],
        "width": 5,
        "dropdown": False,
    },
    "#": {
        "bytes": [0b01010, 0b01010, 0b11111, 0b01010, 0b11111, 0b01010, 0b01010],
        "width": 5,
        "dropdown": False,
    },
    "$": {
        "bytes": [0b00010, 0b01111, 0b10100, 0b01110, 0b00101, 0b11110, 0b00100],
        "width": 5,
        "dropdown": False,
    },
    "%": {
        "bytes": [0b11000, 0b11001, 0b00010, 0b00100, 0b01000, 0b10011, 0b00011],
        "width": 5,
        "dropdown": False,
    },
    "&": {
        "bytes": [0b00110, 0b01001, 0b01001, 0b00110, 0b10011, 0b10011, 0b01101],
        "width": 5,
        "dropdown": False,
    },
    "(": {
        "bytes": [0b00010, 0b00100, 0b01000, 0b01000, 0b01000, 0b00100, 0b00010],
        "width": 5,
        "dropdown": False,
    },
    ")": {
        "bytes": [0b01000, 0b00100, 0b00010, 0b00010, 0b00010, 0b00100, 0b01000],
        "width": 5,
        "dropdown": False,
    },
    "+": {
        "bytes": [0b00000, 0b00100, 0b00100, 0b11111, 0b00100, 0b00100, 0b00000],
        "width": 5,
        "dropdown": False,
    },
    "-": {
        "bytes": [0b00000, 0b00000, 0b00000, 0b11111, 0b00000, 0b00000, 0b00000],
        "width": 5,
        "dropdown": False,
    },
    "/": {
        "bytes": [0b00000, 0b00001, 0b00010, 0b00100, 0b01000, 0b10000, 0b00000],
        "width": 5,
        "dropdown": False,
    },
    ":": {
        "bytes": [0b00000, 0b00100, 0b00000, 0b00000, 0b00100, 0b00000, 0b00000],
        "width": 5,
        "dropdown": False,
    },
    ";": {
        "bytes": [0b00000, 0b00100, 0b00000, 0b00000, 0b00100, 0b00100, 0b00000],
        "width": 5,
        "dropdown": False,
    },
    "<": {
        "bytes": [0b00010, 0b00100, 0b01000, 0b10000, 0b01000, 0b00100, 0b00010],
        "width": 5,
        "dropdown": False,
    },
}

default_font = parse_raw_font(default_font_raw)
