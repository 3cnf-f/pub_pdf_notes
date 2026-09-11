"""Blue-ink (handwriting) annotation detection."""

#: RGB value used by the PDF reader for "blue" ink.
BLUE_RGB = (0.0, 0.0, 1.0)


def is_blue_ink(annot):
    """Return ``True`` when the annotation's stroke colour is blue."""
    stroke = (annot.colors or {}).get("stroke")
    return stroke == list(BLUE_RGB)
