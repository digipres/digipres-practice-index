import urllib.request
import argparse
import json
import csv
import time
import os
import os.path

PHAIDRA_API_URL = "https://phaidra.univie.ac.at/api"
USER_AGENT = "DigiPresPubsRobot/1.0 (+https://www.digipres.org/about/)"
PHAIDRA_COOKIE = os.getenv('PHAIDRA_COOKIE', None)

# To mitigate barriers intended for AI crawlers:
# e.g. export PHAIDRA_COOKIE="VALUE"
if not PHAIDRA_COOKIE:
    raise Exception("No 'PHAIDRA_COOKIE' environment variable set!")


def get_phaidra_metadata(col_id, source_name, year, output_path):
    params = {
        "q" : "*:*",
        "wt" : "json",
        "rows" : 1000,
        "fq" : f'ispartof:"{col_id}"',
        "fl" : "*,dc_language,dc_identifier,size",
        "indent" : "true",
    }
    data = urllib.parse.urlencode(params).encode(encoding='utf-8',errors='ignore')
    req = urllib.request.Request(url=f"{PHAIDRA_API_URL}/search/select", headers={'User-Agent': USER_AGENT, 'Cookie': PHAIDRA_COOKIE }, data=data)
    res = urllib.request.urlopen(req, timeout=30)

    if res.status != 200:
        raise Exception(f"API call failed! -- {res.reason}")

    body = res.read().decode("utf-8")

    if not body:
        raise Exception(f"API call returned an empty response!")

    j = json.loads(body)

    with open(output_path, 'w') as outfile:
        for doc in j['response']['docs']:
            doc['__source_col_id'] = col_id
            doc['__source_name'] = source_name
            doc['__year'] = year
            json.dump(doc, outfile)
            outfile.write('\n')


# Main for CLI
if __name__ == "__main__":
    # Set up a simpler argument parser:
    parser = argparse.ArgumentParser()
    parser.add_argument('action', choices=['fetch-metadata'])
    parser.add_argument('input_csv')
    parser.add_argument('output_dir')

    args = parser.parse_args()

    if args.action == "fetch-metadata":
        # Open the source CSV, read the starting point for each iPres conference site, and parse.
        with open(args.input_csv) as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                print(row)
                if row['repo_system'] == 'phaidra':
                    if not os.path.exists(args.output_dir):
                        os.makedirs(args.output_dir)
                    output_path = os.path.join(args.output_dir, f"{row['source_name'].lower()}{row['year']}.phaidra.jsonl")
                    if not os.path.exists(output_path):
                        get_phaidra_metadata(row['repo_collection_id'], row['source_name'], int(row['year']), output_path)
                        print("...and sleep...")
                        time.sleep(10)
                else:
                    raise Exception(f"Unsupported repository system '{row['repo_system']}'!")
    else:
        raise Exception(f"Unimplemented action '{args.action}'!")