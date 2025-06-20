import urllib.request
import argparse
import json
import os.path
from dppi.models import Publication
import frontmatter
from slugify import slugify

# Main for CLI
if __name__ == "__main__":
    # Set up a simpler argument parser:
    parser = argparse.ArgumentParser()
    parser.add_argument('input_jsonl')
    parser.add_argument('output_dir')

    args = parser.parse_args()

    # Open the source JSONL, convert to a suitably-named Markdown+frontmatter file:
    with open(args.input_jsonl) as in_file:
        for line in in_file:
            pub = Publication.model_validate_json(line)
            year = pub.year
            slug = slugify(pub.title, max_length=64)
            output_file = os.path.join(args.output_dir, f"./ipres-{year}/papers/{slug}.md")
            if not os.path.exists(os.path.dirname(output_file)):
                    os.makedirs(os.path.dirname(output_file))
            # Convert to dict
            metadata = dict(pub)
            metadata['publication_type'] = metadata.pop('type')
            metadata['layout'] = 'publication'
            metadata['parent'] = f'iPRES {year}'
            metadata['grand_parent'] = 'iPRES'
            metadata['year'] = year
            with open(output_file, 'wb') as f:
                 post = frontmatter.Post("", **metadata)
                 frontmatter.dump(post, f)