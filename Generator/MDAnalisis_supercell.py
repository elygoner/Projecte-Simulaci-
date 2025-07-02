import MDAnalysis as mda
import numpy as np
import sisl as sl

# Parameters
xyz_file = "Au.xyz"
n_atoms = 12
a, b, c = 4.17128853, 4.17128853, 4.17128853

# Load structure
u = mda.Universe(xyz_file, format='XYZ')
atoms = u.atoms

# Collect replicated positions

replicated_positions = []
replicated_types = []

x=[0,0,0,0,1,1,0,0,1,0,1,0]
y=[0,0,0,0,1,0,1,0,0,0,1,1]
z=[0,0,0,0,1,0,0,1,0,1,1,0]

for atom in range(n_atoms):
    replicated_positions.append(atoms[atom%4].position + np.array([a*x[atom], b*y[atom], c*z[atom]]))
    replicated_types.append('Au')


# Create new Universe for writing
n_atoms_total = len(replicated_types)

with open("au_mid.xyz", "w") as out:
    out.write(f"{n_atoms_total}\n")
    out.write(f"Supercell {a}x{b}x{c}\n")
    for atom_type, pos in zip(replicated_types, replicated_positions):
        out.write(f"{atom_type} {pos[0]:.5f} {pos[1]:.5f} {pos[2]:.5f}\n")

p = sl.get_sile("au_mid.xyz").read_geometry()

lattice = [
    [20, 0.000, 0.000],  # a1
    [0.000, 20, 0.000],  # a2
    [0.000, 0.000, 20]   # a3
]
p.set_lattice(lattice)

p.write(f"Au_{n_atoms}.fdf")
