# Default to generating the SQLite DB:
.PHONY: all

all: practice.db

# ------

# Run all the fetchers:
fetch-all: fetch-phaidra-metadata fetch-ideals-metadata

fetch-phaidra-metadata: src/fetcher.py
	python src/fetcher.py fetch-metadata sources/ipres/index.csv sources/ipres/raw

fetch-ideals-metadata: src/fetcher-ideals.py
	python src/fetcher-ideals.py sources/ipres/raw/ipres2023.ideals.jsonl

# ------

# Generate the merged version from the raw source files:
sources/ipres/merged.jsonl sources/ipres/merged.csv: sources/ipres/raw/ipres*.jsonl src/merger.py
	python -m src.merger sources/ipres/raw sources/ipres/merged

# Generate the SQLite DB from the JSONL files:
# Make can't automatically delete outputs when things fail.
practice.db: sources/ipres/merged.jsonl
	rm -f practice.db
	sqlite-utils insert practice.db publications sources/ipres/merged.jsonl --nl
	sqlite-utils transform practice.db publications -o source_name -o year -o title -o type -o landing_page_url -o creators
	sqlite-utils enable-fts practice.db publications title creators abstract keywords institutions type

# ------

# Generate the Markdown versions (note that this expects the Publications repo to be available in a neighbouring folder!):
generate-markdown: sources/ipres/merged.jsonl
	rm -f ../publications/ipres/ipres-*/papers/*.md 
	python -m src.pubmaker sources/ipres/merged.jsonl ../publications/ipres

# Generate the author graph:
generate-networks: sources/ipres/merged.jsonl
	python -m src.graph_gen sources/ipres/merged.jsonl ipres-graph.json