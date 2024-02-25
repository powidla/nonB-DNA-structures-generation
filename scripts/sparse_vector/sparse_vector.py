# Created by Nazar

import numpy as np
from joblib import dump, load


def from_slice_to_range(item):
    if_none = lambda a, b: b if a is None else a
    if isinstance(item, slice):
        return list(range(if_none(item.start, 0),
                          item.stop))
    else:
        raise TypeError


def saver(sparse_vec, file_name):
    """
    Saves model
    """

    dump([sparse_vec.shape,
          sparse_vec.data,
          sparse_vec.indices],
         file_name)


def loader(file_name):
    """
    Loads model
    """

    data = load(file_name)
    sparse_vec = SparseVector(1)
    [sparse_vec.shape,
     sparse_vec.data,
     sparse_vec.indices,
     sparse_vec.dtype] = data + [data[1].dtype]
    return sparse_vec


class SparseVector:
    def __init__(self, arg1, shape=None, dtype=np.int64):
        """
        Sparse vector init.

        It can be initiated following ways:

        SparseVector(L: int)
            Creates zeros vector of length L

        SparseVector(V: np.array)
            Creates sparse analogous of V

        SparseVector(inp: Tuple[np.array, np.array], shape)
            Copy directly
            self.data, self.indices = inp
            with certain shape
        """
        if isinstance(arg1, int):
            if arg1 < 1:
                raise TypeError(f"Can't use {arg1} as input, wrong length.")
            self.shape = arg1
            self.data = np.array([0], dtype=dtype)
            self.indices = np.array([0], dtype=np.int64)
            self.dtype = dtype

        elif isinstance(arg1, np.ndarray):
            if arg1.ndim != 1:
                raise TypeError(f"Can't use {arg1} as input, not single-dimensional.")
            self.shape = arg1.shape[0]
            self.dtype = arg1.dtype.type
            self.indices = np.where(np.diff(arg1, prepend=arg1[0] + 1) != 0)[0]
            self.data = arg1[self.indices]


        elif isinstance(arg1, tuple):
            if len(arg1) != 2:
                raise TypeError(f"Can't use {arg1} as input, wrong number of elements to unpack.")

            self.data = arg1[0]
            self.indices = arg1[1]
            self.dtype = arg1[0].dtype.type
            self.shape = shape if shape is not None else self.indices[-1] + 1

        else:
            raise TypeError(f"Can't use {arg1} as input!")

    def tamp(self, index=None):
        if self.data.shape[0] < 3:
            return
        if index is not None:
            # First index
            if index == 0:
                if self.data[0] == self.data[1]:
                    self.data = np.delete(self.data, 1)
                    self.indices = np.delete(self.indices, 1)
            # Last index
            elif index == self.data.shape[0] - 1:
                if self.data[self.data.shape[0] - 1] == self.data[self.data.shape[0] - 2]:
                    self.data = np.delete(self.data, self.data.shape[0] - 1)
                    self.indices = np.delete(self.indices, self.indices.shape[0] - 1)
            # Central index
            else:
                if self.data[index] == self.data[index - 1]:
                    if self.data[index] == self.data[index + 1]:
                        self.data = np.delete(self.data, [index, index + 1])
                        self.indices = np.delete(self.indices, [index, index + 1])
                    else:
                        self.data = np.delete(self.data, index)
                        self.indices = np.delete(self.indices, index)
                elif self.data[index] == self.data[index + 1]:
                    self.data = np.delete(self.data, index + 1)
                    self.indices = np.delete(self.indices, index + 1)
        else:
            raise NotImplementedError

    def __getitem__(self, key):
        if isinstance(key, slice):
            if key.start is None:
                key = slice(0, key.stop)
            if key.stop is None:
                key = slice(key.start, self.shape)
            if key.step is not None:
                raise IndexError("Can't use step")
            if key.start < 0 or key.stop > self.shape:
                raise IndexError(f"Can't use range {(key.start, key.stop)} in vector with {self.shape} shapegth")

            ind_left = np.searchsorted(self.indices, key.start, 'right') - 1
            ind_right = np.searchsorted(self.indices, key.stop, 'right') - 1
            if ind_left == ind_right:
                return np.repeat(self.data[ind_left], key.stop - key.start)
            else:
                result = np.zeros(key.stop - key.start,
                                  dtype=self.data.dtype)
                start_ind = key.start

                for interval in range(ind_left, ind_right + 1):
                    if interval + 1 < self.indices.shape[0]:
                        result[max(0, self.indices[interval] - start_ind):
                               self.indices[interval + 1] - start_ind] = self.data[interval]
                    else:
                        result[self.indices[interval] - start_ind:] = self.data[interval]
                return result

        elif isinstance(key, int):
            ind = np.searchsorted(self.indices, key, 'right') - 1
            return self.data[ind]
        else:
            raise TypeError(f"Can't use {type(key)} as index")

    def __setitem__(self, key, value):
        if not (isinstance(key, slice) or
                isinstance(key, int)):
            raise TypeError(f"Can't use {type(key)} as index")

        if not (isinstance(value, np.ndarray) or
                isinstance(value, self.dtype)):
            raise TypeError(f"Wrong data type, vector has {self.dtype}, but tried to set {type(value)}")

        if isinstance(value, np.ndarray):
            if value.ndim != 1:
                raise TypeError(f"Can't use multydim data")
            if isinstance(key, slice):
                if key.start is None:
                    key = slice(0, key.stop)
                if key.stop is None:
                    key = slice(key.start, self.shape)
                if key.step is not None:
                    raise IndexError("Can't use step")
                if key.start < 0 or key.stop > self.shape:
                    raise IndexError(f"Can't use range {(key.start, key.stop)} in vector with {self.shape} shapegth")

                indices = np.where(np.diff(value,
                                           prepend=value[0] + 1,
                                           append=value[-1] + 1) != 0)[0]
                for i, j in zip(indices[:-1], indices[1:]):
                    self.__setitem__(slice(key.start + i, key.start + j), value[i])
            return
        elif isinstance(value, self.dtype):
            if isinstance(key, slice):
                if key.start is None:
                    key = slice(0, key.stop)
                if key.stop is None:
                    key = slice(key.start, self.shape)
                if key.step is not None:
                    raise IndexError("Can't use step")
                if key.start < 0 or key.stop > self.shape:
                    raise IndexError(f"Can't use range {(key.start, key.stop)} in vector with {self.shape} shapegth")

                # Fast binary search
                ind_left = np.searchsorted(self.indices, key.start, 'right') - 1
                ind_right = np.searchsorted(self.indices, key.stop, 'right') - 1

                if ind_left == ind_right:
                    ind_left_old = self.indices[ind_left]
                    ind_right_old = self.indices[ind_left + 1] \
                        if ind_left + 1 < self.indices.shape[0] \
                        else self.shape

                    # WHOLE CASE
                    if ind_left_old == key.start and ind_right_old == key.stop:
                        self.data[ind_left] = value
                        self.tamp(ind_left)
                        return

                    # LEFT CASE
                    elif ind_left_old == key.start:
                        self.data = np.insert(self.data, ind_left, value)
                        self.indices = np.insert(self.indices, ind_left + 1, key.stop)
                        self.tamp(ind_left)
                        return

                    # RIGHT CASE
                    elif ind_right_old == key.stop:
                        self.data = np.insert(self.data, ind_left + 1, value)
                        self.indices = np.insert(self.indices, ind_left + 1, key.start)
                        self.tamp(ind_left + 1)
                        return

                    # CENTRAL CASE
                    else:
                        self.data = np.insert(self.data, ind_left + 1, [value, self.data[ind_left]])
                        self.indices = np.insert(self.indices, ind_left + 1, [key.start, key.stop])
                        self.tamp(ind_left + 1)
                        return

                else:
                    ind_left_old = self.indices[ind_left]
                    ind_right_old = self.indices[ind_right + 1] \
                        if ind_right + 1 < self.indices.shape[0] \
                        else self.shape

                    # WHOLE CASE
                    if ind_left_old == key.start and ind_right_old == key.stop:
                        self.data[ind_left] = value
                        self.data = np.delete(self.data, range(ind_left + 1, ind_right + 1))
                        self.indices = np.delete(self.indices, range(ind_left + 1, ind_right + 1))
                        self.tamp(ind_left)
                        return

                    # LEFT CASE
                    elif ind_left_old == key.start:
                        self.data[ind_left] = value
                        self.indices[ind_right] = key.stop
                        self.data = np.delete(self.data, range(ind_left + 1, ind_right))
                        self.indices = np.delete(self.indices, range(ind_left + 1, ind_right))
                        self.tamp(ind_left)
                        return

                    # RIGHT CASE
                    elif ind_right_old == key.stop:
                        self.data[ind_left + 1] = value
                        self.indices[ind_left + 1] = key.start

                        self.data = np.delete(self.data, range(ind_left + 2, ind_right + 1))
                        self.indices = np.delete(self.indices, range(ind_left + 2, ind_right + 1))
                        self.tamp(ind_left + 1)
                        return

                    # CENTRAL CASE
                    else:
                        if ind_right - ind_left > 1:
                            self.data[ind_left + 1] = value
                            self.indices[ind_left + 1] = key.start
                            self.indices[ind_right] = key.stop
                            self.data = np.delete(self.data, range(ind_left + 2, ind_right))
                            self.indices = np.delete(self.indices, range(ind_left + 2, ind_right))
                        else:
                            self.indices[ind_right] = key.stop
                            self.data = np.insert(self.data, ind_left + 1, value)
                            self.indices = np.insert(self.indices, ind_left + 1, key.start)
                        self.tamp(ind_left + 1)
                        return

            elif isinstance(key, int):
                self.__setitem__(slice(key, key + 1), value)
                return

    def __repr__(self):
        if self.shape <= 10:
            return 'sparse_array([' + \
                   ', '.join(self.__getitem__(slice(0, self.shape)).astype(str)) + \
                   f'], dtype={self.dtype})'
        else:
            info = 'sparse_array(['
            info += ', '.join(self.__getitem__(slice(0, 5)).astype(str))
            info += ', ..., '
            info += ', '.join(self.__getitem__(slice(self.shape - 6, self.shape)).astype(str))
            info += f'], dtype={self.dtype})'
            return info

    def __str__(self):
        info = ""
        info += f"Shape is {str(self.shape)}\n"
        info += f"Data is {str(self.data)}\n"
        info += f"Indices is {str(self.indices)}\n"
        info += f"Dtype is {str(self.dtype)}\n"
        return info

