"""Convert the annotation JSON produced by ``pdf2_pdf_t_json`` to Markdown.

The output is Silverbullet-flavoured Markdown: a collapsible metadata block
followed by one section per annotation.
"""

import f_js_md_data_n_tools as md


def _iter_annotations(data):
    """Yield annotation dicts from either the ``blocks`` list or ``ANNOT#-N`` keys."""
    if "blocks" in data:
        yield from data["blocks"]
        return
    for key, value in data.items():
        if key.startswith("ANNOT#-"):
            yield value


def fold_controls():
    """Return the Silverbullet fold-all/unfold-all controls."""
    return md.newlines() + "{[Outline: Fold All]}    {[Outline: Unfold All]}"


def metadata_block(data):
    """Render the document-level metadata as a collapsible code block."""
    lines = [md.START_CODE_BLOCK]
    for key in (
        "title", "journal", "main_authors", "abstract", "pubmed_url",
        "date", "volume", "issue", "DOI", "pmid", "file_uuid4",
        "file_datetime_stockholm", "filename", "issn",
    ):
        lines.append(md.key_value_line(data, key))
    lines.append(md.newlines() + md.END_CODE_BLOCK + md.newlines(2))
    return "".join(lines)


def annotation_block(entry, base_url=""):
    """Render a single annotation entry as a Markdown section."""
    kind = entry.get("entry_type")
    if kind == "blue_ink":
        heading = md.plain_heading(f"Handwriting p:{entry.get('page_no')}", level=3)
    elif kind in ("non_blue_ink", "rectangle"):
        heading = md.plain_heading(f"Pen annotation p:{entry.get('page_no')}", level=3)
    else:
        heading = md.plain_heading(f"highlight p:{entry.get('page_no')}", level=3)

    out = [heading]

    image = entry.get("img_filename") or ""
    if image:
        out.append(md.image_ref(base_url + image))

    highlighted = entry.get("highlighted_text") or ""
    if highlighted:
        out.append(md.newlines() + "#### hlt > >" + md.newlines())
        out.append(highlighted + "\n")

    note = entry.get("annotation_text") or ""
    if note:
        out.append(md.newlines() + "#### ant > >" + md.newlines())
        out.append("* " + note + "\n")

    return "".join(out)


def json_to_markdown(json_path, md_path, base_url=""):
    """Write a Markdown export of the annotation JSON at ``json_path``.

    ``base_url`` (optional) is prepended to image references; include a
    trailing slash, e.g. ``"http://host/static/"``.
    """
    data = md.load_json(json_path)
    with open(md_path, "w", encoding="utf-8") as outfile:
        outfile.write(md.heading(data, "title", level=3))
        outfile.write(md.heading(data, "main_author", level=3) + "   -   ")
        outfile.write(md.value_or_default(data, "date"))
        outfile.write(md.heading(data, "journal", level=3))
        outfile.write(fold_controls())
        outfile.write(metadata_block(data))
        for entry in _iter_annotations(data):
            outfile.write(annotation_block(entry, base_url))


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 3:
        raise SystemExit("usage: python f_json_md.py <input.json> <output.md> [base_url]")
    base_url = sys.argv[3] if len(sys.argv) > 3 else ""
    json_to_markdown(sys.argv[1], sys.argv[2], base_url)
