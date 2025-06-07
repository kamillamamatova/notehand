# Handwritten Notes Generator

## Project Purpose:
Allow users to upload samples of their own handwritting (photos or scans) and instantly generate letters, notes, or any document in that exactly handwriting style, so the final output looks like genuine pen-on-paper with no extra manual effort.

This repository provides a pipeline to turn a scanned page of your own handwriting into a fully functional TrueType font, and then render arbitrary plain-text transcripts in your own handwriting style. The main stages are:

### 1. Segmentation (Crop your handwriting)
- Input: a 7×10 grid image (handwriting_template.jpg) where each box contains one handwritten character.
- Process: segment_glyphs.py crops that image into 70 individual binary PNGs (glyph_00.png … glyph_69.png).
- Output: segmentation/glyph_images/ with all the single-letter images.

### 2. Font Assembly (Build a .ttf from those images)
- Input: those 70 PNGs plus glyph_map.txt (which tells FontForge which PNG belongs to which Unicode codepoint).
- Process: build_font.py (a FontForge script) reads each glyph_XX.png, converts it into a vector outline, assigns it to the proper codepoint (A–Z, a–z, 0–9, punctuation), auto-hints, and sets side-bearings.
- Output: font_build/fonts/MyHandwriting.ttf, a TrueType font file that contains your actual handwriting as glyphs.

### 3. Rendering (Typeset any text in your handwriting)
- Input: your new MyHandwriting.ttf plus any plain-text file (like short.txt, medium.txt, long.txt).
- Process: render_handwritten_notes.py loads the TTF, reads the transcript, wraps lines, preserves paragraph breaks, and draws each character onto a blank page using Pillow.
- Output: PNG(s) or a multi-page PDF under rendering/output/ that looks like someone literally wrote the entire transcript by hand.

Putting those steps in order—“scan → crop → build font → render text”—constitutes our pipeline. Each step feeds its output into the next, until you end up with a fully handwritten-style document.

## CIRCLE Framework

To ensure we build the Handwritten Notes Generator in the right way, we follow the **CIRCLE** framework:

1. **Comprehend the situation**  
   We need to turn a plain‐text transcript into a lifelike reproduction of a user’s own handwriting, preserving stroke, slant, and spacing.

2. **Identify the customer**  
   - Students who want digital study notes that look handwritten  
   - Professionals sending personalized memos or letters  
   - Anyone seeking a bespoke “handwritten” touch for digital text

3. **Report customer needs**  
   - **Easy sample collection:** Upload a blank template filled with their handwriting  
   - **Accurate style capture:** Extract glyph shapes, margins, and stroke thickness  
   - **Flexible output:** Export as PNG or multi-page PDF  
   - **Privacy:** Samples and outputs processed locally or securely

4. **Cut through prioritization**  
   - **MVP:**  
     1. Segment glyphs → generate TTF “font”  
     2. Render transcript with that TTF → single-page PNG/PDF  
   - **Next:**  
     - Multi-page support  
     - User-friendly CLI/web UI  
   - **Later:**  
     - Stroke-variation (RNN/GAN) for natural jitter  
     - Extended symbols & languages

5. **List solutions**  
   - **Font-based:** Crop & import glyphs → TrueType font → typeset via Pillow/ReportLab  
   - **Stroke-synthesis:** Train an RNN to generate each stroke sequence on the fly  
   - **Hybrid:** Use font for base shapes + small random offsets per character

6. **Evaluate trade-offs**  

| Approach               | Accuracy | Speed     | Complexity | Privacy implications       |
|------------------------|:--------:|:---------:|:----------:|----------------------------|
| **Font-based**         | Medium   | Fast      | Low–Med    | Samples stored as PNG/TTF  |
| **Stroke-synthesis**   | High     | Slower    | High       | Requires raw stroke data   |
| **Hybrid**             | High     | Medium    | High       | Mix of both storage types  |

By following **CIRCLE**, we stay focused on the user’s real needs and deliver the core feature set in the right order.  


## Sample Transcripts

Located under rendering/transcripts/:

short.txt (~120 words; includes a long unbroken string)

medium.txt (~350 words; contains hyphens, blank lines, bullets)

long.txt (>800 words; multi-section, long strings, blank lines)

These are provided to test rendering as soon as Phase 2 is complete.

## Author & Credits
Created and maintained by Kamilla Mamatova and Diab Ali
If you found this helpful, feel free to star the repo and share!
