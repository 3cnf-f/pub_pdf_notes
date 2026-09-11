"""Export a PDF's annotations (highlights, boxes, ink) to a JSON dict.

The result mixes document-level metadata (DOI, PubMed citation, file uuid,
timestamp) with one ``ANNOT#-N`` entry per annotation. Each annotation carries
its highlighted text, popup note, bounding rect and a rendered PNG snapshot
written into ``img_folder``.
"""

import os
import uuid

import fitz

import f_blue_ink as blue_ink
import f_metapub as metapub
import f_pdf_tools as tools

#: Write rendered PNG snapshots to disk.
SAVE_IMAGES = True
#: Print per-annotation progress/contents while processing.
VERBOSE = False

_ZOOM = 4.0      # pixmap scale factor (4x default resolution)
_PAD = 20        # vertical context padding around a highlight

# PyMuPDF annotation type ids.
HIGHLIGHT = 8
SQUARE = 4
INK = 15

#: Metadata fields copied from PubMed into the output document block.
_META_FIELDS = [
    "pmid", "title", "main_authors", "main_author", "journal", "abstract",
    "volume", "issue", "pubmed_url", "issn", "date",
]


def _render_image(page, rect, img_folder, img_counter, pdf_path):
    """Render the region ``rect`` to a PNG and return its filename."""
    pixmap = page.get_pixmap(matrix=fitz.Matrix(_ZOOM, _ZOOM), clip=rect)
    stem = os.path.splitext(os.path.basename(pdf_path))[0]
    img_name = f"{stem}-img{img_counter}.png"
    if SAVE_IMAGES:
        pixmap.save(os.path.join(img_folder, img_name))
    return img_name


def _highlight_rect(page, annot):
    """Expand a highlight's rect vertically to include surrounding context."""
    rect = annot.rect
    top = max(int(rect.y0 - _PAD), 0)
    bottom = min(int(rect.y1 + _PAD), int(page.rect.y1))
    return fitz.Rect(0, top, page.rect.x1, bottom)


def extract_annotation(annot, page, img_folder, img_counter, pdf_path):
    """Extract text, note and an image for a single annotation.

    Returns ``(img_name, highlighted_text, note_text)``.
    """
    if annot.type[0] == HIGHLIGHT:
        text_rect = annot.rect
        img_rect = _highlight_rect(page, annot)
    else:
        text_rect = img_rect = annot.rect

    highlighted_text = tools.words_in_rect(page, text_rect)
    note_text = tools.annotation_note(annot)
    img_name = _render_image(page, img_rect, img_folder, img_counter, pdf_path)

    if VERBOSE:
        print(highlighted_text)
    return img_name, highlighted_text, note_text


def _document_metadata(doi, meta):
    """Build the document-level metadata block (journal article or handout)."""
    meta = meta or {}
    doc_meta = {field: str(meta.get(field) or "N/A") for field in _META_FIELDS}
    doc_meta["course"] = str(meta.get("course") or "N/A")
    if doi:
        doc_meta["document_type"] = "journal_article"
        doc_meta["DOI"] = doi
    else:
        doc_meta["document_type"] = "handout"
        doc_meta["DOI"] = "N/A"
    return doc_meta


def _annotation_entry(annot, page, page_no, img_counter, pdf_path, img_folder, parent, doi):
    """Build the per-annotation dict for a single annotation."""
    if annot.type[0] == HIGHLIGHT:
        entry_type = "highlight"
    elif annot.type[0] == SQUARE:
        entry_type = "rectangle"
    else:  # INK
        entry_type = "blue_ink" if blue_ink.is_blue_ink(annot) else "non_blue_ink"

    img_name, highlighted_text, note_text = extract_annotation(
        annot, page, img_folder, img_counter, pdf_path
    )

    return {
        "entry_type": entry_type,
        "annot_uuid4": str(uuid.uuid4()),
        "page_no": page_no,
        "img_filename": img_name,
        "highlighted_text": highlighted_text,
        "annotation_text": note_text,
        "rect": str(annot.rect),
        "file_uuid4": parent["file_uuid4"],
        "DOI": doi,
        "main_author": parent.get("main_author"),
        "date": parent.get("date"),
        "title": parent.get("title"),
        "course": parent.get("course"),
    }


def process_pdf(pdf_path, img_folder):
    """Extract all annotations from ``pdf_path`` into a JSON-friendly dict.

    Images are written into ``img_folder`` (created by the caller if needed).
    """
    doc = tools.open_pdf(pdf_path)

    doi = tools.find_doi(doc[0])
    if doi:
        meta = metapub.fetch_metadata(doi=doi)
    else:
        meta = tools.metadata_from_annotations(doc[0])

    parent = {
        "file_uuid4": str(uuid.uuid4()),
        "filename": pdf_path,
        "file_datetime_stockholm": tools.stockholm_timestamp(),
    }
    parent.update(_document_metadata(doi, meta))

    if VERBOSE and doi:
        print("DOI on page 0:", doi)

    img_counter = 1
    for page_no, page in enumerate(doc):
        for annot in page.annots() or []:
            if annot.type[0] not in (HIGHLIGHT, SQUARE, INK):
                continue
            entry = _annotation_entry(
                annot, page, page_no, img_counter, pdf_path, img_folder, parent, doi
            )
            parent[f"ANNOT#-{img_counter}"] = entry
            img_counter += 1

    doc.close()
    return parent
