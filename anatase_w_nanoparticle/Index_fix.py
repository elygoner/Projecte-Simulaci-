def extract_geometry_constraints(fdf_file, x_threshold):
    with open(fdf_file, "r") as f:
        lines = f.readlines()

    # Find block boundaries
    try:
        start = lines.index('%block AtomicCoordinatesAndAtomicSpecies\n') + 1
        end = lines.index('%endblock AtomicCoordinatesAndAtomicSpecies\n')
    except ValueError:
        print("Could not find AtomicCoordinatesAndAtomicSpecies block.")
        return

    constraints = []
    for i, line in enumerate(lines[start:end], start=1):
        if line.strip() == "":
            continue
        parts = line.split()
        x = float(parts[0])
        if x < x_threshold:
            constraints.append(f"atom {i} position  fixed")

    # Output the GeometryConstraints block
    if constraints:
        print("%block GeometryConstraints")
        for constraint in constraints:
            print(constraint)
        print("%endblock GeometryConstraints")
    else:
        print("No atoms found with x <", x_threshold)

fdf_filename = "ana_w_particle.fdf"  # Replace this with your actual filename
x_cutoff = 3.78  # Change threshold as needed
extract_geometry_constraints(fdf_filename, x_cutoff)
