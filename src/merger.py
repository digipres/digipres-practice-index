import os
import re
import csv
import json
import argparse
import logging

logger = logging.getLogger(__name__)

INST_RE = re.compile("^(.*) \((.*)\)$")


def normalise_phaidra_jsonl(input_path, outfile):
    with open(input_path) as f:
        for line in f:
            doc = json.loads(line) 
            nd = {
                'source_name' :doc['__source_name'],
                'source_url': f"https://phaidra.univie.ac.at/{doc['pid']}",
                'year': doc['__year'],
                'title': doc['dc_title'][0],
                'abstract' : doc['dc_description'][0],
                'phaidra_pid': doc['pid'],
                'language': doc['dc_language'][0],
                'content_type': doc.get('dc_format', [None])[0],
                'creators': doc.get('dc_creator', None),
                'institutions' : set(),
                'identifiers': doc['dc_identifier'],
                'keywords': doc.get('keyword_suggest', [""])[0].split(","),
                'license': doc['dc_license'][0],
                'size': int(doc['size']),
                'type': 'paper',
                #'roles': json.loads(doc['uwm_roles_json'][0]), # This field doesn't seem to have anything unique in it.
            }
            # TBC: dc_license, dc_subject_eng, size, tcreated, tmodified, __source_col_id
            # Drop invalid/empty abstracts:
            if nd['abstract'] == 'x':
                nd['abstract'] = None
            # Drop keywords that are just default ones for the whole of iPRES:
            to_keep = []
            for keyword in nd['keywords']:
                if keyword.startswith("Conferences -- iPRES Conference "):
                    continue
                # Otherwise, keep:
                to_keep.append(keyword.strip())
            nd['keywords'] = to_keep
            # Catch how Lightning Talks are indicated:
            if nd['abstract'] == 'Lightning Talk':
                nd['type'] = 'lightning talk'
                nd['abstract'] = None
            # Distinguish posters based on title or phrase in abstract:
            if ": Poster " in nd['title'] or " (Poster) " in nd['title'] or \
                (nd['abstract'] and ("this poster" in nd['abstract'].lower() \
                                     or "the poster" in nd['abstract'].lower() \
                                        or "our poster" in nd['abstract'].lower())):
                nd['type'] = "poster"
            # Shift institutions to separate field if present:
            creators = set()
            insts = set()
            if nd['creators'] == None:
                logger.error(f"No creator for {nd['title']} -- dropping this record")
                continue
            else:
                for creator in nd['creators']:
                    m = INST_RE.match(creator)
                    if m:
                        creators.add(m.group(1).strip())
                        insts.add(m.group(2).strip())
                    else:
                        creators.add(creator.strip())
            nd['creators'] = list(creators)
            nd['institutions'] = list(insts)
            # Write to file
            json.dump(nd, outfile)
            outfile.write('\n')

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
            if path.endswith('.phaidra.jsonl'):
                normalise_phaidra_jsonl(os.path.join(args.input_dir, path), outfile)
    # Also write as CSV:
    write_jsonl_to_csv(input_path=output_jsonl, output_path=output_csv)