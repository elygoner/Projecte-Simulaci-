import MDAnalysis as mda
import sisl as sl
import numpy as np

# Parameters
file1 = "SurRel.xyz"
file2 = "AuRel.xyz"
nx, ny, nz = 1, 4, 2  # how many times to replicate in x, y, z
a, b, c = 3.78, 3.78, 9.62  # lattice dimensions in Å
headspace = 0 # vertical space in z


# Load structure
u = mda.Universe(file1, format='XYZ')
atoms = u.atoms

replicated_positions1 = []
replicated_types1 = []

for i in atoms:
    if i.position[0] > 2*a:
        replicated_positions1.append(i.position - np.array([2*a,0,0]))
        replicated_types1.append(i.name)

# Collect replicated positions
replicated_positions2 = []
replicated_types2 = []
for ix in range(nx):
    for iy in range(ny):
        for iz in range(nz):
            shift = np.array([ix * a, iy * b, iz * c ])
            for i in range(len(replicated_positions1)):
                replicated_positions2.append(replicated_positions1[i] + shift)
                replicated_types2.append(replicated_types1[i])

p = mda.Universe(file2, format='XYZ')
patoms = p.atoms
for i in patoms:
    replicated_positions2.append(i.position + np.array([a+0.5, b, 4]))
    replicated_types2.append(i.name)

# Create new Universe for writing
n_atoms_total = len(replicated_types2)

with open("ana_w_particle.xyz", "w") as out:
    out.write(f"{n_atoms_total}\n")
    out.write(f"Supercell {nx}x{ny}x{nz}\n")
    for atom_type, pos in zip(replicated_types2, replicated_positions2):
        out.write(f"{atom_type} {pos[0]:.5f} {pos[1]:.5f} {pos[2]:.5f}\n")

p = sl.get_sile("ana_w_particle.xyz").read_geometry()

lattice = [
    [a* nx+10, 0.000, 0.000],  # a1
    [0.000, b*ny, 0.000],  # a2
    [0.000, 0.000, c*nz]   # a3
]
p.set_lattice(lattice)

p.write("ana_w_particle.fdf")

