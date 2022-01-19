# Segmentation 

## The Segment Object
`Segment` objects represent the metadata associated with a segment of User Ale logs.  Each object has a variety of fields, including:
- `segment_name`: The given name of a segment
- `start_end_val`: The start and end `clientTime`'s of a segment
- `num_logs`: The number of logs in a segment
- `uids`: A list of the UIDs of the logs within the segment
- `segment_type`: An enumerated type (`Segment_Type`) that denotes how the segment was created
- `generate_field_name`: The field name used for value-matching if a segment was created through segment generation (`generate_segments`)
- `generate_matched_values`: The values used for value-matching if a segment was created through segment generation (`generate_segments`)

### Segment Field Access through Getters
Segment fields can be accessed through get functions.  For example, if a dictionary of segments is created using the `generate_segments` function:
```python
generated_segments = distill.generate_segments(sorted_dict, 'type', ['click'], 1, 1)
```
then the number of logs in each of these segments could be printed to the console by running:
```python
for segment_name in generated_segments:
    print(generated_segments[segment_name].get_num_logs())
```
Note that these functions are called via the `Segment` object itself, following the pattern:
```
segment.get_...()
```
## Segment Creation
### Create_Segment
### Generate_Segment
### Detect Deadspace

## Combining Segments with Set Logic
### Union
### Intersection

## Writing Segments