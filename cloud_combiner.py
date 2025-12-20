import pymeshlab
from os import listdir

# Folder containing the individual scan clouds, one folder per group. This might later be selected in a GUI
input_folder: str = "./cloud_input"

# List of all groups/scan passes that make up the object. These might later be selected in a GUI
object_clouds: list[str]

# All the individual scan clouds belonging to one group/pass (e.g. all ply files in folder 00, 01, etc.)
group_clouds: list[str]

object_name: str = "combined_clouds"  # Name of the object being processed

# Index of the group being processed. Unsure if this will be ultimately required, as the folder name may suffice.
group_index: int = 0


object_set = pymeshlab.MeshSet()  # MeshSet to hold all combined groups


def combine_group_clouds(group_name: str, group_clouds: list[str], group_index: int) -> str:
    """Combines all individual scan clouds of a group into a single mesh and saves it as a PLY file.
    Args:
        group_name (str): Name of the group being processed. (Usually 00, 01, etc.)
        group_clouds (list[str]): List of individual scan cloud filenames belonging to the group. These are ply files.
        group_index (int): Index of the group being processed. This should correspond to the group/folder name.
    Returns:
        str: The file path where the combined group mesh is saved.
    """

    group_set = pymeshlab.MeshSet()  # MeshSet to hold all clouds of the current group

    for cloud in group_clouds:
        group_set.load_new_mesh(f"./{input_folder}/{group_name}/{cloud}")

    # Maybe change this into "loaded clouds from group X"
    print(f"Loaded {len(group_clouds)} clouds from group {group_name}.")

    "flatten layers (necessary?). Turns all the imported clouds into a single mesh"

    group_set.generate_by_merging_visible_meshes()
    print("Merged group clouds into single mesh.")

    "rename to group name/index"

    group_set.set_mesh_name(newname=str(group_index))

    "export group as ply"

    group_set.save_current_mesh(
        f"./output/{object_name}_({group_index}).ply", binary=False)
    print(f"Exported combined clouds as {object_name}_({group_index}).ply")

    return f"./output/{object_name}_({group_index}).ply"


object_clouds = listdir(f"./{input_folder}")

print(object_clouds)

# Iterate over all groups, combine their clouds, and add them to the object MeshSet
for group_name in object_clouds:
    group_clouds = listdir(f"./{input_folder}/{group_name}")
    combined_group_mesh = combine_group_clouds(
        group_name, group_clouds, group_index)
    object_set.load_new_mesh(combined_group_mesh)
    group_index += 1

print("All groups combined into single object mesh.")

# Merge all group meshes into a single mesh representing the entire object
object_set.generate_by_merging_visible_meshes()

object_set.save_current_mesh(
    f"./output/{object_name}_combined.ply", binary=False)

print("Combined mesh saved as " +
      f"./output/{object_name}_combined.ply")

print("Done.")
