import logging
import requests
import lxml.html

logger = logging.getLogger(__name__)

# Helper function to get PDF URLs:
def download_and_extract_pdf_url(url):
    try:
        # Download the web page
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for bad responses

        # Parse the HTML content using lxml
        root = lxml.html.fromstring(response.content)

        # Find the meta tag with name 'citation_pdf_url'
        pdf_url_tag = root.xpath('//meta[@name="citation_pdf_url"]')

        if pdf_url_tag:
            # Extract the content attribute value
            pdf_url = pdf_url_tag[0].get('content')
            return pdf_url
        else:
            logger.warn("No citation_pdf_url metadata tag found.")
            return None

    except Exception as e:
        logger.error(f"Error: {e}")
        return None