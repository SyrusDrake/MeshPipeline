import pymeshlab
import csv

ms = pymeshlab.MeshSet()

input_mesh = ms.load_new_mesh("test_cloud.ply")

comparison_mesh = ms.load_new_mesh("comparison_mesh.ply")

depth: int = 9
pointweight: float = 0.0
preclean: bool = False
scalar_statistics = {}

print("Meshes loaded.")

ms.compute_scalar_by_distance_from_another_mesh_per_vertex(
    measuremesh=1, refmesh=0)
print("Distance computation completed.")

ms.save_current_mesh(
    f"output/quality_scalar.ply", binary=False, save_vertex_quality=True)
print("Reconstructed mesh saved.")
print(ms.current_mesh_id())

meshname = f"d{depth}_pw{int(pointweight*10)}_pc{preclean}"
scalar_statistics[meshname] = ms.get_scalar_statistics_per_vertex()
scalar_statistics[meshname]['d'] = depth
scalar_statistics[meshname]['p'] = pointweight
scalar_statistics[meshname]['c'] = str(preclean).lower()

with open('data.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Mesh',
                     'Average', 'Max', 'Median', 'Min', 'StdDev', 'Variance', 'Depth', 'Pointweight', 'Preclean',])
    writer.writerow([meshname,
                     scalar_statistics[meshname]['avg'],
                     scalar_statistics[meshname]['max'],
                     scalar_statistics[meshname]['med'],
                     scalar_statistics[meshname]['min'],
                     scalar_statistics[meshname]['stddev'],
                     scalar_statistics[meshname]['variance'],
                     scalar_statistics[meshname]['d'],
                     scalar_statistics[meshname]['p'],
                     scalar_statistics[meshname]['c'],])

print(scalar_statistics)
