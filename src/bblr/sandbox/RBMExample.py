import numpy as np
from bblr.models import RBM
from bblr.generators import SimpleLetterGenerator as gen


partialA = """
.XXXX
X..XX
XXXXX
X...X
XX..X
"""

a = gen.to_pattern(gen.A)
z = gen.to_pattern(gen.Z)
rbm = RBM.RBM(25, 5, verbose=True)
patterns = np.atleast_2d((a,z))
print patterns
rbm.train(patterns, 500, 0.01)
recovered = rbm.recall(gen.to_pattern(partialA))
print "Recovered", recovered
gen.display(recovered)