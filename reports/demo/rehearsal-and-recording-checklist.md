# Actual rehearsal and recording

scripts/release/record_demo.py ran an empty-state browser rehearsal with assertions for collection,
7127.78/128 rows, source proof, alternate-date 14255.20, duplicate no-op and safe session failure.
Actual captured screenshots and timing: presentation/recording/. Narration: planning/pitch/narration.txt.
MP4: presentation/demo.mp4, H.264 video/AAC audio, approximately 130.6 seconds, 1440×900.
Voiceover uses offline macOS synthetic speech; captions identify the local synthetic recording.

The HTML deck was rendered by scripts/release/render_slides.cjs into ten PNGs and a PDF, then
scripts/release/build_slides.py --pptx embedded the rendered slides and speaker notes into PowerPoint.
Verification covers navigation, exactly one visible slide, content bounds, notes and browser errors.
Slides 1/3/5/6/9 were visually inspected after a CSS class collision was repaired.

Human rehearsal on the actual event screen and organizer upload are still pending.
The PPTX has raster slide images plus editable speaker notes; HTML is the editable source deck.
