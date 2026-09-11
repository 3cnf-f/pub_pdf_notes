"""End-to-end pipeline: PDF -> JSON / Markdown / notebook + images + zip.

The library entry point is :func:`convert_pdf`; run the module directly for a
command-line interface.
"""

import json
import os
from shutil import copy, make_archive

import f_json_ipynb as ipynb
import f_json_md as markdown
import pdf2_pdf_t_json as exporter


def convert_pdf(pdf_path, export_markdown=False, export_notebook=True, make_zip=True):
    """Process ``pdf_path`` into a per-PDF folder of outputs.

    Creates ``<name>/`` containing a copy of the source PDF, the annotation
    JSON, extracted images, and (optionally) Markdown/notebook exports plus a
    zip archive. Returns the path of the written JSON file.
    """
    name = os.path.splitext(os.path.basename(pdf_path))[0]
    os.makedirs(name, exist_ok=True)

    json_path = os.path.join(name, name + ".json")
    md_path = os.path.join(name, name + ".md")
    ipynb_path = os.path.join(name, name + ".ipynb")

    data = exporter.process_pdf(pdf_path, name)

    with open(json_path, "w", encoding="utf-8") as outfile:
        json.dump(data, outfile, indent=4)

    if export_markdown:
        markdown.json_to_markdown(json_path, md_path)
    if export_notebook:
        ipynb.json_to_notebook(json_path, ipynb_path)

    copy(pdf_path, os.path.join(name, name + ".pdf"))
    if make_zip:
        make_archive(name, "zip", name + "/")

    return json_path


def main(argv=None):
    """Command-line entry point: ``convert_pdf`` for the first argument."""
    import sys

    argv = argv if argv is not None else sys.argv[1:]
    if not argv:
        print("usage: python f_pdf_notes_main.py <input.pdf>")
        return 1
    convert_pdf(argv[0])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
