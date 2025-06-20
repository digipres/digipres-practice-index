import urllib.request
import argparse
import json
import os.path
from .models import Publication
import frontmatter
from slugify import slugify

# Main for CLI
if __name__ == "__main__":
    # Set up a simpler argument parser:
    parser = argparse.ArgumentParser()
    parser.add_argument('input_jsonl')
    parser.add_argument('output_json')

    args = parser.parse_args()

    # Open the source JSONL, convert to a suitably-named Markdown+frontmatter file:
    pubs = []
    with open(args.input_jsonl) as in_file:
        for line in in_file:
            pub = Publication.model_validate_json(line)
            pubs.append(pub)

    # Process for unique nodes:
    creator_counts = {}
    for pub in pubs:
        for creator in pub.creators:
            creator_counts[creator] = creator_counts.get(creator, 0) + 1
    node_index = list(creator_counts.keys())
    #print(node_index)

    # Build up the node list:
    node_list = []
    for i, name in enumerate(node_index):
        node_list.append( { 
            'id': i,
            'name': node_index[i],
            'count': creator_counts[node_index[i]],
            'group': 0
        })
    #print(node_list)

    # Now build a hash of the sets of links, to accumulate the total pubs for each pairing
    # Loop over all publications for the links:
    combos = []
    for pub in pubs:
        # Generate all combinations, excluding self-matches:
        combos += [(x,y) for x in pub.creators for y in pub.creators if x > y]
    # And turn into link counts:
    links_counts = {}
    for combo in combos:
        links_counts[combo] = links_counts.get(combo, 0) + 1
    #print(links_counts)

    # Convert this into the right form:
    links = []
    for link_key in links_counts:
        source, target = link_key
        link = {
            'source': node_index.index(source),
            'target': node_index.index(target),
            'value' : links_counts[link_key]
        }
        links.append(link)

    # Assemble the data:
    data = {
        'nodes': node_list,
        'links': links
    }

    with open(args.output_json, 'w') as f:
        json.dump(data, f)
"""

// Now the links...

// Generates each combination, storing node indexes, and sorted so node pairs always match:
function generate_combinations(array, nodes) { 
  var result = array.reduce( (acc, v, i) =>
    acc.concat(array.slice(i+1).map( w => [nodes.indexOf(v) , nodes.indexOf(w)].sort() )),
  []);
  return result;
}

// Extract out all the individual creator pairs from papers:
const single_links = creators.flatMap( c => generate_combinations(c, node_index));
// Sort the array so we can count unique entries more easily:
single_links.sort();

// Now count them:
var count = 1;
const links = [];
// Loop over the sorted array, looking at pairs:
for (var i = 0; i < single_links.length; i++)
{
    if (i < single_links.length - 1 && single_links[i].join(",") == single_links[i+1].join(","))
    {
      count +=1;
    }
    else
    {
        links.push( {
          source: single_links[i][0],
          target: single_links[i][1],
          value: count
        })
        count=1;
    }
}

//display(links);

const data = {
  nodes: node_list,
  links: links
}
"""
