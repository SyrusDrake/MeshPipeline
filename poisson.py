import pymeshlab
from csv import writer
from os import stat
import itertools

ms = pymeshlab.MeshSet()

input_mesh = 'test_cloud'

depth: int  # Default is 8, max recommended is 12
depth_range = range(4, 6)
pointweight: float  # Default is 4.0
pointweight_range = range(0, 41, 5)  # From 0.0 to 4.0 in steps of 0.5
preclean: bool = False  # Default is False
mesh_statistics = {}


ms.load_new_mesh(f"{input_mesh}.ply")
print("Mesh loaded.")

# Iterate over a range of depth and pointweight values
for pointweight, depth, preclean in itertools.product(pointweight_range, depth_range, [False, True]):

    ms.set_current_mesh(
        0)  # Reset to the original import mesh before each reconstruction, otherwise, the previous reconstruction will be used as the input for the next one.

    ms.generate_surface_reconstruction_screened_poisson(depth=depth,
                                                        pointweight=pointweight/10,
                                                        preclean=preclean)
    print(
        f"Surface reconstruction completed for depth {depth} and point weight {pointweight/10}.")

    ms.compute_scalar_by_distance_from_another_mesh_per_vertex(
        measuremesh=ms.current_mesh_id(), refmesh=0)
    print("Distance computation completed.")

    # Save the reconstructed mesh with parameters in the filename.
    meshname = f"d{depth}_pw{(pointweight)}_pc{preclean}"

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
