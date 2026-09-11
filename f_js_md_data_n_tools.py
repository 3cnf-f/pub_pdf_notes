"""Tiny helpers for building Silverbullet-flavoured Markdown.

Dependency-free string builders used by ``f_json_md`` when exporting the
annotation JSON to a Markdown file.
"""

import json

START_CODE_BLOCK = "\n```pdf_data\n"
END_CODE_BLOCK = "\n```\n"

#: Value used when a key is missing from the annotation data.
DEFAULT = "N/A"


def newlines(count=1):
    """Return ``count`` newline characters."""
    return "\n" * count


def key_value_line(data, key):
    """Format a single ``key: value`` line (falls back to :data:`DEFAULT`)."""
    return newlines() + f"{key}: {data.get(key, DEFAULT)}"


def value_or_default(data, key):
    """Return ``data[key]``, or :data:`DEFAULT` when missing/empty."""
    return str(data.get(key) or DEFAULT)


def heading(data, key, level=3):
    """Return a Markdown heading for ``data[key]`` at the given level."""
    return newlines() + "#" * level + " " + value_or_default(data, key)


def plain_heading(text, level=4):
    """Return a Markdown heading for literal ``text`` at the given level."""
    return newlines() + "#" * level + " " + text


def details(summary):
    """Open a collapsible ``<details>`` block with ``summary``."""
    return newlines() + f"<details><summary>{summary}</summary>" + newlines()


def end_details():
    """Close a collapsible ``<details>`` block."""
    return newlines() + "</details>\n"


def image_ref(path, width="", height=""):
    """Build a Markdown image reference with optional Silverbullet sizing."""
    size = ""
    if width or height:
        size = "|" + width + ("x" + height if height else "")
    return newlines() + f"![img]({path}{size})" + newlines()


def load_json(path):
    """Read a UTF-8 JSON file and return its contents."""
    with open(path, "r", encoding="utf-8") as infile:
        return json.load(infile)
