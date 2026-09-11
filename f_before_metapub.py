"""Optional NCBI API-key check.

The default metadata path in ``f_metapub`` scrapes PubMed HTML and needs no
key. Export ``NCBI_API_KEY`` only if you switch to the keyed E-utilities API.
"""

import os


def ensure_api_key():
    """Raise ``SystemExit`` unless ``NCBI_API_KEY`` is present in the env."""
    if "NCBI_API_KEY" not in os.environ:
        raise SystemExit("Please export the NCBI_API_KEY environment variable.")
