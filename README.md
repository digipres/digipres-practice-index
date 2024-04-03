# digipres-practice-index
An experiment in gathering together sources of information about digital preservation practices

This initial plan is to experiment with using [DVC](ss) to gather useful information sources, starting with iPres. Then see if this can usefully be transformed into something searchable using [Datasette](https://datasette.io/) or [Datasette Lite](https://lite.datasette.io/).

Why DVC? TBA but I like [the way it handles checking data dependencies](https://dvc.org/doc/user-guide/pipelines/defining-pipelines#simple-dependencies). Very #DigiPres... Also, e.g. https://dvc.org/doc/user-guide/data-management/remote-storage/google-drive

## Development Setup

Clone this repo. Set up a Python 3 virtual env, e.g.

    python3 -m venv .venv
    source .venv/bin/activate

Install dependencies:

    pip install .

Pull the derived data:

    dvc pull

## Local Usage

Run the repro chain:

    dvc repro

Try the Datasette:

    datasette serve practice.db

After which you should be able to go to e.g. http://127.0.0.1:8001/practice/publications?_facet=type&_searchmode=raw&_facet=year&_facet_array=creators&_facet_array=institutions&_facet_size=10&_sort=year

## Sources of Practice

### iPRES

Where are the papers and metadata... Links on https://iPRES-conference.org/ are not complete.

It may make more sense to use JSON to store this data, and use [JSON Schema](https://json-schema.org/) in [VSCode](https://code.visualstudio.com/docs/languages/json#_json-schemas-and-settings) to make it easer to edit them. That can then be consumed by the gathering scripts as well as being used to generate tabular forms like this.

The information about each iPRES conference is now stored as a set of Markdown+metadata files in the `publications` repository, and are summarised at http://www.digipres.org/publications/ipres/ 

#### PHAIDRA

- Seems to contain PDFs of individual contributions and whole-conference proceedings documents.
- There are e.g. posters as well as articles and it should be possible to distinguish them.
- There does not seem to be an other materials, e.g. links to recordings, etc.
- Has a kind of implicit API, seems to expose parts of Solr, e.g. [items from the iPRES 2004 collection](https://services.phaidra.univie.ac.at/api/search/select?q=*%3A*&wt=json&start=0&rows=32&fq=owner%3A*%20AND%20ispartof%3A%22o%3A295028%22%20AND%20-isinadminset%3A%22phaidra%3Autheses.univie.ac.at%22%20AND%20-hassuccessor%3A*%20AND%20-ismemberof%3A[%22%22%20TO%20*]&indent=on) which can be simplified to [this](https://services.phaidra.univie.ac.at/api/search/select?q=*%3A*&wt=json&start=0&rows=1000&fq=ispartof%3A%22o%3A295028%22&indent=on)
- Might be easier to just download the CSV for each iPRES collection manually, and then use the object IDs.
- Once you have an object ID for an article, it's straightforward to get:
	- Metadata: https://services.phaidra.univie.ac.at/api/object/o:295002/uwmetadata?format=xml
	- Thumbnail: https://services.phaidra.univie.ac.at/api/object/o:295002/thumbnail
	- Download: https://services.phaidra.univie.ac.at/api/object/o:295002/download

#### OSF

- More recent conferences appear in OSF, which has a much more complicated structure, but allows more types of materials to be stored.
