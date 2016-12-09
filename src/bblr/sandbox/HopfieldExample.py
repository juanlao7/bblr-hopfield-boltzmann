import numpy as np
from bblr.models import Hopfield
from bblr.generators import SimpleLetterGenerator as gen


partialA = """
X...X
.XX..
.....
.XXX.
.XXX.
"""

completeA = """
.XXX.
X...X
XXXXX
X...X
X...X
"""
    
a = gen.to_pattern(gen.A)
z = gen.to_pattern(gen.Z)
patterns = np.atleast_2d((a,z))
print patterns
hop = Hopfield.Hopfield(verbose=True)
'''Using Hebbian rule'''
#hop.trainHebbian(patterns, normW=True)
'''Using Storkey rule'''
hop.trainStorkey(patterns, normW=True)
recovered = hop.recall(gen.to_pattern(partialA),steps=10)
gen.display(recovered)