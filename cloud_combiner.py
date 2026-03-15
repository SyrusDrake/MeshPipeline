import pymeshlab
from os import listdir, makedirs, path
import argparse

# ver.: 1.0.0
# last updated: 2026-03-15

# Folder containing the individual scan clouds, one folder per group.
object_folder: str = "cloud_input"

# List of all groups/scan passes that make up the object. These are folders.
scan_passes: list[str]

# All the individual scan clouds belonging to one group/pass (e.g. all ply files in folder 00, 01, etc.)
group_clouds: dict[str, list[str]] = {}

# Name of the object being processed
object_name: str = "scanned_object"

# MeshSet to hold all combined groups
object_set = pymeshlab.MeshSet()

# Set up command-line argument parsing

parser = argparse.ArgumentParser(
    description="Combine individual scan clouds into a single mesh.")
parser.add_argument("object_name", type=str,
                    help="The name of the object being processed. This will be used for naming the output files and folder.")
parser.add_argument(
    "--input-folder", type=str, default=object_folder, help="The input folder containing all the groups, which contain ply files. Defaults to 'cloud_input'."
)
parser.add_argument("--output-folder", type=str, default=object_name,
                    help="The output folder where the combined meshes will be saved. Defaults to 'output'.")
args = parser.parse_args()

object_name = args.object_name
object_folder = args.input_folder
output_folder = args.output_folder

print(f"Processing object: {object_name}")
print(f"Input folder: {object_folder}")
print(f"Output folder: {output_folder}")

# Check if the input folder exists and contains groups
try:
    scan_passes = listdir(f"./{object_folder}")
    if not scan_passes:
        print(
            f"No groups found in the input folder '{object_folder}'. Exiting.")
        exit(1)
except FileNotFoundError:
    print(f"Input folder '{object_folder}' not found. Exiting.")
    exit(1)

# Check if the output folder exists, if not create it
if not path.exists(f"./{output_folder}"):
    makedirs(f"./{output_folder}")
    print(f"Created output folder '{output_folder}'.")
else:
    print(
        f"Output folder '{output_folder}' already exists. Files may be overwritten.")


def combine_group_clouds(group_name: str, group_clouds: list[str], group_identifier: str) -> str:
    """Combines all individual scan clouds of a group into a single mesh and saves it as a PLY file.
    Args:
        group_name (str): Name of the group being processed. (Usually 00, 01, etc.)
        group_clouds (list[str]): List of individual scan cloud filenames belonging to the group. These are ply files.
        group_identifier (str): Identifier for the group being processed.
    Returns:
        str: The file path where the combined group mesh is saved.
    """

    # MeshSet to hold all clouds of the current group
    group_set = pymeshlab.MeshSet()

    # Adds each ply to the MeshSet, so it can be used by MeshLab.
    for cloud in group_clouds:
        group_set.load_new_mesh(f"./{object_folder}/{group_name}/{cloud}")

    print(f"Loaded {len(group_clouds)} clouds from group {group_name}.")

    # Turns all the imported clouds into a single mesh"
    group_set.generate_by_merging_visible_meshes()
    print("Merged group clouds into single mesh.")

    # Rename to group name/index
    group_set.set_mesh_name(newname=str(group_identifier))

    # export group as ply
    group_set.save_current_mesh(
        f"./{output_folder}/{object_name}_({group_identifier}).ply", binary=False)
    print(
        f"Exported combined clouds as {object_name}_({group_identifier}).ply")

    return f"./{output_folder}/{object_name}_({group_identifier}).ply"


# Get list of all groups making up the object, lists them
scan_passes = listdir(f"./{object_folder}")

# Prepares a dictionary to hold the individual scan clouds of each group, lists the groups
for group in scan_passes:
    group_clouds[group] = listdir(f"./{object_folder}/{group}")

print("The following groups and ply files were found:")
for group, clouds in group_clouds.items():
    print(f"{group}: {clouds}")

for name, clouds in group_clouds.items():
    group_mesh_path = combine_group_clouds(name, clouds, name)
    object_set.load_new_mesh(group_mesh_path)

print("All groups combined into single object mesh.")

# Merge all group meshes into a single mesh representing the entire object
object_set.generate_by_merging_visible_meshes()

# Export the combined object mesh as one ply file
object_set.save_current_mesh(
    f"./{output_folder}/{object_name}_combined.ply", binary=False)

print("Combined mesh saved as " +
      f"./{output_folder}/{object_name}_combined.ply")

print("Done.")
