import os
import sys
import unittest
import numpy as np
sys.path.append(os.path.dirname(os.path.realpath(__file__)))
from sparse_vector import SparseVector


class SparseTester(unittest.TestCase):
    def test_wide(self):
        for i in range(5):
            arr = np.random.randint(-1000, 200, 1000)
            self.assertEqual((SparseVector(arr)[:] == arr).all(), True)

    def test_narrow(self):
        for i in range(5):
            arr = np.random.randint(0, 2, 1000)
            self.assertEqual((SparseVector(arr)[:] == arr).all(), True)

    def test_long(self):
        for i in range(3):
            arr = np.random.randint(0, 10, 10000)
            self.assertEqual((SparseVector(arr)[:] == arr).all(), True)

    def test_insertion(self):
        for _ in range(3):
            arr = np.zeros(1000)
            spr_arr = SparseVector(1000)
            for i in range(100):
                beg, end = np.sort(np.random.randint(0, 1000, 2))
                val = np.random.randint(0, 10000)
                arr[beg:end] = np.int64(val)
                spr_arr[beg:end] = np.int64(val)
            self.assertEqual((spr_arr[:] == arr).all(), True)


if __name__ == '__main__':
    unittest.main()
