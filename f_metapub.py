"""Fetch bibliographic metadata for a DOI from PubMed's HTML.

``fetch_metadata`` parses the citation ``<meta>`` tags that PubMed embeds in a
paper page and returns them as a flat dict. Scraping needs no API key, which
keeps setup simple; ``f_before_metapub`` documents the optional keyed path.
"""

import requests
from bs4 import BeautifulSoup

PUBMED_URL = "https://pubmed.ncbi.nlm.nih.gov/"

#: Maps our output keys to PubMed ``citation_*`` meta tag names.
_CITATION_FIELDS = {
    "pmid": "citation_pmid",
    "title": "citation_title",
    "main_authors": "citation_authors",
    "journal": "citation_publisher",
    "journal_longname": "citation_journal_title",
    "volume": "citation_volume",
    "issue": "citation_issue",
    "date": "citation_date",
    "pubmed_url": "citation_abstract_html_url",
    "issn": "citation_issn",
}


def _meta_content(soup, name):
    """Return the ``content`` attribute of a named meta tag, or ``""``."""
    tag = soup.find("meta", attrs={"name": name})
    return tag.get("content", "") if tag else ""


def _parse_abstract(soup):
    """Extract and flatten the abstract text block."""
    block = soup.find("div", class_=["abstract-content"], id="eng-abstract")
    if block is None:
        return ""
    return block.get_text().replace("\n", "").replace("   ", "")


def _parse_html(html_text):
    """Parse a PubMed page into a flat metadata dict."""
    soup = BeautifulSoup(html_text, "html.parser")
    data = {
        key: _meta_content(soup, meta_name)
        for key, meta_name in _CITATION_FIELDS.items()
    }
    data["abstract"] = _parse_abstract(soup)
    data["main_author"] = data["main_authors"].split(";")[0].strip()
    return data


def fetch_metadata(doi="", html_file=""):
    """Return citation metadata for a DOI (HTTP) or a local HTML file.

    Exactly one of ``doi`` / ``html_file`` should be supplied. Returns ``None``
    when neither is, and ``{}`` when a DOI lookup fails (a non-200 response).
    """
    if doi and not html_file:
        response = requests.get(PUBMED_URL + "?term=doi:" + doi)
        if response.status_code != 200:
            return {}
        return _parse_html(response.text)
    if html_file and not doi:
        with open(html_file, "r", encoding="utf-8") as infile:
            return _parse_html(infile.read())
    return None
