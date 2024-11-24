def parse_bdf(filename):
    with open(filename, "r") as f:
        lines = f.readlines()

    chars = []
    idx = 0
    while idx < len(lines):
        line = lines[idx].strip()
        if line.startswith("STARTCHAR"):
            char_data = {}
            char_name = line.split(" ", 1)[1]
            char_data["name"] = char_name
            idx += 1
            while not lines[idx].strip().startswith("ENDCHAR"):
                line = lines[idx].strip()
                if line.startswith("ENCODING"):
                    char_data["encoding"] = int(line.split(" ", 1)[1])
                elif line.startswith("BBX"):
                    bbx_parts = line.split(" ")
                    char_data["bbx"] = {
                        "width": int(bbx_parts[1]),
                        "height": int(bbx_parts[2]),
                        "xoffset": int(bbx_parts[3]),
                        "yoffset": int(bbx_parts[4]),
                    }
                elif line == "BITMAP":
                    idx += 1
                    bitmap_lines = []
                    while lines[idx].strip() != "ENDCHAR":
                        bitmap_line = lines[idx].strip()
                        if bitmap_line != "":
                            bitmap_lines.append(bitmap_line)
                        idx += 1
                    char_data["bitmap"] = bitmap_lines
                    break
                idx += 1
            chars.append(char_data)
        idx += 1
    return chars


def render_char(char_data):
    width = char_data["bbx"]["width"]
    height = char_data["bbx"]["height"]
    x_offset = char_data["bbx"]["xoffset"]
    y_offset = char_data["bbx"]["yoffset"]
    bitmap = char_data["bitmap"]

    # Initialize the canvas with empty pixels
    canvas_height = height + abs(y_offset)
    canvas = [" " * width for _ in range(canvas_height)]

    # Adjust for y_offset
    if y_offset < 0:
        start_row = -y_offset
    else:
        start_row = 0

    # Process the bitmap lines
    for i, hex_line in enumerate(bitmap):
        bin_line = bin(int(hex_line, 16))[2:].zfill(8)

        # Adjust for x_offset
        if x_offset < 0:
            bin_line = bin_line[-x_offset:].ljust(8, "0")
        elif x_offset > 0:
            bin_line = bin_line[:-x_offset].rjust(8, "0")

        # Extract the leftmost 'width' bits
        bits = bin_line[:width]

        line = ""
        for b in bits:
            line += "#" if b == "1" else " "
        canvas[start_row + i] = line

    # Trim the canvas to the actual character height
    rendered_lines = canvas[:height]

    # Print the character
    return rendered_lines


# if __name__ == '__main__':
#     main()
def main():
    # Replace 'font.bdf' with the path to your BDF font file
    chars = parse_bdf(
        "/Users/bradleyspillert/Documents/GitHub/mbta-tracker/controller/fonts/5x7.bdf"
    )
    for char_data in chars:
        print("Character:", char_data["name"])
        rendered = render_char(char_data)
        for line in rendered:
            print(line)
        print()


if __name__ == "__main__":
    main()
