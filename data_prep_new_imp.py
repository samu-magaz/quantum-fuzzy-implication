import numpy as np
from qiskit import *
import csv

# Declare input range
i = np.arange(0.0, 1.01, 0.05)

# Declare outputs
z = np.zeros((i.size, i.size))

# Calculate outputs
for ix, x in enumerate(i):
  for iy, y in enumerate(i):
    
    ### Quantum implication type S
    qbits = QuantumRegister(3)
    out = ClassicalRegister(1)
    circ = QuantumCircuit(qbits, out)

    circ.ry(x * np.pi, qbits[0])
    circ.ry(y * np.pi, qbits[1])
    circ.cry(np.pi / 4, qbits[0], qbits[2])
    circ.cry(np.pi / 4, qbits[1], qbits[2])
    circ.z(qbits[2])
    circ.cry(-np.pi / 4, qbits[0], qbits[2])
    circ.cry(-np.pi / 4, qbits[1], qbits[2])
    circ.z(qbits[2])
    circ.measure(qbits[2], out[0])

    aer_sim = Aer.get_backend('aer_simulator')
    job = aer_sim.run(circ.decompose(reps=1), shots=10000)
    hist = job.result().get_counts()
    try:
      z[ix][iy] = hist['1']/10000
    except KeyError:
      z[ix][iy] = 0

# Prepare data
tags = [
  'a',
  'b',
  'new_imp',
]

with open('data/data_new_imp.csv', 'w', encoding='UTF8') as f:
    writer = csv.writer(f, quoting=csv.QUOTE_NONE)

    # write the header
    writer.writerow(tags)

    # write the data
    for ix, x in enumerate(i):
      for iy, y in enumerate(i):
        data = []
        data.append(x)
        data.append(y)
        data.append(z[ix][iy])
        writer.writerow(['{:.5f}'.format(d) for d in data])