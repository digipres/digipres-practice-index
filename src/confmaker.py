import urllib.request
import argparse
import json
import csv
import os.path
import frontmatter

# Main for CLI
if __name__ == "__main__":
    # Set up a simpler argument parser:
    parser = argparse.ArgumentParser()
    parser.add_argument('input_csv')
    parser.add_argument('output_dir')

    args = parser.parse_args()

    # Open the source CSV, read the starting point for each iPres conference site, and parse.
    with open(args.input_csv) as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            if not row['name']:
                 continue
            # Pull the year out
            parts = row['name'].split(" ")
            year = int(parts[1])
            output_file = os.path.join(args.output_dir, f"./ipres-{year}/index.md")
            if not os.path.exists(os.path.dirname(output_file)):
                    os.makedirs(os.path.dirname(output_file))
            row['title'] = row.pop('name')
            row['layout'] = 'ipres'
            row['parent'] = 'iPRES'
            row['year'] = year
            with open(output_file, 'wb') as f:
                 post = frontmatter.Post("", **row)
                 frontmatter.dump(post, f)