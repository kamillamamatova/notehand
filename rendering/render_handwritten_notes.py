# rendering/render_handwritten_notes.py

import argparse
import os
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# Configuration
# Page and font settings
FONT_PATH = os.path.join(os.path.dirname(__file__), '..', 'font_build', 'MyHandwriting.ttf')
FONT_NAME = "MyHandwriting"
FONT_SIZE = 14
LINE_HEIGHT = 18
MARGIN_INCH = 0.75

# Main script

def render_transcript_to_pdf(transcript_path, output_path):
    """
    Renders a text transcript to a PDF file using the custom handwriting font
    """
    # Validate inputs
    if not os.path.exists(FONT_PATH):
        print(f"ERROR: Font file not found at '{FONT_PATH}'.")
        print("Please run the font_build/build_font.py script first.")
        return

    if not os.path.exists(transcript_path):
        print(f"ERROR: Transcript file not found at '{transcript_path}'.")
        return

    # Load the transcript content
    with open(transcript_path, "r", encoding = "utf-8") as f:
        text_content = f.read()

    # Set up the page
    page_width, page_height = letter
    margin_px = MARGIN_INCH * 72 # Inches to points
    c = canvas.Canvas(output_path, pagesize = letter)

    # Load the custom handwriting font
    try:
        pdfmetrics.registerFont(TTFont(FONT_NAME, FONT_PATH))
        c.setFont(FONT_NAME, FONT_SIZE)
    except Exception as e:
        print(f"ERROR: Could not load font. Ensure '{FONT_PATH}' is a valid .ttf file.")
        print(f"ReportLab Error: {e}")
        return

    # Draw the text onto the PDF
    # We start drawing at the top margin
    text = c.beginText(margin_px, page_height - margin_px)
    text.setFont(FONT_NAME, FONT_SIZE, leading = LINE_HEIGHT)

    # Processes lines to preserve paragraphs
    lines = text_content.split('\n')
    for line in lines:
        # Handles wrapping long lines automatically
        text.textLine(line)

    c.drawText(text)

    # 6. Save the PDF file 
    c.save()

    # Ensures the output directory exists
    output_dir = os.path.dirname(output_path)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)
    
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
        help="Path to save the output .pdf file."
    )

    args = parser.parse_args()
    render_transcript_to_pdf(args.transcript_path, args.output_path)