# Graph Functions

The file 'graph.py' provides Python functions for creating charts from edge lists.

## Sankey Function

```python
sankey(edges_segmentN, node_labels=False)
```

The Sankey Function passes an edge list, or a list of tuples, and returns a Sankey, or a flow chart where width corresponds to quantity. Below is an example of a Sankey Diagram:

[![sankey0.png](https://i.postimg.cc/4NnnmphJ/sankey0.png)](https://postimg.cc/w789ryVP)
Additionally, users have the option to pass a dictionary of node labels to replace existing labels.

Below is an example:

**Input:**
```python
edges = [('a','b'),
         ('b','c'),
         ('c','b'),
         ('b','c'),
         ('c','d'),
         ('d','a')]

labels = {'d':'enD'}
         
sankey(edges, labels)
```

**Output:**
[![sankey.png](https://i.postimg.cc/50v6NJH8/sankey.png)](https://postimg.cc/YGrpbJzS)


