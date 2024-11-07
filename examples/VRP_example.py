


from dwave.system import DWaveSampler, EmbeddingComposite
from greedy import SteepestDescentSolver
import dwave.inspector
import dimod
sampler = EmbeddingComposite(DWaveSampler(token="DEV-edba7dbb3a72fc17fe9561831ed5792ddea6c5b2"))
Q = {**linear_dict, **quadratic_dict}
print("Q dictionary structure:")
for key, value in Q.items():
    print(key, value)
bqm = dimod.BinaryQuadraticModel.from_qubo(Q)
sampleset_qc = sampler.sample(bqm, num_reads=500, chain_strength=500000)
print("Original sampleset from quantum computer:")
print(sampleset_qc)
dwave.inspector.show(sampleset_qc)
solver_greedy = SteepestDescentSolver()
sampleset_pp = solver_greedy.sample(bqm, initial_states=sampleset_qc)
print("Post-processed sampleset using SteepestDescentSolver:")
print(sampleset_pp)

