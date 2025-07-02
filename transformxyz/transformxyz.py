import MDAnalysis as mda
import numpy as np
import sisl as sl


n=12
p = sl.get_sile(f"AuR_{n}.xyz").read_geometry()

lattice = [
    [20, 0.000, 0.000],  # a1
    [0.000, 20, 0.000],  # a2
    [0.000, 0.000, 20]   # a3
]
p.set_lattice(lattice)

p.write(f"AuR_{n}.fdf")
