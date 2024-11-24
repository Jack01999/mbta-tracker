from PIL import Image, ImageDraw

def parse_bdf(file_path):
    """Manually parses a BDF font file and extracts character data."""
    characters = {}
    bounding_box = None
    current_char = None
    bitmap = []
    width = height = x_offset = y_offset = 0
    recording = False

    with open(file_path, "r") as file:
        for line in file:
            line = line.strip()

            if line.startswith("FONTBOUNDINGBOX"):
                _, width, height, x_offset, y_offset = line.split()
                bounding_box = (int(width), int(height), int(x_offset), int(y_offset))

            if line.startswith("STARTCHAR"):
                current_char = None
                bitmap = []
                recording = False

            if line.startswith("ENCODING"):
                current_char = int(line.split()[1])

            if line.startswith("BBX"):
                _, width, height, x_offset, y_offset = line.split()
                width = int(width)
                height = int(height)

            if line == "BITMAP":
                recording = True
                bitmap = []
                continue

            if recording:
                if line == "ENDCHAR":
                    characters[current_char] = {
                        "bitmap": bitmap,
                        "width": width,
                        "height": height,
                    }
                    current_char = None
                    bitmap = []
                    recording = False
                else:
                    bitmap.append(line)

    return characters, bounding_box


def render_glyph_as_image(glyph_data, bounding_box):
    """Render a glyph bitmap as a PIL image."""
    width, height = glyph_data["width"], glyph_data["height"]
    bitmap = glyph_data["bitmap"]
    image = Image.new("1", (bounding_box[0], bounding_box[1]), color=0)  # Black background
    draw = ImageDraw.Draw(image)

    y_offset = bounding_box[1] - height  # Align the glyph to the bottom of the bounding box
    for y, row in enumerate(bitmap):
        row_data = int(row, 16)  # Convert hex string to integer
        for x in range(width):
            if (row_data >> (width - 1 - x)) & 1:  # Check each bit in the row
                draw.point((x, y + y_offset), fill=1)  # White pixel

    return image


def display_font(file_path):
    """Load and display each character in the BDF font file."""
    characters, bounding_box = parse_bdf(file_path)

    for char_code, glyph_data in characters.items():
        char = chr(char_code) if 32 <= char_code < 127 else f"U+{char_code:04X}"
        print(f"Displaying character: {repr(char)}")
        image = render_glyph_as_image(glyph_data, bounding_box)
        image = image.resize(
            (bounding_box[0] * 10, bounding_box[1] * 10), Image.NEAREST
        )  # Scale up for visibility
        image.show()


# Path to your BDF font file
bdf_font_path = "/Users/bradleyspillert/Documents/GitHub/mbta-tracker/controller/fonts/6x10.bdf"
display_font(bdf_font_path)