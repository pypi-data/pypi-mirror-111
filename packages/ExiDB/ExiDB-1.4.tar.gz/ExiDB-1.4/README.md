# ExiDB NOSQL Database


## Installation

+ pip : `pip install ExiDB`

## Getting Started

```py
from exidb import *

db = ExiDB('path/file.json',indent=None)

```


# Insert `key,value` to the database

```py

from exidb import *

db = ExiDB('path/file.json',indent=None)

db.insert("Exi",{"_id":0})

```

# Add `key,value` to the database

```py

from exidb import *

db = ExiDB('path/file.json',indent=None)

db.add("Exi.Items",["Pen"])

```

# Edit `key,value` to the database

```py

from exidb import *

db = ExiDB('path/file.json',indent=None)

db.edit("Exi.Items","Paper")

```

# Append `key,value` to the database

```py

from exidb import *

db = ExiDB('path/file.json',indent=None)

db.append("Exi.Items",["Pen"])


```

# get value from `key` to the database

```py

from exidb import *

db = ExiDB('path/file.json',indent=None)

print(db.get("Exi.Items"))


```

# get all the file

```py

from exidb import *

db = ExiDB('path/file.json',indent=None)

db.all()


```

# delete value from `key` to the database

```py

from exidb import *

db = ExiDB('path/file.json',indent=None)

db.delete("Exi.Items")


```
# purge the file to the database

```py

from exidb import *

db = ExiDB('path/file.json',indent=None)

db.purge()

```

# QueryDB

```py

from exidb import *

Query = QueryDB('path/file.json')

Query.Serch("Username") #return all the value that it key is Username

Query.JSONPathRaw("$..Username") #return raw JSONPath
 
```


## Contact the Developer 

### Discord : iExi#0416
### Discord Server : [Server](https://discord.gg/Q48kJxFsU7)

