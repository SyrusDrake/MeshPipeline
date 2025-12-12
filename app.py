import gradio as gr
from poisson import mesh_analysis

depth_range = range(0, 13)  # Default is 8, max recommended is 12
# Default is 4.0, no idea what the recommended max is, arbritrarily set to 8.0
pointweight_range = range(0, 81, 5)
preclean: bool = False  # Default is False
mesh_statistics = {}
input_file: str


def upload_file(filepath):
    # Required to make upload button work.
    return filepath


def gui():
    """Draws the GUI for the mesh analyzer.

    Returns:
        None
    """

    with gr.Blocks() as comparison:

        gr.Markdown("# Mesh Analyzer")  # : Title of the app

        #: input mesh
        selected_file = gr.File(label="Input Mesh (.ply)", file_types=[
                                ".ply"], interactive=True)

        with gr.Row():
            #: depth range
            depth_range_slider_min = gr.Slider(label="min depth", minimum=depth_range.start, maximum=depth_range.stop -
                                               1, step=1, interactive=True)
            depth_range_slider_max = gr.Slider(label="max depth (inclusive)", minimum=depth_range.start, maximum=depth_range.stop -
                                               1, step=1, interactive=True)
        with gr.Row():
            #: pointweight range

            pointweight_range_slider_min = gr.Slider(
                label="min pointweight", minimum=pointweight_range.start/10, maximum=(pointweight_range.stop-1)/10, step=0.5, interactive=True)
            pointweight_range_slider_max = gr.Slider(
                label="max pointweight (inclusive)", minimum=pointweight_range.start/10, maximum=(pointweight_range.stop-1)/10, step=0.5, interactive=True)

        #: save mesh option
        save_mesh_checkbox = gr.Checkbox(
            label="Save Reconstructed Meshes", value=True, interactive=True)

        #: create csv option
        create_csv_checkbox = gr.Checkbox(
            label="Create CSV with Statistics", value=True, interactive=True)

        #: output folder
        output_folder_selector = gr.Textbox(
            label="Output Folder", placeholder="Enter output folder path", interactive=True, value="./output/")

        #: csv filename
        csv_filename_textbox = gr.Textbox(
            label="CSV Filename", placeholder="Enter CSV filename", interactive=True, value="mesh_statistics.csv")

        #: run button
        run_button = gr.Button("Run Mesh Analysis")
        run_button.click(fn=mesh_analysis,
                         inputs=[selected_file, depth_range_slider_min, depth_range_slider_max, pointweight_range_slider_min,
                                 pointweight_range_slider_max, output_folder_selector, save_mesh_checkbox, create_csv_checkbox, csv_filename_textbox],
                         outputs=[])

    comparison.launch(inbrowser=True)


if __name__ == "__main__":
    gui()
