import pymeshlab
from csv import writer as writer
from os import stat, path
import itertools
from pathlib import Path

"""The following variables are not used in practices, but remain included for testing, if necessary."""

input_mesh: str  # Path to input mesh without extension

depth: int  # Default is 8, max recommended is 12
depth_range = range(4, 6)
pointweight: float  # Default is 4.0
pointweight_range = range(0, 41, 5)  # From 0.0 to 4.0 in steps of 0.5
preclean: bool = False  # Default is False


def mesh_analysis(input_mesh_path: str, depth_min: int, depth_max: int, pointweight_min: int, pointweight_max: int, output_folder: str = "./output", save_mesh: bool = True, create_csv: bool = True, csv_filename: str = "data.csv"):
    """
    Performs a Poisson surface reconstruction on the input mesh over a range of depth and pointweight values, computes distance to reference as vertex quality, saves the resulting meshes, and generates a CSV file with statistics.

    :param input_mesh_path: The complete file path to the input mesh.
    :type input_mesh_path: str

    :param depth_min: Minimum depth value for Poisson reconstruction.
    :type depth_min: int
    :param depth_max: Maximum depth value for Poisson reconstruction (inclusive).
    :type depth_max: int

    :param pointweight_min: Minimum pointweight value for Poisson reconstruction. Note that the input is divided by 10 for the actual reconstruction (and is thus a float), but is required as an integer for the file name.
    :type pointweight_min: int
    :param pointweight_max: Maximum pointweight value for Poisson reconstruction (inclusive).
    :type pointweight_max: int

    :param output_folder: Folder where output files will be saved. Default is "./output".
    :type output_folder: str

    :param save_mesh: Whether to save the reconstructed meshes. Default is True.
    :type save_mesh: bool

    :param create_csv: Whether to create a CSV file with mesh statistics. Default is True.
    :type create_csv: bool

    :param csv_filename: Name of the CSV file to be created. Default is "data.csv".
    :type csv_filename: str
    """

    # Create output folder if it doesn't exist
    Path(output_folder).mkdir(parents=True, exist_ok=True)

    mesh_statistics = {}  # Dictionary to hold statistics for each mesh
    # Turning the min and max values into a range
    depth_range = range(depth_min, depth_max + 1)
    pointweight_range = range(int(pointweight_min*10),
                              int((pointweight_max*10)+1), 5)  # Turning the min and max values into a range
    # Get the name of the input mesh without file path and extension
    input_mesh_name = path.basename(input_mesh_path)[:-4]

    # This keeps throwing an error, I don't know why, but it still works.
    ms = pymeshlab.MeshSet()

    ms.load_new_mesh(input_mesh_path)
    print("Mesh loaded.")

    if create_csv:
        # Store dict into a CSV file
        with open(f"{output_folder}/{csv_filename}", 'w', newline='') as file:
            file_writer = writer(file)
            file_writer.writerow(['Mesh',
                                  'Average', 'Max', 'Median', 'Min', 'StdDev', 'Variance', 'Depth', 'Pointweight', 'Preclean', 'Size_KB', 'Faces'])

    # Iterate over a range of depth and pointweight values
    for pointweight, depth in itertools.product(pointweight_range, depth_range):

        ms.set_current_mesh(
            0)  # Reset to the original import mesh before each reconstruction, otherwise, the previous reconstruction will be used as the input for the next one.

        ms.generate_surface_reconstruction_screened_poisson(depth=depth,
                                                            pointweight=pointweight/10,
                                                            preclean=preclean)  # Perform Poisson surface reconstruction
        print(
            f"Surface reconstruction completed for depth {depth} and point weight {pointweight/10}.")

        ms.compute_scalar_by_distance_from_another_mesh_per_vertex(
            measuremesh=ms.current_mesh_id(), refmesh=0)  # Compute distance to the input cloud as vertex quality
        print("Distance computation completed.")

        # Create a name for the mesh based on current parameters
        meshname = f"d{depth}_pw{(pointweight)}_pc{preclean}"

        if save_mesh:
            # Save the reconstructed mesh with parameters in the filename.
            ms.save_current_mesh(
                f"{output_folder}/{input_mesh_name}({meshname}).ply", binary=False, save_vertex_quality=True)  # Binary false to save as human readable ASCII, save vertex quality to include the calculated distances
            print("Reconstructed mesh saved.")

            filesize = (
                stat(f"{output_folder}/{input_mesh_name}({meshname}).ply").st_size)/1024  # Get file size in KB
        else:
            # If not saving the mesh, set filesize to 0, so that something can be recorded in the CSV.
            filesize = 0

        # Get statistics of the vertex quality (distances)
        mesh_statistics[meshname] = ms.get_scalar_statistics_per_vertex()
        mesh_statistics[meshname]['d'] = depth
        # Store pointweight as the actually used float
        mesh_statistics[meshname]['p'] = pointweight/10
        mesh_statistics[meshname]['c'] = str(preclean).lower()
        mesh_statistics[meshname]['size_kb'] = filesize
        mesh_statistics[meshname]['faces'] = ms.current_mesh(
        ).face_number()  # Store number of faces

        if create_csv:
            # Store dict into a CSV file
            with open(f"{output_folder}/{csv_filename}", 'a', newline='') as file:
                file_writer = writer(file)
                file_writer.writerow([meshname,
                                      mesh_statistics[meshname]['avg'],
                                      mesh_statistics[meshname]['max'],
                                      mesh_statistics[meshname]['med'],
                                      mesh_statistics[meshname]['min'],
                                      mesh_statistics[meshname]['stddev'],
                                      mesh_statistics[meshname]['variance'],
                                      mesh_statistics[meshname]['d'],
                                      mesh_statistics[meshname]['p'],
                                      mesh_statistics[meshname]['c'],
                                      mesh_statistics[meshname]['size_kb'],
                                      mesh_statistics[meshname]['faces']])
    print('done')
