# This script assumes that there is a scanned image of a fixed grid template
# It will slice the grid into individual character images (one file per glyph)

import cv2 # Used to load images, split into sub-images, binarize, etc.
import os # Used to create the output folder, and build file paths

# Configuration
NUM_ROWS = 7
NUM_COLS = 10
MARGIN = 5 # To not accidently crop a letter

# Loads the scanned template
template_path = "segmentation/handwritten_template.jpg"
img = cv2.imread(template_path, cv2.IMREAD_GRAYSCALE)
if img is None:
    raise FileNotFoundError(f"Could not load {template_path}")

height, width = img.shape

# Computes the height/width of each cell
cell_width = width // NUM_COLS
cell_height = height // NUM_ROWS

# Creates output folder if it doesn't exist
output_folder = "glyph_images" # Each cropped letter will be saved here
os.makedirs(output_folder, exist_ok = True)

# Loops over columns/rows to crop each glyph
glyph_index = 0
for row in range(NUM_ROWS):
    for col in range(NUM_COLS):
        x1 = col * cell_width + MARGIN
        y1 = row * cell_height + MARGIN
        x2 = (col + 1) * cell_width + MARGIN
        y2 = (row + 1) * cell_height + MARGIN

        glyph = img[y1:y2, x1:x2] # row_start:row_end, col_start:col_end

        # Threshold to isolate pen strockes (binarize)
        # Any pixel > 200 is "ink"
        # glyph_bin is a 2D array of 0s and 255s, no grays
        _, glyph_bin = cv2.threshold(glyph, 200, 255, cv2.THRESH_BINARY_INV) # Per pixel test
        
        # Saves each glyph as its own PNG
        out_path = os.path.join(output_folder, f"glyph_{glyph_index:02d}.png") # Produces glyphs like glyph_00.png, ...
        cv2.imwrite(out_path, glyph_bin)

        glyph_index += 1 # Next loop writes glyph_01.png, then glyph_02.png, and so on

print(f"Saved {glyph_index} glyphs to '{output_folder}")