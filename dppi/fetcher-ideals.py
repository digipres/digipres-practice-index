import sys
import json
from sickle import Sickle
import requests
import lxml.html
import logging
import argparse

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

sickle = Sickle('https://www.ideals.illinois.edu/oai-pmh')

# This function was used to work out what the right metadata set ID was:
def list_all_sets(sickle):
    sets = sickle.ListSets()
    for s in sets:
        print(s)


# This gets the records for a set and outputs them
def write_set_to_file(oai_set, output_file):
    logger.info(f"Listing the records for collection {oai_set}...")
    recs = sickle.ListRecords(metadataPrefix="oai_dc", set=oai_set)
    logger.info(f"Writing records to {output_file}...")
    with open(output_file, 'w') as f:
        for r in recs:
            doc = r.get_metadata()
            doc['oai_identifier'] = r.header.identifier
            # Have to know to reconstruct this (e.g. oai:www.ideals.illinois.edu:2142/121087) into a handle:
            handle_id = doc['oai_identifier'].split(":")[2]
            source_url = f"https://hdl.handle.net/{handle_id}"
            # De-reference and parse for citation_pdf_url:
            logger.info(f"Getting {source_url}...")
            response = requests.get(source_url, allow_redirects=True)
            response.raise_for_status()  # Raise an exception for bad responses
            tree = lxml.html.fromstring(response.text)
            pdf_url = tree.xpath('/html/head/meta[@name="citation_pdf_url"]')[0].attrib['content']
            # Store additional data:
            doc['source_url'] = source_url
            doc['pdf_url'] = pdf_url
            # Send to file:
            f.write(json.dumps(doc))
            f.write('\n')



if __name__ == "__main__":
    # Set up a simpler argument parser:
    parser = argparse.ArgumentParser()
    parser.add_argument('output_jsonl')

    args = parser.parse_args()

    # This gets the records for the iPRES 2023 metadata set:
    write_set_to_file("com_2142_120947", args.output_jsonl)