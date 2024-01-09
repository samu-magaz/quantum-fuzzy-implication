import numpy as np
from qiskit import *
import csv

# Declare input range
i = np.arange(0.0, 1.01, 0.05)

# Declare implications to test
implications = np.array([
  lambda a,b: min(1, 1 - a + b),    # Lukasiewicz
  lambda a,b: max(1 - a, b),        # Kleene
  lambda a,b: 1 - a + a * b,        # Reichenbach
  lambda a,b: max(1 - a, min(a,b)), # Zadeh
  lambda a,b: 1 if a <= b else b,   # Gödel
])

# Declare outputs
z = np.zeros((implications.size + 3, i.size, i.size))

# Calculate outputs
for ix, x in enumerate(i):
  for iy, y in enumerate(i):
    # For each t-norm
    for ip, imp in enumerate(implications):
      z[ip][ix][iy] = imp(x, y)
    
    ### Quantum implication type S
    qbits = QuantumRegister(3)
    out = ClassicalRegister(1)
    circ = QuantumCircuit(qbits, out)

    circ.ry(np.pi*x, qbits[0])
    circ.ry(np.pi*y, qbits[1])
    circ.x(qbits[0])
    circ.x(qbits[0])                        
    circ.x(qbits[1])
    circ.ccx(qbits[0], qbits[1], qbits[2])
    circ.x(qbits[0])
    circ.x(qbits[1])
    circ.x(qbits[2])
    circ.measure(qbits[2], out[0])

    aer_sim = Aer.get_backend('aer_simulator')
    job = aer_sim.run(circ, shots=10000)
    hist = job.result().get_counts()
    try:
      z[len(implications)][ix][iy] = hist['1']/10000
    except KeyError:
      z[len(implications)][ix][iy] = 0
    
    ### Quantum implication type QL
    qbits = QuantumRegister(4)
    out = ClassicalRegister(1)
    circ = QuantumCircuit(qbits, out)

    circ.ry(np.pi*x, qbits[0])
    circ.ry(np.pi*y, qbits[1])
    circ.ccx(qbits[0], qbits[1], qbits[2])
    circ.x(qbits[0])
    circ.x(qbits[0])
    circ.x(qbits[2])
    circ.ccx(qbits[0], qbits[2], qbits[3])
    circ.x(qbits[0])
    circ.x(qbits[2])
    circ.x(qbits[3])
    circ.measure(qbits[3], out[0])

    aer_sim = Aer.get_backend('aer_simulator')
    job = aer_sim.run(circ, shots=10000)
    hist = job.result().get_counts()
    try:
      z[len(implications) + 1][ix][iy] = hist['1']/10000
    except KeyError:
      z[len(implications) + 1][ix][iy] = 0
    
    ### Quantum implication type R
    c_values = np.sin(np.arange(0.0, np.pi, 0.001))
    f_ac = np.zeros((c_values.size))
    for ic, c in enumerate(c_values):
      qbits = QuantumRegister(3)
      out = ClassicalRegister(1)
      circ = QuantumCircuit(qbits, out)

      circ.ry(np.pi*x, qbits[0])
      circ.ry(np.pi*c, qbits[1])
      circ.ccx(qbits[0], qbits[1], qbits[2])
      circ.measure(qbits[2], out[0])

      aer_sim = Aer.get_backend('aer_simulator')
      job = aer_sim.run(circ, shots=10000)
      hist = job.result().get_counts()
      try:
        f_ac[ic] = hist['1']/10000
      except KeyError:
        f_ac[ic] = 0
    try:
      z[len(implications) + 2][ix][iy] = np.max(c_values[f_ac <= y])
    except ValueError:
      z[len(implications) + 2][ix][iy] = 0

# Prepare data
tags = [
  'a',
  'b',
  'lukasiewicz',
  'kleene',
  'reichenbach',
  'zadeh',
  'godel',
  'quantum_S',
  'quantum_QL',
  'quantum_R',
]

with open('data/data_imp.csv', 'w', encoding='UTF8') as f:
    writer = csv.writer(f, quoting=csv.QUOTE_NONE)

    # write the header
    writer.writerow(tags)

    # write the data
    for ix, x in enumerate(i):
      for iy, y in enumerate(i):
        data = []
        data.append(x)
        data.append(y)
        for ip, _ in enumerate(implications):
          data.append(z[ip][ix][iy])
        data.append(z[len(implications)][ix][iy])
        data.append(z[len(implications) + 1][ix][iy])
        data.append(z[len(implications) + 2][ix][iy])
        writer.writerow(['{:.5f}'.format(d) for d in data])