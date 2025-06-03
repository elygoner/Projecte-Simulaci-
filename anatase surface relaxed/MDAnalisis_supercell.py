import MDAnalysis as mda
import numpy as np

# Parameters
xyz_file = "relaxation.xyz"
nx, ny, nz = 2, 2, 1  # how many times to replicate in x, y, z
a, b, c = 3.78, 3.78, 9.62  # lattice dimensions in Å
headspace = 10.0  # vertical space in z

# Load structure
u = mda.Universe(xyz_file, format='XYZ')
atoms = u.atoms

# Collect replicated positions
replicated_positions = []
replicated_types = []

for ix in range(nx):
    for iy in range(ny):
        for iz in range(nz):
            shift = np.array([ix * a, iy * b, iz * c + headspace])
            for atom in atoms:
                replicated_positions.append(atom.position + shift)
                replicated_types.append(atom.name)

# Create new Universe for writing
n_atoms_total = len(replicated_types)

with open("anataseSC.xyz", "w") as out:
    out.write(f"{n_atoms_total}\n")
    out.write(f"Supercell {nx}x{ny}x{nz}, with headspace {headspace:.1f} Å\n")
    for atom_type, pos in zip(replicated_types, replicated_positions):
        out.write(f"{atom_type} {pos[0]:.5f} {pos[1]:.5f} {pos[2]:.5f}\n")
