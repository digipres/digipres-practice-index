# digipres-practice-index
An experiment in gathering together sources of information about digital preservation practices

This initial plan is to experiment with using [DVC](ss) to gather useful information sources, starting with iPres. Then see if this can usefully be transformed into something searchable using [Datasette](https://datasette.io/) or [Datasette Lite](https://lite.datasette.io/).


## Sources of Practice

### iPRES

Where are the papers and metadata... Links on https://iPRES-conference.org/ are not complete.

It may make more sense to use JSON to store this data, and use [JSON Schema](https://json-schema.org/) in [VSCode](https://code.visualstudio.com/docs/languages/json#_json-schemas-and-settings) to make it easer to edit them. That can then be consumed by the gathering scripts as well as being used to generate tabular forms like this.

- 💀 means the link is dead.
- 🗃️ means the link goes to an archived copy.
- the names in the proceedings columns are those of the linked repository.

| Conference | Location & Date | Website | Proceedings (single PDF) | Proceedings (articles) |
| ---- | ---- | ---- | ---- | ---- |
| iPRES 2004 | Beijing, China<br>July 14 - 16, 2004 | [official site💀](http://www.las.ac.cn/cedp/index_en.html), [mirror](https://iPRES-conference.org/iPRES04/) |  | [phaidra](https://phaidra.univie.ac.at/detail/o:295028) |
| iPRES 2005 | Göttingen, Germany<br>September 15 - 16, 2005 | [official site💀](http://rdd.sub.uni-goettingen.de/conferences/ipres05/), [mirror](https://ipres-conference.org/ipres05/) | [phaidra](https://phaidra.univie.ac.at/detail/o:295047) | [phaidra](https://phaidra.univie.ac.at/detail/o:295048) |
| iPRES 2006 | Ithaca, NY, U.S.A<br>October 8 - 10, 2006 | [official site🗃️](http://ipres.library.cornell.edu/), [mirror](https://ipres-conference.org/ipres06/) |  | [phaidra](https://phaidra.univie.ac.at/detail/o:294903) |
| iPRES 2007 | Beijing, China<br>October 11 - 12, 2007 | [official site💀](http://ipres.las.ac.cn/), [mirror](https://iPRES-conference.org/ipres07/) |  | [phaidra](http://phaidra.univie.ac.at/o:294846) |
| iPRES 2008 | London, United Kingdom<br>September 29 - 30, 2008  | [official site💀](http://www.bl.uk/ipres2008/), [mirror](https://ipres-conference.org/ipres08/) |  | [phaidra](http://phaidra.univie.ac.at/o:294193) |
| iPRES 2009 | San Francisco, CA, U.S.A.<br>October 5 - 6, 2009 | [official site💀](http://www.cdlib.org/ipres/ipres2009.html), [mirror](https://ipres-conference.org/ipres09/) |  |  [phaidra](http://phaidra.univie.ac.at/o:294045) |
| iPRES 2010 | Vienna, Austria<br>September 19 - 24, 2010 | [official site](http://www.ifs.tuwien.ac.at/dp/ipres2010/index.html), [mirror](https://ipres-conference.org/ipres10/) |  | [phaidra](http://phaidra.univie.ac.at/o:245914) |
| iPRES 2011 | Singapore<br>November 1 - 4, 2011  | [mirror](https://ipres-conference.org/ipres11/) |  |  [phaidra](http://phaidra.univie.ac.at/o:294299) |
| iPRES 2012 | Toronto, Canada<br>October 1 - 5 ,2012   | [official site💀](http://iPRES.ischool.utoronto.ca/), [mirror](https://ipres-conference.org/ipres12/) |  | [phaidra](http://phaidra.univie.ac.at/o:293685) |
| iPRES 2013 | Lisbon, Portugal<br>September 2 - 6, 2013 | [official site💀](http://ipres2013.sysresearch.org/), [mirror](https://ipres-conference.org/ipres13/) |  |  [phaidra](https://phaidra.univie.ac.at/detail/o:378098) |
| iPRES 2014 | Melbourne, Australia<br>October 6 - 10, 2014  | [official site🗃️](http://pandora.nla.gov.au/pan/149803/20150323-1209/ipres2014.org/index.html), [mirror](https://ipres-conference.org/ipres14/) | [phaidra](https://phaidra.univie.ac.at/o:378066) | [phaidra](https://phaidra.univie.ac.at/detail/o:378735) |
| iPRES 2015 | Chapel Hill, North Carolina, USA<br>November 2 - 6, 2015 | [official site💀](http://ipres2015.org/), [mirror](https://ipres-conference.org/ipres15/) | [phaidra](https://phaidra.univie.ac.at/detail/o:429524) | [phaidra](https://phaidra.univie.ac.at/detail/o:429627) |
| iPRES 2016 | Bern, Switzerland<br>October 3 - 6, 2016  | [official site💀](http://www.ipres2016.ch), [mirror](https://ipres-conference.org/ipres16/) |  | [phaidra](https://phaidra.univie.ac.at/o:502812) |
| iPRES 2017 | Kyoto, Japan<br>September 25 - 29, 2017  | [official site💀](https://ipres2017.jp/), [mirror](https://ipres-conference.org/ipres17/) |  | [phaidra](https://phaidra.univie.ac.at/detail/o:931148) |
| iPRES 2018 | Boston, Massachusetts, US<br>September 24 - 28, 2018 |  [official site](https://ipres2018.org/), [mirror](https://ipres-conference.org/ipres18/) |  | [osf-home](https://osf.io/u5w3q/), [phaidra](https://phaidra.univie.ac.at/detail/o:988723) |
| iPRES 2019 | Amsterdam, The Netherlands<br>September 16 - 20, 2019 | [official site](https://ipres2019.org/),  | [official site](https://ipres2019.org/static/proceedings/iPRES2019.pdf) | [osf-home](https://osf.io/6ern4/), [phaidra](https://phaidra.univie.ac.at/detail/o:1049636) |
| iPRES 2020 | _Cancelled due to SARS-CoV-2_ | - |  |  |
| \#weMissiPRES | Virtual Festival<br>September 22 - 24, 2020 | [official site](https://www.dpconline.org/events/past-events/wemissipres) |  |  |
| iPRES 2021 | Beijing, China, October 19 - 22, 2021 |  [official site💀](http://ipres2021.ac.cn/en/web/index/) |  | [osf-home](https://osf.io/rb2dt/), [phaidra](https://phaidra.univie.ac.at/detail/o:1417044) |
| iPRES 2022 | Glasgow, Scotland<br>September 12 - 16, 2022 | [official site](https://ipres2022.scot/) | [phaidra](https://phaidra.univie.ac.at/detail/o:1893644) | [osf-home](https://osf.io/8bczf/) |
| iPRES 2023 | Champaign-Urbana, Illinois, U.S.A.<br>September 19 - 22, 2023 | [official site](https://ipres2023.us/) | [ideals](https://www.ideals.illinois.edu/items/128305) | [ideals](https://www.ideals.illinois.edu/units/541) |
| iPRES 2024 | Ghent, Belgium, September 16 - 20, 2024 | [official site](https://ipres2024.pubpub.org/) |  |  |
| iPRES 2025 | Wellington, New Zealand, November 03 - 07, 2025 |  |  |  |
| iPRES 2026 | Copenhagen, Denmark, September 21 - 25, 2026 |  |  |  |

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
