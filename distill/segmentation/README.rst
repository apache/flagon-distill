
============
Segmentation
============

The ``Segment`` Object
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

.. code:: python

    generated_segments = distill.generate_segments(sorted_dict, 'type', ['clicks'], 1, 1)

then the number of logs in each of these segments could be printed to the console by running:

.. code:: python

    for segment_name in generated_segments:
        print(generated_segments[segment_name].get_num_logs())

.. note ::
    These functions are called via the ``Segment`` object itself, following the pattern ``segment.get_...()``

The ``Segments`` Object
-------------------
When creating ``Segment`` objects, the segment creation functions described in the following section return ``Segments`` objects.  These objects contain a list of ``Segment`` objects and help us to access, filter, and represent these objects in a variety of different ways described below:

Using Subscripts
****************
Individual ``Segment`` objects can be accessed using subscripts.  These subscripts can either be an index indicating the location of the ``Segment`` object in the underlying list or the segment name of a ``Segment`` object.

.. code:: python

    segments    # A Segments object
    segment0 = segments[0]  # Accessing the first Segment object via numeric index
    segment1 = segments["1"]  # Accessing the second Segment object via segment name

``Segments`` Iteration
**********************
``Segments`` iteration can be done as follows:

.. code:: python

    segments    # A Segments object
    for segment in segments:
        print(segment)

The above code will print each ``Segment`` in the underlying list of ``Segments``.

List Comprehensions
*******************
``Segments`` objects can also be used when performing list comprehensions.

.. code:: python

    segments    # A Segments object
    segment_names = [segment.segment_name for segment in segments]     # Returns a list of segment names

The list comprehension example above can be used to get a list of all of the segment names that exist in the ``Segments`` object.

Filtering ``Segments``
**********************
The ``Segments`` object is particularly useful when attempting to curate a collection of ``Segment`` objects.  The ``Segments`` class currently contains three functions that filter the underlying list of ``Segment`` objects: ``get_num_logs``, ``get_segments_before``, and ``get_segments_of_type``.

``get_num_logs``
^^^^^^^^^^^^^^^^
The ``get_num_logs`` function returns a new ``Segments`` object that only contains the ``Segment`` objects within the calling ``Segments`` object that contain at least the specified number of logs.  An example is shown below:

**Input:**

.. code:: python

    print("Original Segments Object:")
    print(segments)

    segments = segments.get_num_logs(5)

    print("\nFiltered Segments Object:")
    print(segments)

**Console Output:**

.. code:: console

    Original Segments Object:
    Segments: [
    Segment: name=0, num_logs=3, start=1623691890656, end=1623691895656, type=Segment_Type.FIXED_TIME
    Segment: name=1, num_logs=0, start=1623691895656, end=1623691900656, type=Segment_Type.FIXED_TIME
    Segment: name=2, num_logs=9, start=1623691900656, end=1623691905656, type=Segment_Type.FIXED_TIME
    Segment: name=3, num_logs=7, start=1623691905656, end=1623691910656, type=Segment_Type.FIXED_TIME
    ]

    Filtered Segments Object:
    Segments: [
    Segment: name=2, num_logs=9, start=1623691900656, end=1623691905656, type=Segment_Type.FIXED_TIME
    Segment: name=3, num_logs=7, start=1623691905656, end=1623691910656, type=Segment_Type.FIXED_TIME
    ]

The above code removes the second ``Segment`` object from the ``Segments`` object since it only contains 3 logs.

``get_segments_before``
^^^^^^^^^^^^^^^^^^^^^^^
The ``get_segments_before`` function returns a new ``Segments`` object that contains all the ``Segment`` objects from the calling ``Segments`` object that have end times before the user given time.  An example usage of this function is shown below:

**Input:**

.. code:: python

    print("Original Segments Object:")
    print(segments)

    segments = segments.get_segments_before(1623691905656)

    print("\nFiltered Segments Object:")
    print(segments)

**Console Output:**

