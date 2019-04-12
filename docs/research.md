# Random Research
## Looking only at 1 team
This can be achieved by adding a filter
for a dashboard. An example query for this filter would be
```JSON
{
  "query": {
    "wildcard": {
      "VictimIP": "10.*.1.*" 
    }
  }
}
```

## Advanced Settings
Navigate to `Management->Advanced Settings` and change the following settings:
```
doc_table:hideTimeColumn: True
doc_table:highlight: False
```
