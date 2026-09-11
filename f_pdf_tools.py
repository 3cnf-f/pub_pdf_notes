"""PDF text and DOI/metadata helpers.

Small utilities shared by the PDF exporter, all built on PyMuPDF (``fitz``).
"""

import re
from datetime import datetime
from zoneinfo import ZoneInfo

import fitz

#: Maps annotation-tag markers to the metadata field they populate.
TAG_NAMES = {
    "#_title": "title",
    "#_t": "title",
    "#_author": "main_author",
    "#_a": "main_author",
    "#_date": "date",
    "#_d": "date",
    "#_course": "course",
    "#_c": "course",
}

_TAG_RE = re.compile(
    r"#_(?P<tag>title|author|date|course|t|a|d|c)"
    r"\s*\(\s*(?P<args>[\w\s_-]*?)\s*\)"
)

#: DOI preceded by a typical marker ("doi:", "doi.org", "Published online").
_DOI_RE = re.compile(
    r"(?:Published online|https?://(?:dx\.)?doi\.org/|doi:)\s*/?\s*"
    r"(?P<doi>10\.\d{4,}(?:/[\w.\-]+)+)",
    re.IGNORECASE,
)


def open_pdf(path):
    """Open a PDF and return the PyMuPDF document."""
    return fitz.open(path)


def page_text(pdf, page_no=0):
    """Return the plain text of page ``page_no``."""
    return pdf.load_page(page_no).get_text("text", sort=True)


def page_text_dict(pdf, page_no=0):
    """Return the structured text of page ``page_no`` as a dict."""
    return pdf.load_page(page_no).get_text("dict", sort=True)


def words_in_rect(page, rect):
    """Join the words on ``page`` whose bounding boxes touch ``rect``."""
    return " ".join(
        w[4] for w in page.get_text("words") if fitz.Rect(w[:4]).intersects(rect)
    )


def annotation_note(annot):
    """Return an annotation's popup text, collapsed to a single line."""
    return annot.info.get("content", "No note").replace("\n", " ").replace("\r", " ")


def extract_doi_from_text(text):
    """Return the first DOI found in ``text``, else ``None``."""
    match = _DOI_RE.search(text)
    return match.group("doi") if match else None


def find_doi(page):
    """Locate the DOI on ``page`` (normally the first page of the PDF)."""
    for token in page.get_text().split():
        doi = extract_doi_from_text(token)
        if doi:
            return doi
    for block in page.get_textpage().extractBLOCKS():
        if block[-1] == 0:  # text block
            doi = extract_doi_from_text(block[-3])
            if doi:
                return doi
    return None


def stockholm_timestamp():
    """Return the current Europe/Berlin time as ``YYYY-MM-DD HH:MM:SS``."""
    return datetime.now(ZoneInfo("Europe/Berlin")).strftime("%Y-%m-%d %H:%M:%S")


def parse_annotation_tag(note):
    """Parse ``#_tag(args)`` markers from an annotation note.

    Returns a list of ``(tag, args)`` tuples.
    """
    return _TAG_RE.findall(note)


def tag_value(args, highlighted):
    """Resolve a tag argument: ``hl``/empty means "use the highlighted text"."""
    return highlighted if args in ("hl", "") else args


def metadata_from_annotations(page):
    """Build a ``{title, main_author, date, course}`` dict from tagged highlights.

    Highlights whose note contains ``#_title(...)`` / ``#_author(...)`` /
    ``#_date(...)`` / ``#_course(...)`` markers are treated as document
    metadata (used for PDFs without a DOI, e.g. handouts).
    """
    meta = {"main_author": None, "date": None, "title": None, "course": None}
    for annot in page.annots() or []:
        if annot.type[0] != 8:  # only highlights
            continue
        highlighted = words_in_rect(page, annot.rect)
        for tag, args in parse_annotation_tag(annotation_note(annot)):
            field = TAG_NAMES.get("#_" + tag)
            if field is not None:
                meta[field] = tag_value(args.strip(), highlighted)
    return meta
