# Handwritten Notes Generator

**Turn any transcript into “your” handwriting**—no manual tracing required.  
Built with Python, OpenCV, FontForge & Pillow.

---

## Project Framework: CIRCLE

We applied the CIRCLE framework to deliver a polished MVP and roadmap:

1. **Comprehend**  
   Translate plain-text into lifelike handwriting, preserving stroke & slant.  
2. **Identify**  
   Users: students, professionals, anyone wanting digital notes that feel personal.  
3. **Report**  
   Needs: easy sample upload, accurate style capture, flexible PNG/PDF export, privacy.  
4. **Cut**  
   **MVP**: segmentation → font → single-page render  
   **Next**: multi-page, web UI  
   **Later**: stroke-variation RNN, extended symbols  
5. **List**  
   - Font-based (fast, predictable)  
   - Stroke-synthesis (natural, complex)  
   - Hybrid  
6. **Evaluate**  

| Approach             | Accuracy | Speed   | Complexity | Privacy          |
|----------------------|:--------:|:-------:|:----------:|------------------|
| **Font-based**       | Medium   | Fast    | Low–Med    | Local PNG/TTF    |
| **Stroke-synthesis** | High     | Slower  | High       | Raw stroke data  |
| **Hybrid**           | High     | Medium  | High       | Mixed            |

---

## 🚀 Pipeline & Key Achievements

1. **Segmentation**  
   • Cropped a 7×10 grid into 70 binary PNGs via OpenCV—reduced manual effort from hours to seconds.  
2. **Font Assembly**  
   • Automated glyph import into a TrueType font with FontForge; delivered MyHandwriting.ttf.  
3. **Rendering**  
   • Typeset any transcript into PNG/PDF with Pillow; preserved line breaks & margins.  

---

## 📂 Sample Transcripts  

Ready for Phase 3 testing—short (120 w), medium (350 w), long (925 w) with edge cases.  

```bash
ls rendering/transcripts/
# short.txt  medium.txt  long.txt

##Tech Stack

- Languages: Python
- CV: OpenCV
- Font: FontForge (Python API)
- Rendering: Pillow, ReportLab
- Future: Flask web UI, Docker

## How to Run

1. **Segment:**
    ```bash
    cd segmentation
    python3 segment_glyphs.py
2. **Build font:**
    ```bash
    cd ../font_build
    fontforge -script build_font.py
3. **Render**
    ```bash
    cd ../rendering
    python3 render_handwritten_notes.py transcripts/short.txt

## Authors and Credits
Created and maintained by Kamilla Mamatova and Diab Ali If you found this helpful, feel free to star the repo and share!