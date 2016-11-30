import numpy as np
import matplotlib.pyplot as plt
from bblr.models import Hopfield
from bblr.generators import SimpleLetterGenerator as gen


partialA = """
X...X
.XX..
.....
.XXX.
.XXX.
"""
    
a = gen.to_pattern(gen.A)
z = gen.to_pattern(gen.Z)
hop = Hopfield.Hopfield(verbose=True)
patterns = np.atleast_2d((a,z))
print patterns
hop.train(patterns, normW=True)
recovered = hop.recall(gen.to_pattern(partialA),steps=5)
gen.display(recovered)