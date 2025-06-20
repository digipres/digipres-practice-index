import json
from .models import Publication
from pyzotero import zotero
library_id = '5564150' # The iPRES group library
library_type = 'group'
api_key = None # No key needed to read...
zot = zotero.Zotero(library_id, library_type, api_key)
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

for pub_type, collection_key in kinds.items():
    # Get the whole set:
    items = zot.everything(zot.collection_items(collection_key))

    # Convert to JSON
    for item in items:
        # Note item type based on collection (but not on attachments):
        if item['data']['itemType'] != "attachment":
            item['publication_type'] = pub_type
        print(json.dumps(item))
