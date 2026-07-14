# ADUC public website

Static source for the ADUC Working Draft public site.

Canonical public URL: https://bacoul.github.io/AI-Data-Understanding-Core-ADUC/

The site intentionally separates:

- available Core artifacts;
- active deterministic complete-Core formatting work;
- planned compiler, review UI, registry, MCP adapter, packages and extensions;
- not-yet-proven external multi-consumer evidence.

Run:

```bash
python -m unittest discover -s tests/website -p "test_*.py"
python tools/validate_website.py
```
