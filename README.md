# Paola Carvajal · Professional CV

Operations Strategy | Supply Chain Transformation | Program Leadership

[View the CV website](https://paocarvajal.github.io/Paola-Carvajal-CV/) · [Download the PDF](PCS%20CV.pdf)

Updated September 2026 from the latest owner-provided CV. The website and PDF share the repository's green and gray visual identity and use a personal contact address.

## Files

- `cv.json`: shared editorial source for experience, credentials and contact details.
- `index.html`: generated, accessible static website. All career content is present in HTML; expandable projects work without JavaScript.
- `assets/style.css`: responsive styles; no third-party runtime or fonts required.
- `PCS CV.pdf`: searchable three-page CV with embedded fonts, retaining the original download path.
- `scripts/build.py`: generates the website and PDF from `cv.json`.

## Update

Requires Python 3 and ReportLab (see `requirements.txt`).

```sh
python3 -m pip install -r requirements.txt
python3 scripts/build.py
python3 -m http.server 8000
```

Review the site at `http://localhost:8000` and visually inspect all three PDF pages before committing generated files. The PDF has deliberate page breaks; recheck pagination when expanding its content. GitHub Pages serves committed static files and does not need to run Python.

## Editorial conventions

- Preserve official job titles separately from project responsibilities.
- Keep modeled capacity opportunities distinct from achieved business results.
- Distinguish certifications, completed courses and education in progress.
- Maintain the existing PDF filename to preserve external links.
