# Examples

## MultiMaps
Think of them like reversible dictionaries 

```python
from pyutils.multimap import MultiMap

# language word to definition
dictionary = MultiMap([
    ("automobile", "wheeled road vehicle"),
    ("bank", "slope side of a river"),
    ("bank", "a financial institution"),
    ("car", "wheeled road vehicle"),
])

# lookup definitions
dictionary("bank")  # homonyms
dictionary.inverse()("wheeled road vehicle")  # synonyms

# update dictionary
if "thing" not in dictionary.domain:
    dictionary += MultiMap([
        ("thing", "object without name"),
    ])
```
