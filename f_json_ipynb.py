"""Convert the annotation JSON produced by ``pdf2_pdf_t_json`` to an ``.ipynb``.

Each annotation becomes a Markdown cell carrying its text and metadata, so the
notebook can be opened and edited in Jupyter.
"""

import json

import nbformat as nbf


def _pick(data, keys, default="N/A"):
    """Return ``{key: data.get(key, default)}`` for each key in ``keys``."""
    return {key: data.get(key, default) for key in keys}


def _annotation_cell(entry):
    """Build a Markdown cell for one annotation."""
    keys = [
        "annot_uuid4", "page_no", "img_filename", "highlighted_text",
        "annotation_text", "rect", "file_uuid4", "entry_type", "DOI",
        "title", "document_type", "course", "main_author", "date",
    ]
    meta = _pick(entry, keys)
    source = [
        f"p:({meta['page_no']})\n",
        f"![{meta['img_filename']}]({meta['img_filename']})\n",
        f"#### {meta['annotation_text']}\n",
    ]
    return nbf.v4.new_markdown_cell(source=source, metadata=meta)


def _header_cell(data):
    """Build the document header cell (journal article or handout)."""
    keys = [
        "date", "DOI", "title", "main_author", "journal", "abstract",
        "pubmed_url", "file_uuid4", "filename", "file_datetime_stockholm",
        "pmid", "main_authors", "volume", "issue", "issn", "course",
        "document_type",
    ]
    meta = _pick(data, keys)
    if meta["document_type"] == "journal_article":
        source = [
            f"## {meta['title']}\n",
            f"#### {meta['main_author']}  -   {meta['journal']}  -   {meta['date']}\n",
            f"[DOI: {meta['DOI']}]({meta['pubmed_url']})\n",
            "##### Abstract: \n",
            f"{meta['abstract']}\n",
        ]
    else:
        source = [
            f"## {meta['title']}\n",
            f"#### Document type: {meta['document_type']}\n",
            f"#### Course: {meta['course']}\n",
            f"#### {meta['main_author']}  -   {meta['date']}\n",
        ]
    return nbf.v4.new_markdown_cell(source=source, metadata=meta)


def notebook_from_json(data):
    """Build a notebook object from annotation JSON."""
    notebook = nbf.v4.new_notebook()
    notebook.cells.append(_header_cell(data))
    for key, value in data.items():
        if key.startswith("ANNOT#-"):
            notebook.cells.append(_annotation_cell(value))
    return notebook


def json_to_notebook(json_path, ipynb_path):
    """Read annotation JSON and write a notebook to ``ipynb_path``."""
    with open(json_path, "r", encoding="utf-8") as infile:
        data = json.load(infile)
    nbf.write(notebook_from_json(data), ipynb_path)


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 3:
        raise SystemExit("usage: python f_json_ipynb.py <input.json> <output.ipynb>")
    json_to_notebook(sys.argv[1], sys.argv[2])
