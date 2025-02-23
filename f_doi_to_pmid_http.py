import requests
from bs4 import BeautifulSoup

def get_pmid_content(doi_in):
    try:
        # Send an HTTP GET request
        response = requests.get("https://pubmed.ncbi.nlm.nih.gov/?term="+doi_in)
        
        # Check if the request was successful
        if response.status_code == 200:
            # Parse the HTML content using BeautifulSoup
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Find the meta tag with name="citation_pmid"
            meta_tag = soup.find('meta', attrs={'name': 'citation_pmid'})
            meta_authors = soup.find('span',class_=['docsum-authors','full-authors'])
            
            # If the meta tag exists, return its content
            if meta_tag and meta_authors:
                return meta_tag.get('content'),meta_authors.text
            else:
                return "Meta tag 'citation_pmid' not found."
        else:
            return f"Failed to retrieve page. Status code: {response.status_code}"
            
    except Exception as e:
        return f"An error occurred: {str(e)}"
