# Sparse vector for bioinformatics tasks

This python package based on numpy that can be used for memory efficient interval-constant vector operating.

It based on an assumption that data in vector has interval-constant type. 
Having this assumption we can more efficiently utilize RAM memory.

For example:

[1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0] is interval-constant type.

[0, 7, 1, 2, 1, 4, 7, 7, 5, 9] is not interval-constant type.


### Usage

For example this code allows to use 5 time less memory than simple vector of length 10000

```python
from .sparce_vector import SparseVector
import numpy as np

sp_vec = SparseVector(np.arange(10000) // 10, 
                      dtype=np.int64)

# returns numpy array
sp_vec[3:6]

#returns whole array as numpy array
sp_vec[:]
```


On the real data this package can achieve much better results. 
For example on this real [data](http://dbarchive.biosciencedbc.jp/kyushu-u/hg19/assembled/Pol.Prs.50.AllAg.AllCell.bed)
compression exceeded 1.4 * 10^4.

This format makes available to use much more bioinformatics data.

## Authors

* **Nazar Beknazarov**