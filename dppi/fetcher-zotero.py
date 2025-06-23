import json
import requests
from .models import Publication
from pyzotero import zotero

# Connect to the iPRES group library:
library_id = '5564150' 
library_type = 'group'
api_key = None # No key needed to read...
zot = zotero.Zotero(library_id, library_type, api_key)

# Each kind of publication is in a separate Zotero collection:
kinds = {
    "Game": "I5ZIMPFF",
    "Keynote": "HXWC2B33",
    "Lightning Talk": "C5N2QWPL",
    "Long Paper": "SUQMAHPE",
    "Panel": "MH2X5XH5",
    "Poster": "4M6S4PBV",
    "Short Paper": "TZKTD9WG",
    "Tutorial": "9FTP48DL",
    "Workshop": "PIDIXJUZ", 
}

# Loop through the kinds:
for pub_type, collection_key in kinds.items():

    # Get the whole set of items for this kind:
    items = zot.everything(zot.collection_items(collection_key))

    # Convert to JSON:
    for item in items:
        # Note item type based on collection (on normal items, not on attachments):
        if item['data']['itemType'] != "attachment":
            item['publication_type'] = pub_type
        else:
            # For attachments, check for an OSF link and grab it:
            att = item['data']
            if att['linkMode'] == 'imported_url' and att['url'].startswith("https://osf.io/"):
                landing_page = att['url']
                osf_id = landing_page.replace('https://osf.io/', '')
                osf_id = osf_id.replace('/','')
                # And record the details:
                att['osf_id'] = osf_id
                att['landing_page'] = landing_page
                osf_files_url = f"https://api.osf.io/v2/nodes/{osf_id}/files/osfstorage/?filter%5Bname%5D=&format=json&page=1&sort=name"
                att['osf_files'] = requests.get(osf_files_url).json()

        print(json.dumps(item))
