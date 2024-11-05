from dwave.system import DWaveSampler, EmbeddingComposite
from greedy import SteepestDescentSolver
import dwave.inspector
import dimod

# Initialize D-Wave sampler
sampler = EmbeddingComposite(DWaveSampler(token="DEV-edba7dbb3a72fc17fe9561831ed5792ddea6c5b2"))

# Define the QUBO problem
linear = {('a', 'a'): -1, ('b', 'b'): -1, ('c', 'c'): -1}
quadratic = {('a', 'b'): 2, ('b', 'c'): 2, ('a', 'c'): 2}
Q = {**linear, **quadratic}

# Sample on D-Wave
sampleset_qc = sampler.sample_qubo(Q, num_reads=5000)
print("Original sampleset from quantum computer:")
print(sampleset_qc)
dwave.inspector.show(sampleset_qc)

# Convert QUBO dictionary to a BinaryQuadraticModel (BQM)
bqm = dimod.BinaryQuadraticModel.from_qubo(Q)

# Initialize the SteepestDescentSolver
solver_greedy = SteepestDescentSolver()

# Post-process the samples from the quantum sampler
sampleset_pp = solver_greedy.sample(bqm, initial_states=sampleset_qc)

print("Post-processed sampleset using SteepestDescentSolver:")
print(sampleset_pp)

