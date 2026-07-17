# Resume Parsing Evaluation Report

## Overview
This report evaluates the resume parser across multiple PDF formats to measure text extraction quality, reading order, and failure cases.

## Evaluation Table

| Resume Type | Status | Issue | Solution | Notes |
|---|---|---|---|---|
| ATS Resume | ✅ | None | Good | Clean linear extraction, no artifacts, sections in proper order. |
| Modern Resume | ⚠️ | Bullet encoding | Text cleaning | Bullet characters extracted as `(cid:127)` glyph errors instead of `•`. |
| Two Column | ⚠️ | Layout mixing | Layout detection | Sidebar and main column text interleaved out of order. |
| Scanned Resume | ❌ | OCR needed | Tesseract OCR | Complete extraction failure because there is no text layer. |
| Sample Resume | ✅ | Sparse content | Acceptable | Clean extraction, but content is very minimal. |

## Key Findings
- The parser works well on ATS-friendly resumes.
- Decorative layouts reduce extraction quality.
- Scanned PDFs require OCR.
- Text cleaning is needed to remove unwanted bullet glyphs.

## Conclusion
The parser is effective for standard PDFs but still needs OCR and layout handling improvements for real-world resumes.