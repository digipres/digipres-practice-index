import os
import re
import csv
import json
import argparse
import logging

logger = logging.getLogger(__name__)

INST_RE = re.compile("^(.*) \((.*)\)$")

from datetime import datetime
from typing import List, Optional, Set
from pydantic import BaseModel

class ConferenceResource(BaseModel):
    source_name: str
    source_url: str
    year: int
    title: str
    abstract: Optional[str] = None
    language: str
    creators: Optional[List[str]] = None
    institutions: List[str]
    license: Optional[str] = None
    size: Optional[int]
    type: str = 'paper'
    date: Optional[datetime] = None
    keywords: List[str] = []

def normalise_phaidra_jsonl(input_path):
    with open(input_path) as f:
        for line in f:
            doc = json.loads(line) 
            nd = ConferenceResource(
                source_name = doc['__source_name'],
                source_url = f"https://phaidra.univie.ac.at/{doc['pid']}",
                year = doc['__year'],
                title = doc['dc_title'][0],
                abstract = doc['dc_description'][0],
                phaidra_pid = doc['pid'],
                language = doc['dc_language'][0],
                content_type = doc.get('dc_format', [None])[0],
                creators = doc.get('dc_creator', None),
                institutions = set(),
                identifiers = doc['dc_identifier'],
                keywords = doc.get('keyword_suggest', [""])[0].split(","),
                license = doc['dc_license'][0],
                size = int(doc['size']),
            )
            # TBC: dc_license, dc_subject_eng, size, tcreated, tmodified, __source_col_id
            # Drop invalid/empty abstracts:
            if nd.abstract == 'x':
                nd.abstract = None
            # Catch how Lightning Talks are indicated:
            if nd.abstract == 'Lightning Talk':
                nd.type = 'lightning talk'
                nd.abstract = None
            # Distinguish posters based on title or phrase in abstract:
            if ": Poster " in nd.title or " (Poster) " in nd.title or \
                (nd.abstract and ("this poster" in nd.abstract.lower() \
                                     or "the poster" in nd.abstract.lower() \
                                        or "our poster" in nd.abstract.lower())):
                nd.type = "poster"
            # Shift institutions to separate field if present:
            creators = set()
            insts = set()
            if nd.creators == None:
                logger.error(f"No creator for {nd.title} -- dropping this record")
                continue
            else:
                for creator in nd.creators:
                    m = INST_RE.match(creator)
                    if m:
                        creators.add(m.group(1).strip())
                        insts.add(m.group(2).strip())
                    else:
                        creators.add(creator.strip())
            nd.creators = list(creators)
            nd.institutions = list(insts)
            yield nd

def normalise_eventsair_json(input_file):
    with open(input_file) as input:
        events = json.load(input)
    for item in events['AgendaData']['AgendaItems']:
        if len(item['Speakers']) > 0:
            for speaker in item['Speakers']:
                for doc in speaker['Documents']:
                    if doc['Name'] == 'Abstract':
                        abstract = doc['PlainText']
                    elif doc['Name'] == 'Keywords':
                        keywords = doc['PlainText'].split(", ")
                    elif doc['Name'] == 'Proposal Document':
                        source_url = doc['Url']
                d = ConferenceResource(
                    source_name='iPRES',
                    year=2022,
                    language='eng',
                    title=speaker['PresenationTitle'],
                    creators=[f"{speaker['LastName']}, {speaker['FirstName']}"],
                    institutions=[speaker['Organization']],
                    license="CC-By Attribution 4.0 International",
                    size=None,
                    source_url=source_url,
                    keywords=keywords,
                    abstract=abstract,
                    type='unknown',
                    )
                # Handle type:
                types = [ "Panel", "Tutorial", "Workshop", "Long Paper", "Short Paper", "Poster" ]
                for type in types:
                    if d.title.startswith(f"{type}: "):
                        d.type = type.lower()
                yield d

def normalise_ideals_jsonl(input_path):
    with open(input_path) as f:
        for line in f:
            doc = json.loads(line)
            # Have to know to reconstruct this (e.g. oai:www.ideals.illinois.edu:2142/121087) into a handle:
            handle_id = doc['oai_identifier'].split(":")[2]
            source_url = f"https://hdl.handle.net/{handle_id}"
            d = ConferenceResource(
                source_name = 'iPRES',
                source_url = source_url,
                year = '2023',
                title = doc['title'][0],
                abstract = doc.get('description',[None])[0],
                language = doc.get('language',['eng'])[0],
                creators = doc.get('creator',[]),
                institutions = [],
                keywords = doc['subject'],
                license="CC-By Attribution 4.0 International",
                #license = doc.get('rights',[None])[0], # Some variation in formatting, so hardcoding it instead.
                size = None,
                type = 'unknown',
            )
            if d.title.endswith(' [presentation]'):
                d.type = 'presentation'
            yield d

def common_cleanup(nd: ConferenceResource):
    # Drop keywords that are just default ones for the whole of iPRES, normalise to lower case:
    to_keep = []
    for keyword in nd.keywords:
        keyword = keyword.strip().lower()
        if keyword.startswith("conferences -- ipres conference "):
            continue
        if keyword == 'ipres' or keyword.startswith('ipres '):
            continue
        if keyword == "":
            continue
        # Otherwise, keep:
        to_keep.append(keyword)
    nd.keywords = to_keep
    # Standard three-character language code:
    if nd.language == 'en':
        nd.language = 'eng'
    # Return the modified item:
    return nd

def write_jsonl_to_csv(input_path, output_path):
    with open(input_path) as f:
        with open(output_path, 'w+') as outf:
            counter = 0
            writer = None
            for line in f:
                doc = json.loads(line)
                # If this is the first pass, set the writer up:
                if counter == 0:
                    writer = csv.DictWriter(outf, doc.keys())
                    writer.writeheader()
                # write the actual data:
                writer.writerow(doc)
                counter += 1

# Main for CLI
if __name__ == "__main__":
    # Set up a simpler argument parser:
    parser = argparse.ArgumentParser()
    parser.add_argument('input_dir')
    parser.add_argument('output_prefix')

    args = parser.parse_args()
    output_jsonl = args.output_prefix+".jsonl"
    output_csv = args.output_prefix+".csv"

    with open(output_jsonl, 'w') as outfile:
        for path in os.listdir(args.input_dir):
            input_file = os.path.join(args.input_dir, path)
            if input_file.endswith('.phaidra.jsonl'):
                input_reader = normalise_phaidra_jsonl
            elif input_file.endswith('.eventsair.json'):
                input_reader = normalise_eventsair_json
            elif input_file.endswith('ideals.jsonl'):
                input_reader = normalise_ideals_jsonl
            else:
                logger.warn(f"No code to handle {input_file}!")
                continue
            for d in input_reader(input_file):
                # Perform some common cleanup:
                d = common_cleanup(d)
                # Write to file
                outfile.write(f'{d.model_dump_json()}\n')
    # Also write as CSV:
    write_jsonl_to_csv(input_path=output_jsonl, output_path=output_csv)