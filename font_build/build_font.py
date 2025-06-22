import fontforge
import os

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__), os.pardir)

# Configuration
GLYPH_MAP_PATH = os.path.join(PROJECT_ROOT, "segmentation", "glyph_map.txt")
GLYPH_IMAGES_DIR = os.path.join(PROJECT_ROOT, "segmentation", "glyph_images/")
OUTPUT_FONT_PATH = os.path.join(PROJECT_ROOT, "font_build", "MyHandwriting.ttf")
FONT_NAME = "MyHandwriting"
FONT_FAMILY = "My Handwriting"
FONT_WEIGHT = "Regular"

# Create a new, empty font
font = fontforge.font()
font.fontname = FONT_NAME
font.familyname = FONT_FAMILY
font.fullname = FONT_NAME
font.weight = FONT_WEIGHT

print(f"Created new font: {FONT_NAME}")

# Read the glyph map to associate images with characters
try:
    with open(GLYPH_MAP_PATH, "r") as f:
        glyph_mappings = f.readlines()
except FileNotFoundError:
    print(f"ERROR: Glyph map not found at '{GLYPH_MAP_PATH}'")
    exit(1)

# Process each glyph in the map
for mapping in glyph_mappings:
    mapping = mapping.strip()
    if not mapping:
        continue

    try:
        image_file, codepoint_str, char = mapping.split(maxsplit=2)
        codepoint = int(codepoint_str.replace("U+", ""), 16)
        image_path = os.path.join(GLYPH_IMAGES_DIR, image_file)

        # Create a new glyph in the font at the specified Unicode codepoint
        glyph = font.createChar(codepoint)

        # Import the corresponding PNG image into the glyph slot
        glyph.importOutlines(image_path)

        # Clean up the imported glyph
        glyph.simplify()
        glyph.correctDirection()
        glyph.removeOverlap()

        # Set side-bearings (spacing around the character)
        glyph.left_side_bearing = 20
        glyph.right_side_bearing = 20
        
        print(f"Processed: {image_file} -> {char} (U+{codepoint:04X})")

    except Exception as e:
        print(f"Skipping invalid line or error processing '{mapping}': {e}")


# Generate the final TTF font file
print(f"\nGenerating font file at '{OUTPUT_FONT_PATH}'...")
font.generate(OUTPUT_FONT_PATH)
print("Font generation complete!")