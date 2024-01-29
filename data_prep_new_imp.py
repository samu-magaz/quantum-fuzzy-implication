import numpy as np
from qiskit import *
from qiskit.quantum_info.operators import Operator
import csv

# Declare input range
i = np.arange(0.0, 1.01, 0.05)

# Declare outputs
z = np.zeros((4, i.size, i.size))

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
    
    ### Quantum implication type 1CC-2Z
    qbits = QuantumRegister(3)
    out = ClassicalRegister(1)
    circ = QuantumCircuit(qbits, out)

    circ.ry(x * np.pi, qbits[0])
    circ.ry(y * np.pi, qbits[1])
    circ.append(ccry(np.pi / 2), [qbits[0], qbits[1], qbits[2]])
    circ.z(qbits[2])
    circ.append(ccry(-np.pi / 2), [qbits[0], qbits[1], qbits[2]])
    circ.z(qbits[2])
    # circ.ccx(qbits[0], qbits[1], qbits[2])
    circ.measure(qbits[2], out[0])

    aer_sim = Aer.get_backend('aer_simulator')
    job = aer_sim.run(circ, shots=10000)
    hist = job.result().get_counts()
    try:
      z[0][ix][iy] = hist['1']/10000
    except KeyError:
      z[0][ix][iy] = 0
    
    ### Quantum implication type 2C-2Z
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
      z[1][ix][iy] = hist['1']/10000
    except KeyError:
      z[1][ix][iy] = 0
    
    ### Quantum implication type 2C-2Z'
    qbits = QuantumRegister(3)
    out = ClassicalRegister(1)
    circ = QuantumCircuit(qbits, out)

    circ.ry(x * np.pi, qbits[0])
    circ.ry(y * np.pi, qbits[1])
    circ.cry(np.pi / 2, qbits[0], qbits[2])
    circ.cry(np.pi / 2, qbits[1], qbits[2])
    circ.z(qbits[2])
    circ.cry(-np.pi / 2, qbits[0], qbits[2])
    circ.cry(-np.pi / 2, qbits[1], qbits[2])
    circ.z(qbits[2])
    circ.x(qbits[2])
    circ.measure(qbits[2], out[0])

    aer_sim = Aer.get_backend('aer_simulator')
    job = aer_sim.run(circ.decompose(reps=1), shots=10000)
    hist = job.result().get_counts()
    try:
      z[2][ix][iy] = hist['1']/10000
    except KeyError:
      z[2][ix][iy] = 0
    
    ### Quantum implication type 2C-4S
    qbits = QuantumRegister(3)
    out = ClassicalRegister(1)
    circ = QuantumCircuit(qbits, out)

    circ.ry(x * np.pi, qbits[0])
    circ.ry(y * np.pi, qbits[1])
    circ.cry(np.pi / 4, qbits[0], qbits[2])
    circ.s(qbits[2])
    circ.cry(np.pi / 4, qbits[1], qbits[2])
    circ.s(qbits[2])
    circ.cry(-np.pi / 4, qbits[0], qbits[2])
    circ.s(qbits[2])
    circ.cry(-np.pi / 4, qbits[1], qbits[2])
    circ.s(qbits[2])
    circ.measure(qbits[2], out[0])

    aer_sim = Aer.get_backend('aer_simulator')
    job = aer_sim.run(circ.decompose(reps=1), shots=10000)
    hist = job.result().get_counts()
    try:
      z[3][ix][iy] = hist['1']/10000
    except KeyError:
      z[3][ix][iy] = 0

# Prepare data
tags = [
  'a',
  'b',
  '1CC_2Z',
  '2C_2Z',
  '2C_2Z\'',
  '2C_4S',
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
        for n in range(4):
          data.append(z[n][ix][iy])
        writer.writerow(['{:.5f}'.format(d) for d in data])