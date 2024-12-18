# digipres-practice-index
An experiment in gathering together sources of information about digital preservation practices

This initial plan is to experiment with using Python to gather useful information sources, starting with iPres. Then see if this can usefully be transformed into something searchable using [Datasette](https://datasette.io/) or [Datasette Lite](https://lite.datasette.io/).

This originally relied on a tool called [DVC](https://dvc.org/). Why DVC? Because I wanted to manage how the data is complied, and I liked [the way it handles checking data dependencies](https://dvc.org/doc/user-guide/pipelines/defining-pipelines#simple-dependencies). Very #DigiPres... Also, e.g. [remote storage integration for data sets on Google Drive](https://dvc.org/doc/user-guide/data-management/remote-storage/google-drive).

However, having tried both DVC and [Snakemake](https://snakemake.readthedocs.io/), they seem very difficult to work with. Lots of complex dependencies that don't always install easily, and over-engineered for this use case. So, instead, build pipelines are manage the old-fashioned way, using [Make](https://en.wikipedia.org/wiki/Make_(software)). There's lots of tutorials for Make ([e.g.](https://makefiletutorial.com/)), and the Turing Way book has a really good section called [Reproducibility with Make](https://book.the-turing-way.org/reproducible-research/make.html).

## Development Setup

You need Python 3 and Make.

Clone this repo. Set up a Python 3 virtual env, e.g.

    python3 -m venv .venv
    source .venv/bin/activate

Install dependencies:

    pip install .

Optionally, install NLP data required for some analysis/processing (not in production use):

    python -m spacy download en_core_web_lg

## Local Usage

Build the data:

    make

Try the Datasette view:

    datasette serve practice.db --setting truncate_cells_html 120

After which you should be able to go to e.g. http://127.0.0.1:8001/practice/publications?_facet=type&_searchmode=raw&_facet=year&_facet_array=creators&_facet_array=institutions&_facet_size=10&_sort=year

Other build targets generate other derivatives. Check the [Makefile](./Makefile) for details.

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

#### IDEALS

