from collections import namedtuple
import numpy as np

class PeriodicSet:
    """
    Represents a periodic set. Has attributes motif, cell and name.
    PeriodicSet objects are returned by the Readers in amd.io.
    """
    def __init__(self, motif, cell, name=None, **kwargs):
        self.motif = motif
        self.cell  = cell
        self.name  = name
        self.tags = kwargs

    # only called for attrs that don't exist
    def __getattr__(self, attr):
        if attr in self.tags:
            return self.tags[attr]
        else:
            raise AttributeError(f"{self.__class__.__name__} object has no attribute or tag {attr}")

    def __str__(self):
        m, dims = self.motif.shape
        return f"PeriodicSet({self.name}: {m} motif points in {dims} dimensions)"
    
    def __repr__(self):
        return f"PeriodicSet(name: {self.name}, cell: {self.cell}, motif: {self.motif}, tags: {self.tags})"
    
    # actually, this doesn't make complete sense. Used for debugging.
    def __eq__(self, other):
        return self.cell.shape == other.cell.shape and \
               self.motif.shape == other.motif.shape and \
               np.allclose(self.cell, other.cell) and \
               np.allclose(self.motif, other.motif)
    
    def __ne__(self, other):
        return not self.__eq__(other)
    
    def astype(self, dtype):
        return PeriodicSet(name=self.name, 
                           motif=self.motif.astype(dtype),
                           cell=self.cell.astype(dtype))