# vitess-helpers
This library is intended to be a general library to help manage the lifecycle of a Vitess cluster.

Visit https://vitess.io/ for more information on what Vitess is.

## shard range library
Generate shard ranges using python. The library takes a single input `shards` and generates a list of shard range names.

See Vitess documentation for further information:

https://vitess.io/docs/reference/features/sharding/

Example usage:
```python
>>> from vitess_helpers import shard_ranges
>>> shard_ranges(3)
['-55', '55-aa', 'aa-']
>>>
```

## to install

`pip install vitess-helpers`
