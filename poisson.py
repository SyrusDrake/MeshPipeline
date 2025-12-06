import pymeshlab
from csv import writer
from os import stat

ms = pymeshlab.MeshSet()

input_mesh = 'test_cloud'

depth: int = 8  # Default is 8, max recommended is 12
pointweight: float = 4.0  # Default is 4.0
preclean: bool = False  # Default is False
mesh_statistics = {}


ms.load_new_mesh(f"{input_mesh}.ply")
print("Mesh loaded.")

# Iterate over a range of depth and pointweight values
for i in range(9, 10):
    # Depths are increased in steps of 1

    depth = i

    for j in range(0, 16, 5):
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

        ms.compute_scalar_by_distance_from_another_mesh_per_vertex(
            measuremesh=ms.current_mesh_id(), refmesh=0)
        print("Distance computation completed.")

        # Save the reconstructed mesh with parameters in the filename. Note that the vertex quality is not calculated as of now, the function will be added later.
        meshname = f"d{depth}_pw{(j)}_pc{preclean}"

        ms.save_current_mesh(
            f"output/{input_mesh}({meshname}).ply", binary=False, save_vertex_quality=True)
        print("Reconstructed mesh saved.")

        filesize = (stat(f"output/{input_mesh}({meshname}).ply").st_size)/1024

        mesh_statistics[meshname] = ms.get_scalar_statistics_per_vertex()
        mesh_statistics[meshname]['d'] = depth
        mesh_statistics[meshname]['p'] = pointweight
        mesh_statistics[meshname]['c'] = str(preclean).lower()
        mesh_statistics[meshname]['size_kb'] = filesize

with open('data.csv', 'w', newline='') as file:
    writer = writer(file)
    writer.writerow(['Mesh',
                     'Average', 'Max', 'Median', 'Min', 'StdDev', 'Variance', 'Depth', 'Pointweight', 'Preclean', 'Size_KB'])
    for key, value in mesh_statistics.items():
        writer.writerow([key,
                         value['avg'],
                         value['max'],
                         value['med'],
                         value['min'],
                         value['stddev'],
                         value['variance'],
                         value['d'],
                         value['p'],
                         value['c'],
                         value['size_kb']])

print('done')
