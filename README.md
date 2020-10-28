# Sawmill
ELK stack for hacking


## Deployment

Generate the lookup tables from a topology file. The topology file can be anywhere on the system.
```
# Within the root repo directory
python scripts/build_lookup_tables.py topology.json
```


Also start all the elk docker files then wait then start nginx