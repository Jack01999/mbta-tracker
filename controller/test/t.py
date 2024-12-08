from PIL import Image, ImageDraw, ImageFont


def render_text_with_ttf(font_path, text, font_size=7):
    """Render text using a .ttf font."""
    # Load the font
    font = ImageFont.truetype(font_path, font_size)

    # Calculate the size of the rendered text
    width, height = font.getbbox(text)[
        2:
    ]  # Extract width and height from the bounding box

    # Create an image canvas
    image = Image.new("1", (width, height), color=0)  # Black background
    draw = ImageDraw.Draw(image)

    # Render the text onto the canvas
    draw.text((0, 0), text, font=font, fill=1)  # White text

    # Print the bitmap to the terminal
    for y in range(height):
        row = ""
        for x in range(width):
            row += "#" if image.getpixel((x, y)) else " "
        print(row)


# Path to your .ttf font file
ttf_font_path = "controller/fonts/5x7_practical.ttf"

# Text to render
text_to_render = "Hello"

# Render and display the text
render_text_with_ttf(ttf_font_path, text_to_render, font_size=7)
