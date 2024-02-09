from sickle import Sickle

sickle = Sickle('https://www.ideals.illinois.edu/oai-pmh')

# This function was used to work out what the right metadata set ID was:
def list_all_sets(sickle):
    sets = sickle.ListSets()
    for s in sets:
        print(s)

# This gets the records for the iPRES 2023 metadata set:
recs = sickle.ListRecords(metadataPrefix="oai_dc", set="com_2142_120947")
for r in recs:
    print(r.get_metadata())
