import numpy as np
from qiskit import *
from qiskit.quantum_info.operators import Operator
import csv

# Declare input range
i = np.arange(0.0, 1.01, 0.05)
weights = np.arange(0.0, 0.51, 0.125)

# Declare outputs
z = np.zeros((len(weights) * len(weights), i.size, i.size))

def ccry(theta):
  return Operator([
    [1, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 0, 0, 0, 0, 0, 0],
    [0, 0, 1, 0, 0, 0, 0, 0],
    [0, 0, 0, np.cos(theta/2), 0, 0, 0, -np.sin(theta/2)],
    [0, 0, 0, 0, 1, 0, 0, 0],
    [0, 0, 0, 0, 0, 1, 0, 0],
    [0, 0, 0, 0, 0, 0, 1, 0],
    [0, 0, 0, np.sin(theta/2), 0, 0, 0, np.cos(theta/2)],
  ])

def cry(theta):
  return Operator([
    [1, 0, 0, 0,],
    [0, 1, 0, 0,],
    [0, 0, np.cos(theta/2), -np.sin(theta/2)],
    [0, 0, np.sin(theta/2), np.cos(theta/2)],
  ])

# Calculate outputs
for ix, x in enumerate(i):
  for iy, y in enumerate(i):
    for ip, pre in enumerate(weights):
        imp = 0.5 - pre
        ### Quantum implication type 2C-2Z
        qbits = QuantumRegister(3)
        out = ClassicalRegister(1)
        circ = QuantumCircuit(qbits, out)

        circ.ry(x * np.pi, qbits[0])
        circ.ry(y * np.pi, qbits[1])
        circ.cry(np.pi * pre, qbits[0], qbits[2])
        circ.cry(np.pi * imp, qbits[1], qbits[2])
        circ.z(qbits[2])
        circ.cry(-np.pi * pre, qbits[0], qbits[2])
        circ.cry(-np.pi * imp, qbits[1], qbits[2])
        circ.z(qbits[2])
        circ.measure(qbits[2], out[0])

        aer_sim = Aer.get_backend('aer_simulator')
        job = aer_sim.run(circ.decompose(reps=1), shots=10000)
        hist = job.result().get_counts()
        try:
          z[ip][ix][iy] = hist['1']/10000
        except KeyError:
          z[ip][ix][iy] = 0

# Prepare data
tags = [
  'a',
  'b',
]

for pre in weights:
    tags.append('2C_2Z_{:.2f}_{:.2f}'.format(pre, 0.5 - pre))

print(len(tags))

with open('data/data_2c2z_imp.csv', 'w', encoding='UTF8') as f:
    writer = csv.writer(f, quoting=csv.QUOTE_NONE)

    # write the header
    writer.writerow(tags)

    # write the data
    for ix, x in enumerate(i):
      for iy, y in enumerate(i):
        data = []
        data.append(x)
        data.append(y)
        for ip, _ in enumerate(weights):
              data.append(z[ip][ix][iy])
        writer.writerow(['{:.5f}'.format(d) for d in data])