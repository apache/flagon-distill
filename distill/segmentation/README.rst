
============
Segmentation
============

The Segment Object
------------------
`Segment` objects represent the metadata associated with a segment of UserAle logs.  Each object has a variety of fields, including:

* ``segment_name``: The given name of a segment
* ``start_end_val``: The start and end ``clientTime``'s of a segment
* ``num_logs``: The number of logs in a segment
* ``uids``: A list of the UIDs of the logs within the segment
* ``segment_type``: An enumerated type (``Segment_Type``) that denotes how the segment was created
* ``generate_field_name``: The field name used for value-matching if a segment was created through segment generation (`generate_segments`)
* ``generate_matched_values``: The values used for value-matching if a segment was created through segment generation (`generate_segments`)

These fields can be accessed through `get` functions.  For example, if a dictionary of segments is created using the ``generate_segments`` function:
::
    generated_segments = distill.generate_segments(sorted_dict, 'type', ['clicks'], 1, 1)
then the number of logs in each of these segments could be printed to the console by running:
::
    for segment_name in generated_segments:
        print(generated_segments[segment_name].get_num_logs())
.. note ::
    These functions are called via the ``Segment`` object itself, following the pattern ``segment.get_...()``

Segment Creation
----------------

Combining Segments with Set Logic
---------------------------------
Segments can be combined to create set logic


You can perform union on the following:
::
    uids = segment1.uids
    for uid in segment2.uids:
        if uid not in uids:
            uids.append(uid)

.. note::
    A new segment with the given segment_name, start and end values based on the smallest client time and
    largest client time of the given segments, and a list of the union of the uids of segment1 and segment2.



You can perform intersection on the following:
::
    uids = []
    for uid in segment2.uids:
        if uid in segment1.uids:
            uids.append(uid)
.. note::
    A new segment with the given segment_name, start and end values based on the smallest client time and
    largest client time of the given segments, and a list of the intersection of the uids of segment1 and segment2.

Writing Segments
----------------
Write Segment creates a nested of segment names to UIDs which then map to individual logs (i.e result['segment_name'][uid] --> log). This assists with easy iteration over defined segments
::
    result = {}
    create_result = create_segment(target_dict, segment_names, start_end_vals)

    # Iterate through segments to get logs
    for segment_name in create_result:
        result[segment_name] = {}
        for uid in create_result[segment_name].uids:
            result[segment_name][uid] = target_dict[uid]

    return result
.. note::
    A nested dictionary of segment_names to uids to individual log

Exporting Segments
------------------