.. code:: console

    Original Segments Object:
    Segments: [
    Segment: name=0, num_logs=3, start=1623691890656, end=1623691895656, type=Segment_Type.FIXED_TIME
    Segment: name=1, num_logs=0, start=1623691895656, end=1623691900656, type=Segment_Type.FIXED_TIME
    Segment: name=2, num_logs=9, start=1623691900656, end=1623691905656, type=Segment_Type.FIXED_TIME
    Segment: name=3, num_logs=7, start=1623691905656, end=1623691910656, type=Segment_Type.FIXED_TIME
    ]

    Filtered Segments Object:
    Segments: [
    Segment: name=0, num_logs=3, start=1623691890656, end=1623691895656, type=Segment_Type.FIXED_TIME
    Segment: name=1, num_logs=0, start=1623691895656, end=1623691900656, type=Segment_Type.FIXED_TIME
    ]

The above output shows that the ``get_segments_before`` function filtered out any ``Segment`` object that did not have an end time before 1623691905656.

``get_segments_of_type``
^^^^^^^^^^^^^^^^^^^^^^^^
The ``get_segments_of_type`` function filters out ``Segment`` objects that do not have the indicated type of segment creation method.  An example usage of this function is shown below:

**Input:**

.. code:: python

    print("Original Segments Object:")
    print(segments)

    segments = segments.get_segments_of_type(distill.Segment_Type.FIXED_TIME)

    print("\nFiltered Segments Object:")
    print(segments)

**Console Output:**

.. code:: console

    Original Segments Object:
    Segments: [
    Segment: name=0, num_logs=3, start=1623691890656, end=1623691895656, type=Segment_Type.FIXED_TIME
    Segment: name=1, num_logs=0, start=1623691895656, end=1623691900656, type=Segment_Type.CREATE
    Segment: name=2, num_logs=9, start=1623691900656, end=1623691905656, type=Segment_Type.FIXED_TIME
    Segment: name=3, num_logs=7, start=1623691905656, end=1623691910656, type=Segment_Type.DEADSPACE
    ]

    Filtered Segments Object:
    Segments: [
    Segment: name=0, num_logs=3, start=1623691890656, end=1623691895656, type=Segment_Type.FIXED_TIME
    Segment: name=2, num_logs=9, start=1623691900656, end=1623691905656, type=Segment_Type.FIXED_TIME
    ]

The example above shows how this function can be used to create a ``Segments`` object that only contains ``Segment`` objects that were created through the fixed time generation function (this function is explained further in the following section).

Appending and Deleting ``Segment`` Objects
******************************************
``Segment`` objects can be appended or deleted from ``Segments`` objects using three functions: ``append``, ``append_segments``, and ``delete``.

``append``
^^^^^^^^^^
The ``append`` function takes a ``Segment`` object as a parameter and appends it to the calling ``Segments`` object.  An example usage of this function is shown below:

**Input:**

.. code:: python

    print("Original Segments Object:")
    print(segments)

    print("\nSegment object to add:")
    print(segment)

    segments.append(segment)

    print("\nModified Segments Object:")
    print(segments)

**Console Output:**

.. code:: console

    Original Segments Object:
    Segments: [
    Segment: name=0, num_logs=3, start=1623691890656, end=1623691895656, type=Segment_Type.FIXED_TIME
    ]

    Segment object to add:
    Segment: name=1, num_logs=0, start=1623691895656, end=1623691900656, type=Segment_Type.FIXED_TIME

    Modified Segments Object:
    Segments: [
    Segment: name=0, num_logs=3, start=1623691890656, end=1623691895656, type=Segment_Type.FIXED_TIME
    Segment: name=1, num_logs=0, start=1623691895656, end=1623691900656, type=Segment_Type.FIXED_TIME
    ]

The above example shows how a ``Segment`` object can be appended to a ``Segments`` object.  Note that this function modifies the underlying ``Segments`` object rather than returning a new ``Segments`` object.

``append_segments``
^^^^^^^^^^^^^^^^^^^
The ``append_segments`` function appends an entire ``Segments`` object to the calling ``Segments`` object.  This results in an updated ``Segments`` object that contains all of the ``Segment`` objects that were in the two ``Segments`` objects.  An example usage of this function is shown below:

**Input:**

.. code:: python

    print("Original Segments Object:")
    print(segments1)

    print("\nSegments object to append:")
    print(segments2)

    segments1.append_segments(segments2)

    print("\nModified Segments Object:")
    print(segments1)

**Console Output:**

