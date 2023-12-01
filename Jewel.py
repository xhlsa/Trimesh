import trimesh
import numpy as np

def create_oval_mesh(length, width, height, divisions):
    # Create an ellipsoid and scale it to get an oval shape
    mesh = trimesh.creation.icosphere(subdivisions=divisions)
    mesh.apply_scale([length, width, height])

    # Flatten the top and bottom to create flat surfaces
    max_z = np.max(mesh.vertices[:, 2])
    min_z = np.min(mesh.vertices[:, 2])
    mesh.vertices[mesh.vertices[:, 2] == max_z, 2] = max_z * 0.95
    mesh.vertices[mesh.vertices[:, 2] == min_z, 2] = min_z * 0.95

    return mesh

def add_chamfer_refractions(mesh, chamfer_ratio):
    # Iterate through each edge and create chamfers
    edges = mesh.edges_unique
    for edge in edges:
        edge_midpoint = np.mean(mesh.vertices[mesh.edges_unique[edge]], axis=0)
        mesh.vertices[mesh.edges_unique[edge]] = (
            mesh.vertices[mesh.edges_unique[edge]] * (1 - chamfer_ratio) + 
            edge_midpoint * chamfer_ratio
        )
    return mesh

# Parameters for the jewel
length = 1.0
width = 0.5
height = 0.3
divisions = 3
chamfer_ratio = 0.1

# Create the jewel mesh
jewel_mesh = create_oval_mesh(length, width, height, divisions)
jewel_mesh = add_chamfer_refractions(jewel_mesh, chamfer_ratio)

# Export the mesh
jewel_mesh.export('many_faced_jewel.stl')

# For visualization in notebook
jewel_mesh.show()
