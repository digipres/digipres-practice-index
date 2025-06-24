import os
import re
import csv
import sys
import json
import argparse
import logging
from .models import Publication

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

INST_RE = re.compile("^(.*) \((.*)\)$")
TITLE_END_1_RE = re.compile(r"(:|-) (iPres|iPRES|iPES) \d{4} (: |- |– |)[a-zA-Z, ]+$")
TITLE_END_2_RE = re.compile(r"(:|-) ([a-zA-Z ]+) (:|-) (iPres|iPRES) \d{4} (:|-) [a-zA-Z, ]+$")
DEFAULT_LICENSE = "CC-BY 4.0 International"

# Normalised data item generators:
    
def normalise_phaidra_jsonl(input_path):
    with open(input_path) as f:
        for line in f:
            doc = json.loads(line) 
            nd = Publication(
                source_name = doc['__source_name'],
                landing_page_url = f"https://phaidra.univie.ac.at/{doc['pid']}",
                document_url = f"https://services.phaidra.univie.ac.at/api/object/{doc['pid']}/download",
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
            # Clean up titles, using any useful metadata in the title:
            m = TITLE_END_2_RE.search(nd.title)
            logger.debug(f"Processing PHAIDRA article \"{nd.title}\"...")
            if m:
                nd.type = m.group(2).lower()
                nd.title = TITLE_END_2_RE.sub("", nd.title)
            nd.title = TITLE_END_1_RE.sub("", nd.title)
            # Shift institutions to separate field if present:
            creators = list()
            insts = list()
            if nd.creators == None:
                logger.error(f"No creator for {nd.title} -- dropping this record")
                continue
            else:
                for creator in nd.creators:
                    m = INST_RE.match(creator)
                    if m:
                        creator = m.group(1).strip()
                        # Don't duplicate but retain order:
                        inst = m.group(2).strip()
                        if inst not in insts:
                            insts.append(inst)
                    else:
                        creator = creator.strip()
                    creator = uncomma_name(creator)
                    creators.append(creator)
            nd.creators = creators
            nd.institutions = insts
            yield nd

def normalise_eventsair_json(input_file):
    # Some strings to strip from title:
    to_remove = ['Short Paper: ', 'Long Paper: ', 'Workshop: ', 'Panel: ', 'Poster: ', 'Tutorial: ', 'TUTORIAL: ']
    # Read the file:
    with open(input_file) as input:
        events = json.load(input)
    counter = 0
    for item in events['AgendaData']['AgendaItems']:
        if len(item['Speakers']) > 0:
            # Reset fields so they don't get copied:
            abstract = None
            keywords = []
            source_url = None
            for speaker in item['Speakers']:
                for doc in speaker['Documents']:
                    if doc['Name'] == 'Abstract':
                        abstract = doc['PlainText']
                    elif doc['Name'] == 'Keywords':
                        keywords = doc['PlainText'].split(", ")
                    elif doc['Name'] == 'Proposal Document':
                        source_url = doc['Url']
                # Tidy the title:
                title = speaker['PresenationTitle'] # Mis-spelling is required!
                for rem in to_remove:
                    title = title.replace(rem,"")
                # Create the pub
                counter += 1
                d = Publication(
                    source_name=f'iPRES:ea2022:{counter}',
                    year=2022,
                    language='eng',
                    title=title, 
                    creators=[f"{speaker['FirstName']} {speaker['LastName']}"],
                    institutions=[speaker['Organization']],
                    license=DEFAULT_LICENSE,
                    size=None,
                    document_url=source_url,
                    keywords=keywords,
                    abstract=abstract,
                    type='unknown',
                    )
                # Handle type:
                types = [ "Panel", "Tutorial", "Workshop", "Long Paper", "Short Paper", "Poster" ]
                for type in types:
                    if speaker['PresenationTitle'].startswith(f"{type}: "):
                        d.type = type.lower()
                yield d

def get_ipres2022_mapping(zotero_path):
    # Read in the mapping file:
    mapping = {}
    mapping_path = zotero_path.replace(".zotero.jsonl", ".eventsair-osf-mapping.csv")
    mapping_reader = csv.DictReader(open(mapping_path))
    for row in mapping_reader:
        mapping[row['ea_id']] = row['osf_id']
    # Read in the EventsAir items:
    ea = {}
    ea_path = zotero_path.replace(".zotero.jsonl", ".eventsair.json")
    for d in normalise_eventsair_json(ea_path):
        osf_id = mapping[d.source_name]
        ea[osf_id] = d
    # And return
    return ea


def normalise_zotero_jsonl(input_path):
    # Store publications under their key:
    pubs = {}
    # Store attachments separately:
    attachments = []
    # Type is stored under this key:
    type_key = 'publication_type'
    # Loop through Zotero items:
    with open(input_path) as f:
        for line in f:
            item = json.loads(line)
            data = item['data']
            if data['itemType'] == 'attachment':
                attachments.append(data)
            else:
                # Copy the type key into the data block:
                data[type_key] = item[type_key]
                pubs[data['key']] = data
    # Assign attachments to publications:
    for att in attachments:
        parent_key = att['parentItem']
        item_attachments = pubs[parent_key].get('attachments', [])
        item_attachments.append(att)
        pubs[parent_key]['attachments'] = item_attachments

    # Now go get the EventsAir data, keyed on OSF ID
    ea = get_ipres2022_mapping(input_path)

    # Now loop through assembled items
    for key, data in pubs.items():
        # Grab attachment link:
        landing_page = None
        document_url = None
        slides_url = None
        notes_url = None
        stream_url = None
        osf_id = None
        for att in data['attachments']:
            if 'osf_id' in att:
                osf_id = att['osf_id']
                landing_page = att['landing_page']
                for osf_file in att['osf_files']['data']:
                    title = osf_file['attributes']['name']
                    if title.startswith('iPres22_Biography_') or title.startswith('iPres22_Holding-Slide'):
                        logger.info(f"Skipping OSF File: {title}")
                    elif title.startswith('iPres22_Abstract_') or re.search("iPres22_.. Transcript_", title) or title.startswith('iPres22_Posters_') or title.startswith('iPres22_Video-Transcript_') or title.startswith('iPres22_Memo_'):
                        logger.warning(f"Skipping OSF File: {title} <<< Should do something with this!?")
                    elif title.startswith('iPres22_Slides_') or title.startswith('iPres22_LightningTalk_') or title.startswith('iPres22_Poster_'):
                        slides_url = osf_file['links']['download']
                    elif title.startswith('iPres22_Collaborative-Notes'):
                        notes_url = osf_file['links']['download']
                    elif title.startswith('iPres22_Long-Paper_') or title.startswith('iPres22_Short-Paper_') or title.startswith('iPres22_Panel_') or title.startswith('iPres22_Tutorial_') or title.startswith('iPres22_Workshop_') or title.startswith('iPres22_Poster-Proposal_'):
                        document_url = osf_file['links']['download']
                    elif title.startswith('iPres22_Recording_') or title.startswith('iPres22_Poster-Video_'):
                        stream_url = osf_file['links']['download']
                    else:
                        logger.fatal(f"Unknown OSF File attachment! :: {json.dumps(osf_file)}")
                        sys.exit(42) # The Answer
        # Convert list of creators:
        creators = []
        for creator in data['creators']:
            creators.append(f"{creator['firstName']} {creator['lastName']}")
        # Extract the YouTube stream URL from the abstract (if needed?):
        if not stream_url and "Recording: " in data['abstractNote']:
            r = re.compile(r"Recording: ([^ ]+)", re.MULTILINE)
            m = r.search(data['abstractNote'])
            stream_url = m.group(1)
        # Construct the item:
        d = Publication(
            source_name = f'iPRES:osf:{osf_id}',
            landing_page_url = landing_page,
            document_url=document_url,
            slides_url=slides_url,
            notes_url=notes_url,
            stream_url=stream_url,
            year = "2022",
            title = data['title'][:-9],
            abstract = data['abstractNote'],
            language = data['language'],
            creators = creators,
            institutions = [],
            keywords = [],
            license= data.get('rights', DEFAULT_LICENSE),
            size = None,
            type = data[type_key].lower(),
        )
        # Enrich with EventsAir data if possible:
        if d.source_name in ea:
            ead = ea[d.source_name]
            d.abstract = ead.abstract
            d.institutions = ead.institutions
            d.keywords = ead.keywords
            d.license = ead.license
        else:
            # Wipe defaults that are not being overridden via Zotero:
            if "Recording: " in d.abstract:
                d.abstract = None
            if not d.license:
                d.license = DEFAULT_LICENSE
        # And return:
        yield d

def canon_title(title):
    # map title strings to a 'canonical' form to compensate for minor variations
    canon = title.lower()
    canon = canon.replace("  ", " ")
    return canon

def normalise_ideals_jsonl(input_path):
    # Normalise and separate:
    papers = {}
    presentations = []
    presentation_marker = ' [presentation]'
    with open(input_path) as f:
        for line in f:
            doc = json.loads(line)
            creators = []
            for creator in doc.get('creator',[]):
                creators.append(uncomma_name(creator))
            d = Publication(
                source_name = 'iPRES',
                landing_page_url = doc['source_url'],
                document_url=doc['pdf_url'],
                year = '2023',
                title = doc['title'][0],
                abstract = doc.get('description',[None])[0],
                language = doc.get('language',['eng'])[0],
                creators = creators,
                institutions = [],
                keywords = doc['subject'],
                license=DEFAULT_LICENSE,
                #license = doc.get('rights',[None])[0], # Some variation in formatting, so hardcoding it instead.
                size = None,
                type = 'paper',
            )
            if d.title.endswith(presentation_marker):
                d.type = 'presentation'
                d.title = d.title[:-len(presentation_marker)]
                presentations.append(d)
            else:
                canon = canon_title(d.title)
                if canon in papers:
                    raise Exception(f"Duplicate title for {d}!")
                else:
                    papers[canon] = d
    
    # Merge presentations
    for p in presentations:
        canon = canon_title(p.title)
        print(f"'{p.title}' > {canon}")
        if canon in papers:
            papers[canon].slides_url = p.landing_page_url
        else:
            # This is just a presentation, so keep it as-is:
            papers[canon] = p
        
    # Output papers:
    for canon in papers:
        yield papers[canon]

def normalise_ghent_csv(input_file):
    with open(input_file, encoding='utf-8-sig') as csv_file:
        reader = csv.DictReader(csv_file)
        for item in reader:
            # Skip non-publications:
            if not item['Authors']:
                continue
            # Otherwise:
            # First set up the document_url, using the Poster or PubPub PDF if available:
            document_url = None
            if item['PosterImageLocation']:
                document_url = item['PosterImageLocation']
            elif item['PublicationLocation']:
                document_url = item['PublicationLocation']
                if "ipres2024.pubpub.org" in document_url:
                    if document_url.endswith('/'):
                        document_url += "download/pdf"
                    else:
                        document_url += "/download/pdf"
            d = Publication(
                source_name='iPRES',
                year=2024,
                language='eng',
                title=item['Title'],
                creators=[x.strip() for x in item['Authors'].split(',')],
                institutions=[],
                license=item['License'],
                size=None,
                document_url=document_url,
                landing_page_url=item['PublicationLocation'],
                slides_url=item['PresentationMaterials'],
                stream_url=item['SessionVideoLocation'],
                notes_url=item['CollaborativeNotesLocation'],
                keywords=[ item['CompetencyFrameworkBestMatch'], item['ConferenceTheme'] ],
                abstract=item['Abstract_MARKDOWN'],
                type=item['AcceptedFormat'].lower(),
                date=f"{item['PresentationDate']}T{item['PresentationStart']}:00+01:00",
                )
            yield d

def uncomma_name(name):
    if ',' in name:
        surname, fornames = name.split(",", maxsplit=1)
        return f"{fornames.strip()} {surname.strip()}"
    else:
        return name.strip()

# Helper to perfom some standard cleanup:
def common_cleanup(nd: Publication):
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

# Helper to generate a CSV version of the data:
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
            # Get the full input path:
            input_file = os.path.join(args.input_dir, path)
            logger.info(f"Reading {input_file}...")

            # Choose which reader to use:
            if input_file.endswith('.phaidra.jsonl'):
                input_reader = normalise_phaidra_jsonl
            elif input_file.endswith('.eventsair.json'):
                #input_reader = normalise_eventsair_json
                logger.info(f"Skipping {input_file} as this is handled elsewhere...")
                continue
            elif input_file.endswith('.zotero.jsonl'):
                input_reader = normalise_zotero_jsonl
            elif input_file.endswith('ideals.jsonl'):
                input_reader = normalise_ideals_jsonl
            elif input_file.endswith('ghent.csv'):
                input_reader = normalise_ghent_csv
            else:
                logger.warning(f"No code to handle {input_file}!")
                continue

            # Use the supplied generator to parse the file into records:
            for d in input_reader(input_file):
                # Perform some common cleanup:
                d = common_cleanup(d)
                # Write to file
                outfile.write(f'{d.model_dump_json()}\n')

    # Also write as CSV:
    write_jsonl_to_csv(input_path=output_jsonl, output_path=output_csv)