.. code:: console

    Original Segments Object:
    Segments: [
    Segment: name=0, num_logs=3, start=1623691890656, end=1623691895656, type=Segment_Type.FIXED_TIME
    ]

    Segments object to append:
    Segments: [
    Segment: name=1, num_logs=0, start=1623691895656, end=1623691900656, type=Segment_Type.FIXED_TIME
    Segment: name=2, num_logs=9, start=1623691900656, end=1623691905656, type=Segment_Type.FIXED_TIME
    ]

    Modified Segments Object:
    Segments: [
    Segment: name=0, num_logs=3, start=1623691890656, end=1623691895656, type=Segment_Type.FIXED_TIME
    Segment: name=1, num_logs=0, start=1623691895656, end=1623691900656, type=Segment_Type.FIXED_TIME
    Segment: name=2, num_logs=9, start=1623691900656, end=1623691905656, type=Segment_Type.FIXED_TIME
    ]

The above code appends the ``Segment`` objects within segments2 to the segments1 object.

``delete``
^^^^^^^^^^
The ``delete`` function takes in a segment name and removes the ``Segment`` object with that name from the calling ``Segments`` object.  Below is an example usage of this function:

**Input:**

.. code:: python

    print("Original Segments Object:")
    print(segments)

    segments.delete("0")

    print("\nModified Segments Object:")
    print(segments)

**Console Output:**

.. code:: console

    Original Segments Object:
    Segments: [
    Segment: name=0, num_logs=3, start=1623691890656, end=1623691895656, type=Segment_Type.FIXED_TIME
    Segment: name=1, num_logs=0, start=1623691895656, end=1623691900656, type=Segment_Type.FIXED_TIME
    Segment: name=2, num_logs=9, start=1623691900656, end=1623691905656, type=Segment_Type.FIXED_TIME
    ]

    Modified Segments Object:
    Segments: [
    Segment: name=1, num_logs=0, start=1623691895656, end=1623691900656, type=Segment_Type.FIXED_TIME
    Segment: name=2, num_logs=9, start=1623691900656, end=1623691905656, type=Segment_Type.FIXED_TIME
    ]

The above code removes the ``Segment`` object from the calling ``Segments`` object that is denoted by the segment name "0".

Returning Different Data Structures
***********************************
An additional feature of the ``Segments`` object is the ability to return different data structures that represent the ``Segment`` objects within the ``Segments`` object.  Currently there are two different data structure representations that can be returned by the ``Segments`` object: a list of ``Segment`` objects and a dictionary of segment names to ``Segment`` objects.  Below are examples of each function.

``get_segment_list``
^^^^^^^^^^^^^^^^^^^^
This function returns a list of the ``Segment`` objects within the calling ``Segments`` object.

**Example:**

.. code:: python

    segments    # A Segments object

    segments_list = segments.get_segment_list()     # A list of the Segment objects within segments

``get_segment_name_dict``
^^^^^^^^^^^^^^^^^^^^^^^^^
The ``get_segment_name_dict`` function returns a dictionary whose keys are the segment names of the ``Segment`` objects which refer to the ``Segment`` objects themselves.

**Example:**

.. code:: python

    segments    # A Segments object

    segments_dict = segments.get_segment_name_dict()     # A dictionary of the Segment objects within segments

Segment Creation
----------------
The creation of segments can be done through the use of three functions: ``create_segment``, ``generate_segments``, and ``detect_deadspace``.

Create Segment
**************
The most literal way to create a segment is through the use of the ``create_segment`` function.  This function takes in three parameters in order to create segments: a target dictionary of UserAle logs, a list of segment names, and a list of tuples that represent the start ``clientTime`` and end ``clientTime`` of the segment.  Given this information, segments can be created as follows:

.. code:: python

    # Sorted dictionary of UserAle logs
    sorted_dict

    # List of segment names
    segment_names = ["segment1", "segment2"]

    # Time tuples
    start_end_vals = [(start_time_1, end_time_1), (start_time_2, end_time_2)]

    # Create Segments
    segments = distill.create_segment(sorted_dict, segment_names, start_end_vals)

The above code will output a dictionary of ``segment_name`` to ``Segment`` objects following the respective order of the segment names and start/end tuples.  For instance, we can access the first segment by doing the following:

.. code:: python

    segment1 = segments["segment1"]


Generate Segments
*****************
Segment generation is a more automatic way to create segments and is based off of the matching of a particular UserAle log field with a list of possible values.  The function ``generate_segments`` will then generate segments based on windows of time starting before and after the matched field, indicated in seconds as a function parameter.  The below code illustrates the basic use of this function:

