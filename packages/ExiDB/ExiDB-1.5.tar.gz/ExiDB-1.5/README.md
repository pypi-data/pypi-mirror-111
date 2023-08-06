# ExiDB NOSQL Database


## Installation

+ pip : `pip install ExiDB`

## Getting Started

```py
import exidb
db = ExiDB('path/file.json',None)
```

# Insert `key,value` to the database

```py
from exidb import ExiDB,QueryDB
db = ExiDB('path/file.json',None)
db.insert("Exi",{"_id":0})
```

# Add `key,value` to the database

```py
from exidb import ExiDB,QueryDB
db = ExiDB('path/file.json',None)
db.add("Exi.Items",["Pen"])
```

# Edit `key,value` to the database

```py
from exidb import ExiDB,QueryDB
db = ExiDB('path/file.json',None)
db.edit("Exi.Items","Paper")
```

# Append `key,value` to the database

```py
from exidb import ExiDB,QueryDB
db = ExiDB('path/file.json',None)
db.append("Exi.Items",["Pen"])
```

# get value from `key` to the database

```py
from exidb import ExiDB,QueryDB
db = ExiDB('path/file.json',None)
print(db.get("Exi.Items"))
```

# get all the file

```py
from exidb import ExiDB,QueryDB
db = ExiDB('path/file.json',None)
db.all()
```

# delete value from `key` to the database

```py
from exidb import ExiDB,QueryDB
db = ExiDB('path/file.json',None)
db.delete("Exi.Items")
```
# purge the file to the database

```python
from exidb import ExiDB,QueryDB
db = ExiDB('path/file.json',None)
db.purge()
```

# QueryDB

```py
from exidb import QueryDB
Query = QueryDB('path/file.json')
Query.Serch("Username") #return all the value that it key is Username
Query.JSONPathRaw("$..Username") #return raw JSONPath
```

