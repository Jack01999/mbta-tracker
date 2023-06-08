from datamodels.types import Character, Font

# TODO store a map rather than searching for each letter
def key_to_character(
    font: Font,
    key: str,
) -> Character:
    for character in font.characters:
        if character.character_key == key:
            return character
    raise ValueError