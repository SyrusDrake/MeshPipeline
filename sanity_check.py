import pymeshlab

ms = pymeshlab.MeshSet()

input_mesh = 'test_cloud'

depth: int = 9  # Default is 8, max recommended is 12
pointweight: float = 5.0  # Default is 4.0
preclean: bool = False  # Default is False


ms.load_new_mesh(f"{input_mesh}.ply")
print("Mesh loaded.")


ms.generate_surface_reconstruction_screened_poisson(
    depth=9, pointweight=5.000000)

print(
    f"Surface reconstruction completed for depth {depth} and point weight {pointweight}.")

ms.save_current_mesh(
    f"output/{input_mesh}_sanity_check.ply", binary=False, save_vertex_quality=True)
print("Reconstructed mesh saved.")
