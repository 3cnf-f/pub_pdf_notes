# pdf_notes

Extract annotations (highlights, boxes, ink) from a PDF into a structured
JSON file, with optional Markdown and Jupyter-notebook exports. The pipeline
resolves a paper's DOI and pulls its citation metadata from PubMed, or falls
back to metadata written as tags in the PDF for documents without a DOI
(handouts, book chapters).

## Install

```sh
pip install PyMuPDF nbformat requests beautifulsoup4 tzdata
```

No API key is required: metadata is scraped from PubMed's HTML. (The
keyed E-utilities path is optional; see `f_before_metapub.py`.)

## Usage

Command line:

```sh
python main.py path/to/paper.pdf
# or, equivalently:
python f_pdf_notes_main.py path/to/paper.pdf
```

This creates a folder named after the PDF:

```
paper/
├── paper.pdf            # copy of the source
├── paper.json           # all annotations + metadata
├── paper-img1.png       # rendered annotation snapshots
├── paper-img2.png
├── paper.ipynb          # notebook export
└── paper.zip            # archive of the folder
```

As a library:

```python
import f_pdf_notes_main

f_pdf_notes_main.convert_pdf(
    "paper.pdf",
    export_markdown=True,   # also write paper.md
    export_notebook=True,   # also write paper.ipynb
    make_zip=True,
)
```

### Converting an existing JSON file

The individual converters can be run directly on a JSON file produced by the
pipeline:

```sh
python f_json_md.py paper.json paper.md            # optional base_url arg
python f_json_ipynb.py paper.json paper.ipynb
```

## Intended workflow

1. **PDF → flat metafile.** Each PDF is processed into a single flat JSON
   file. Every annotation carries the unique id (`file_uuid4`) of its parent
   PDF.
2. **Versioned.** The flat metafile is small and text-only, so it version
   controls cleanly.
3. **Aggregation.** Because each annotation references its PDF's uuid, the
   per-PDF files can later be merged into one or two databases: one for
   documents, one for annotations.
4. **Human-readable folder names.** For long-term storage, rename the output
   folder to include the first author, topic and year, e.g.:

   ```
   smith_NMOSD_2015_260520/
   └── Smith_NMOSD_2015_260520.pdf
   ```

## JSON schema

The top-level object mixes document metadata with annotation entries:

```jsonc
{
  "file_uuid4": "…",                  // unique id for this PDF
  "filename": "paper.pdf",
  "file_datetime_stockholm": "…",
  "document_type": "journal_article",  // or "handout"
  "DOI": "10.1148/…",
  "pmid": "…", "title": "…", "main_author": "…",
  "journal": "…", "abstract": "…", "pubmed_url": "…",
  // …
  "ANNOT#-1": {
    "entry_type": "highlight",         // highlight | rectangle | blue_ink | non_blue_ink
    "annot_uuid4": "…",
    "page_no": 0,
    "highlighted_text": "…",
    "annotation_text": "…",            // popup note
    "img_filename": "paper-img1.png",
    "rect": "Rect(…)"
  }
}
```

## Annotation tags for PDFs without a DOI

For handouts or book chapters there is no DOI to look up. Instead, annotate
the first page with highlights whose note contains `#_tag(...)` markers. The
value in parentheses becomes the metadata field; `hl` (or empty) means "use
the highlighted text itself".

| Tag | Field | Example |
|---|---|---|
| `#_title(...)` | title | `#_title(hl)` |
| `#_author(...)` | main_author | `#_author(Smith)` |
| `#_date(...)` | date | `#_date(2015)` |
| `#_course(...)` | course | `#_course(Neuro 101)` |

Short forms `#_t`, `#_a`, `#_d`, `#_c` are accepted too.

## Modules

| File | Purpose |
|---|---|
| `main.py` / `f_pdf_notes_main.py` | entry points / pipeline |
| `pdf2_pdf_t_json.py` | PDF → annotation JSON + images |
| `f_pdf_tools.py` | DOI regex, text/metadata helpers |
| `f_metapub.py` | PubMed citation metadata |
| `f_doi_to_pmid_http.py` | DOI → pmid utility |
| `f_json_md.py` | JSON → Markdown |
| `f_json_ipynb.py` | JSON → notebook |
| `f_js_md_data_n_tools.py` | Markdown string helpers |
| `f_blue_ink.py` | blue-ink detection |
| `f_before_metapub.py` | optional NCBI key check |
