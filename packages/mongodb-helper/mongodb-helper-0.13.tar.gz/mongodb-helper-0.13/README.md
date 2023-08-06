## mongodb-helper
### Methods that simplify MongoDB collection reading and writing.
Method | Description
--- | --- |
get_document | Reads a document with the given id
update_document | Updates a document with the given id
insert_document | Creates a new document with the given id and data
delete_document | Deletes a document with the given id

#### Example:
```python
from mongodb_helper import Helper
from pymongo import MongoClient

URI = "CLUSTER URI"

cluster = MongoClient(URI)
db = cluster["database name"]
collection = db["collection name"]

helper = Helper("_id", collection)

document = helper.get_document(1122334455667788)
```
