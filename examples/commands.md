# Example commands

```sh
# Check the sample JSON is valid
python tools/jsontool.py validate examples/sample.json

# Pretty-print it
python tools/jsontool.py format examples/sample.json pretty.json

# Pretty-print with sorted keys
python tools/jsontool.py format examples/sample.json pretty.json --sort-keys

# Flatten nested data to dot-separated keys
python tools/jsontool.py flatten examples/sample.json flat.json

# Get one value by dot path
python tools/jsontool.py get examples/sample.json user.address.city
python tools/jsontool.py get examples/sample.json orders.0.item

# Diff two JSON files (create a changed copy first to see differences)
python tools/jsontool.py diff examples/sample.json pretty.json
```
