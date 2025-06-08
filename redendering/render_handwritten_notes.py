# rendering/render_handwritten_notes.py

import argparse
import os
import textwrap
from PIL import Image, ImageDraw, ImageFont

# --- Configuration ---
# Page and Font settings, as suggested in the project plan 
FONT_PATH = "font_build/MyHandwriting.ttf"
PAGE_WIDTH_PX = 2550  # 8.5 inches * 300 DPI
PAGE_HEIGHT_PX = 3300 # 11 inches * 300 DPI
MARGIN_PX = 150       # 0.5 inch margin * 300 DPI
FONT_SIZE = 90
LINE_SPACING = 30

# --- Main Script ---

def render_transcript(transcript_path, output_path):
    """
    Renders a text transcript to an image file using the custom handwriting font.
    """
    # 1. Validate inputs
    if not os.path.exists(FONT_PATH):
        print(f"ERROR: Font file not found at '{FONT_PATH}'.")
        print("Please run the build_font.py script first.")
        return

    if not os.path.exists(transcript_path):
        print(f"ERROR: Transcript file not found at '{transcript_path}'.")
        return

    # 2. Load the transcript content
    with open(transcript_path, "r") as f:
        text_content = f.read()

    # 3. Set up the canvas (the page)
    # Create a new blank white image
    img = Image.new('RGB', (PAGE_WIDTH_PX, PAGE_HEIGHT_PX), 'white')
    draw = ImageDraw.Draw(img)

    # Load the custom handwriting font
    try:
        font = ImageFont.truetype(FONT_PATH, FONT_SIZE)
    except IOError:
        print(f"ERROR: Could not load font. Ensure '{FONT_PATH}' is a valid .ttf file.")
        return

    # 4. Wrap text to fit the page width 
    # The textwrap library calculates where to break lines.
    char_width, _ = font.getbbox("a")[2:] # Get approximate width of a character
    chars_per_line = (PAGE_WIDTH_PX - 2 * MARGIN_PX) // char_width
    wrapped_text = textwrap.fill(text_content, width=chars_per_line)

    # 5. Draw the text onto the image
    # We start drawing at the top margin.
    y_position = MARGIN_PX
    draw.text(
        (MARGIN_PX, y_position),
        wrapped_text,
        font=font,
        fill="black",
        spacing=LINE_SPACING
    )

    # 6. Save the final image 
    # Ensure output directory exists
    output_dir = os.path.dirname(output_path)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)
    
    img.save(output_path)
    print(f"Successfully rendered transcript to '{output_path}'")


if __name__ == "__main__":
    # Set up command-line argument parsing as specified in the project plan example 
    parser = argparse.ArgumentParser(
        description="Render a text transcript into a handwritten-style PNG."
    )
    parser.add_argument(
        "transcript_path",
        type=str,
        help="Path to the input transcript .txt file."
    )
    parser.add_argument(
        "-o", "--output",
        dest="output_path",
        type=str,
        required=True,
        help="Path to save the output .png image."
    )

    args = parser.parse_args()
    render_transcript(args.transcript_path, args.output_path)