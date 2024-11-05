# Create a native Ising problem
from dwave.system import DWaveSampler
import numpy as np
import dwave.inspector

sampler = DWaveSampler(token="DEV-edba7dbb3a72fc17fe9561831ed5792ddea6c5b2")
h = {v: 0.0 for v in sampler.nodelist}
J = {tuple(c): np.random.choice(list(range(-5, 6))) for c in sampler.edgelist}

from greedy import SteepestDescentSolver

solver_greedy = SteepestDescentSolver()

sampleset_qpu = sampler.sample_ising(h, J, \
                                     num_reads=100, \
                                     answer_mode='raw', \
                                     label='SDK Examples - Postprocessing')

dwave.inspector.show(sampleset_qpu)
# Postprocess
sampleset_pp = solver_greedy.sample_ising(h, J, initial_states=sampleset_qpu)

import matplotlib.pyplot as plt    

plt.plot(list(range(100)), sampleset_qpu.record.energy, 'b.-',
                           sampleset_pp.record.energy, 'r^-') 
plt.legend(['QPU samples', 'Postprocessed Samples'])          
plt.xlabel("Sample")    
plt.ylabel("Energy")    
plt.show() 