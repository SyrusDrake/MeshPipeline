import pymeshlab

ms = pymeshlab.MeshSet()

input_mesh = 'test_cloud'

depth: int = 8  # Default is 8, max recommended is 12
pointweight: float = 4.0  # Default is 4.0
preclean: bool = False  # Default is False


ms.load_new_mesh(f"{input_mesh}.ply")
print("Mesh loaded.")

# Iterate over a range of depth and pointweight values
for i in range(10, 11):
    # Depths are increased in steps of 1

    depth = i

    for j in range(10, 16, 5):
        """
        IMPORTANT!
        Point weights are increaseed in steps of 0.5, however, since floats cannot be used in the file name, they are multiplied by 10.
        Thus, a point weight of 0.5 is represented as 5 in the file name.       
        """
        ms.set_current_mesh(
            0)  # Reset to the original import mesh before each reconstruction, otherwise, the previous reconstruction will be used as the input for the next one.
        # Converting j to the actual point weight by dividing by 10. (See IMPORTANT note above)
        pointweight = j / 10.0
        ms.generate_surface_reconstruction_screened_poisson(depth=depth,
                                                            pointweight=pointweight,
                                                            preclean=preclean)
        print(
            f"Surface reconstruction completed for depth {depth} and point weight {pointweight}.")

        # Save the reconstructed mesh with parameters in the filename. Note that the vertex quality is not calculated as of now, the function will be added later.
        ms.save_current_mesh(
            f"output/{input_mesh}(d{depth}_pw{j}_pc{preclean}).ply", binary=False, save_vertex_quality=True)
        print("Reconstructed mesh saved.")
