"""DOI -> PubMed id (pmid) lookup via PubMed's web interface.

This is a standalone utility; the main pipeline resolves metadata directly
through ``f_metapub``. Use ``lookup_pmid`` when all you need is the pmid.
"""

import requests
from bs4 import BeautifulSoup

PUBMED_URL = "https://pubmed.ncbi.nlm.nih.gov/"


def lookup_pmid(doi):
    """Return the pmid for ``doi``, or a descriptive error message string."""
    try:
        response = requests.get(PUBMED_URL + "?term=" + doi)
    except Exception as exc:  # noqa: BLE001 - surface network errors as text
        return f"An error occurred: {exc}"

    if response.status_code != 200:
        return f"Failed to retrieve page. Status code: {response.status_code}"

    soup = BeautifulSoup(response.text, "html.parser")
    meta_tag = soup.find("meta", attrs={"name": "citation_pmid"})
    if meta_tag is None:
        return "Meta tag 'citation_pmid' not found."
    return meta_tag.get("content")
