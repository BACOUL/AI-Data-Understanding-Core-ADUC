# ADUC public website

Static, dependency-free public website for the ADUC Working Draft.

Canonical public URL: https://bacoul.github.io/AI-Data-Understanding-Core-ADUC/

The generator centralizes navigation, metadata and repeated project facts:

```bash
python website/build_site.py
python tools/validate_website.py
python -m unittest discover -s tests/website -p "test_*.py"
```

Visual release evidence must cover 360×800, 390×844, 768×1024, 1024×768, 1440×900 and 1920×1080 before a redesign PR may be merged.