.. code:: python

    # Sorted dictionary of UserAle logs
    sorted_dict

    # Generate segments based on user clicks
    segments = distill.generate_segments(sorted_dict, 'type', ['click'], 1, 2)

The above code will create segments that represent windows of time 1 second prior to a 'click' type and 2 seconds after a 'click' type.  If we wanted to generate segments that matched both 'click' and 'load' types, then we could use the following code:

.. code:: python

    # Sorted dictionary of UserAle logs
    sorted_dict

    # Generate segments based on user clicks and loads
    segments = distill.generate_segments(sorted_dict, 'type', ['click', 'load'], 1, 2)

.. note::
    ``generate_segments`` does not overlap segments.  In the event that two matching events happen back-to-back within the logs and the second log is already in the segment generated by the first, the second segment will not have its own segment created.  This non-overlapping behavior also may create segments that are shorter in time than expected.  For instance, if a segment is created with an end time that is after the start time of a new segment, the new segment's start time will default to the end time of the previous segment.

Detect Deadspace
****************
Another way to create segments is to do so based on deadspace in the UserAle logs.  Deadspace is simply time in which the user is idle.  The ``detect_deadspace`` function creates segments based on deadspace in the logs given a threshold for what is considered to be 'deadspace'.  An example of this is shown below:

.. code:: python

    # Sorted dictionary of UserAle logs
    sorted_dict

    # Create segments based on detected deadspace
    segments = distill.detect_deadspace(sorted_dict, 20, 1, 2)

The above code will output a dictionary of segment names to ``Segment`` objects that represent deadspace segments.  In this case, we have defined 'deadspace' to be any idle time of 20 seconds.  Each time deadspace is detected, the logs that occurred 1 second before and 2 seconds after that idle time are recorded in the segment.

Generating Fixed Time Segments
******************************
Generates segments based on fixed time intervals

.. code:: python

        segments = distill.generate_fixed_time_segments(sorted_dict, 5, label="generated")
        #results
        Segment: name=generated0, num_logs=3, start=1623691890656, end=1623691895656, type=Segment_Type.FIXED_TIME

..note::


Collapsing Window Segments
**************************
Generates segments based on a window to time in which the given field name has a value matching one of the values indicated by the field_values_of_interest list.

.. code:: python

    #segments = create_segment(target_dict, segment_names, start_end_vals)


Combining Segments with Set Logic
---------------------------------
Segments can be combined to create set logic.

Union
*****
You can perform union on the following:

.. code:: python

    # Segment 1
    segment1.get_uids()     #[uid1, uid2, uid3]

    # Segment 2
    segment2.get_uids()     #[uid3, uid4, uid5]

    # Perform Union
    new_segment = distill.union(new_segment, segment1, segment2)
    new_segment.get_uids()  #[uid1, uid2, uid3, uid4, uid5]

.. note::
    A new segment with the given segment_name, start and end values based on the smallest client time and
    largest client time of the given segments, and a list of the union of the uids of segment1 and segment2.


Intersection
************
You can perform intersection on the following:

.. code:: python

    # Code to create a segment
    segment1.get_uids()   #[uid1, uid3, uid6]

    # Segment 2
    segment2.get_uids()     #[uid3, uid6, uid9]

    new_segment = distill.intersection(new_segment, segment1, segment2)
    new_segment.get_uids()  #[uid3, uid6]

.. note::

    A new segment with the given segment_name, start and end values based on the smallest client time and
    largest client time of the given segments, and a list of the intersection of the uids of segment1 and segment2.

Difference
**********
Difference creates a new segment based on the logical difference of segments.

.. code:: python

    # Code to create a segment
    segment1.get_uids()   #[uid1, uid2, uid3]

    # Segment 2
    segment2.get_uids()     #[uid2, uid4, uid5]

    new_segment1 = distill.difference(new_segment, segment1, segment2)
    new_segment1.get_uids()  #[uid1, uid3]

    new_segment2 = distill.difference(new_segment, segment2, segment1)
    new_segment2.get_uids()  #[uid4, uid5]

Writing Segments
----------------
Write Segment creates a nested of segment names to UIDs which then map to individual logs (i.e result['segment_name'][uid] --> log). This assists with easy iteration over defined segments

.. code:: python

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
Segments can be exported into csv files using the ``export_segments`` function.  This function will take the path to place the new file along with a dictionary of segment objects (matching the form outputted by the segment creation functions) and output a new csv with each segment on a new line.
