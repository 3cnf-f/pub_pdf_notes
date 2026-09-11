"""Command-line entry point: `python main.py <input.pdf>`."""

import f_pdf_notes_main


def main(argv=None):
    """Run the PDF export pipeline for ``argv[0]``."""
    import sys

    argv = argv if argv is not None else sys.argv[1:]
    if not argv:
        print("usage: python main.py <input.pdf>")
        return 1
    f_pdf_notes_main.convert_pdf(argv[0])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
